import { relationalStore } from '@kit.ArkData';
import { Course, KnowledgePoint, LearningSession, DialogueRecord, ReviewRecord } from '../model/DataModel';

let rdbStore: relationalStore.RdbStore | null = null;

function getStore(): Promise<relationalStore.RdbStore> {
  return new Promise<relationalStore.RdbStore>((resolve, reject) => {
    if (rdbStore) {
      resolve(rdbStore);
      return;
    }
    relationalStore.getRdbStore(getContext(), {
      name: 'study_machine.db',
      securityLevel: relationalStore.SecurityLevel.S1,
    }, (err, store) => {
      if (err) { reject(err); return; }
      rdbStore = store;
      initTables(store).then(() => resolve(store)).catch(reject);
    });
  });
}

async function initTables(store: relationalStore.RdbStore): Promise<void> {
  console.info('[DatabaseHelper] Initializing database tables...');
  const sqls = [
    `CREATE TABLE IF NOT EXISTS courses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      description TEXT,
      is_sample INTEGER DEFAULT 0,
      created_at TEXT DEFAULT (datetime('now','localtime'))
    )`,
    `CREATE TABLE IF NOT EXISTS knowledge_points (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      course_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      content TEXT,
      created_at TEXT DEFAULT (datetime('now','localtime')),
      FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
    )`,
    `CREATE TABLE IF NOT EXISTS learning_sessions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      knowledge_point_id INTEGER NOT NULL,
      step TEXT NOT NULL,
      status TEXT DEFAULT 'in_progress',
      started_at TEXT DEFAULT (datetime('now','localtime')),
      completed_at TEXT,
      score REAL DEFAULT 0,
      FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id) ON DELETE CASCADE
    )`,
    `CREATE TABLE IF NOT EXISTS dialogue_records (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id INTEGER NOT NULL,
      turn_index INTEGER DEFAULT 0,
      user_input TEXT,
      ai_response TEXT,
      timestamp TEXT DEFAULT (datetime('now','localtime')),
      FOREIGN KEY (session_id) REFERENCES learning_sessions(id) ON DELETE CASCADE
    )`,
    `CREATE TABLE IF NOT EXISTS review_records (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      knowledge_point_id INTEGER NOT NULL,
      ease_factor REAL DEFAULT 2.5,
      interval_days INTEGER DEFAULT 1,
      next_review_date TEXT,
      last_reviewed_at TEXT,
      review_count INTEGER DEFAULT 0,
      avg_score REAL DEFAULT 0,
      status TEXT DEFAULT 'pending',
      FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id) ON DELETE CASCADE
    )`,
    `CREATE TABLE IF NOT EXISTS preferences (
      key TEXT PRIMARY KEY,
      value TEXT
    )`
  ];
  
  for (let i = 0; i < sqls.length; i++) {
    console.info('[DatabaseHelper] Creating table ' + (i + 1) + '/' + sqls.length);
    await new Promise<void>((resolve, reject) => {
      store.executeSql(sqls[i], [], (err) => { 
        if (err) {
          console.error('[DatabaseHelper] Failed to create table: ' + err.message);
          reject(err); 
        } else {
          resolve(); 
        }
      }); 
    });
  }
  console.info('[DatabaseHelper] Database tables initialized successfully');
}

function rowToCourse(rs: relationalStore.ResultSet): Course {
  return {
    id: rs.getLong(rs.getColumnIndex('id')),
    name: rs.getString(rs.getColumnIndex('name')),
    description: rs.getString(rs.getColumnIndex('description')),
    is_sample: rs.getLong(rs.getColumnIndex('is_sample')) === 1,
    created_at: rs.getString(rs.getColumnIndex('created_at')),
  };
}

function rowToKP(rs: relationalStore.ResultSet): KnowledgePoint {
  return {
    id: rs.getLong(rs.getColumnIndex('id')),
    course_id: rs.getLong(rs.getColumnIndex('course_id')),
    title: rs.getString(rs.getColumnIndex('title')),
    content: rs.getString(rs.getColumnIndex('content')),
    created_at: rs.getString(rs.getColumnIndex('created_at')),
  };
}

function rowToSession(rs: relationalStore.ResultSet): LearningSession {
  return {
    id: rs.getLong(rs.getColumnIndex('id')),
    knowledge_point_id: rs.getLong(rs.getColumnIndex('knowledge_point_id')),
    step: rs.getString(rs.getColumnIndex('step')),
    status: rs.getString(rs.getColumnIndex('status')),
    started_at: rs.getString(rs.getColumnIndex('started_at')),
    completed_at: rs.getString(rs.getColumnIndex('completed_at')),
    score: rs.getDouble(rs.getColumnIndex('score')),
  };
}

function rowToDialogue(rs: relationalStore.ResultSet): DialogueRecord {
  return {
    id: rs.getLong(rs.getColumnIndex('id')),
    session_id: rs.getLong(rs.getColumnIndex('session_id')),
    turn_index: rs.getLong(rs.getColumnIndex('turn_index')),
    user_input: rs.getString(rs.getColumnIndex('user_input')),
    ai_response: rs.getString(rs.getColumnIndex('ai_response')),
    timestamp: rs.getString(rs.getColumnIndex('timestamp')),
  };
}

function rowToReview(rs: relationalStore.ResultSet): ReviewRecord {
  return {
    id: rs.getLong(rs.getColumnIndex('id')),
    knowledge_point_id: rs.getLong(rs.getColumnIndex('knowledge_point_id')),
    ease_factor: rs.getDouble(rs.getColumnIndex('ease_factor')),
    interval_days: rs.getLong(rs.getColumnIndex('interval_days')),
    next_review_date: rs.getString(rs.getColumnIndex('next_review_date')),
    last_reviewed_at: rs.getString(rs.getColumnIndex('last_reviewed_at')),
    review_count: rs.getLong(rs.getColumnIndex('review_count')),
    avg_score: rs.getDouble(rs.getColumnIndex('avg_score')),
    status: rs.getString(rs.getColumnIndex('status')),
  };
}

export async function getAllCourses(): Promise<Course[]> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM courses ORDER BY created_at DESC', [], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  const courses: Course[] = [];
  while (rs.goToNextRow()) {
    courses.push(rowToCourse(rs));
  }
  return courses;
}

export async function getCourseById(id: number): Promise<Course | null> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM courses WHERE id = ?', [id], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) return rowToCourse(rs);
  return null;
}

export async function addCourse(name: string, description: string, isSample: boolean): Promise<number> {
  console.info('[DatabaseHelper] Adding course: ' + name);
  const store = await getStore();
  await new Promise<void>((resolve, reject) => {
    store.executeSql('INSERT INTO courses (name, description, is_sample) VALUES (?, ?, ?)',
      [name, description, isSample ? 1 : 0], (err) => { 
        if (err) {
          console.error('[DatabaseHelper] Failed to add course: ' + err.message);
          reject(err); 
        } else {
          resolve(); 
        }
      });
  });
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT last_insert_rowid() as id', [], (err, rs) => { 
      if (err) reject(err); 
      else resolve(rs); 
    });
  });
  rs.goToFirstRow();
  const id = rs.getLong(rs.getColumnIndex('id'));
  console.info('[DatabaseHelper] Course added with id: ' + id);
  return id;
}

export async function addKnowledgePoint(courseId: number, title: string, content: string): Promise<number> {
  console.info('[DatabaseHelper] Adding knowledge point: ' + title + ' for courseId: ' + courseId);
  const store = await getStore();
  await new Promise<void>((resolve, reject) => {
    store.executeSql('INSERT INTO knowledge_points (course_id, title, content) VALUES (?, ?, ?)',
      [courseId, title, content], (err) => { 
        if (err) {
          console.error('[DatabaseHelper] Failed to add KP: ' + err.message);
          reject(err); 
        } else {
          resolve(); 
        }
      });
  });
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT last_insert_rowid() as id', [], (err, rs) => { 
      if (err) reject(err); 
      else resolve(rs); 
    });
  });
  rs.goToFirstRow();
  const id = rs.getLong(rs.getColumnIndex('id'));
  console.info('[DatabaseHelper] KP added with id: ' + id);
  return id;
}

export async function getCourseCount(): Promise<number> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT COUNT(*) as cnt FROM courses', [], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  rs.goToFirstRow();
  return rs.getLong(rs.getColumnIndex('cnt'));
}

export async function getKnowledgePoints(courseId: number): Promise<KnowledgePoint[]> {
  return getKnowledgePointsByCourse(courseId);
}

export async function getKnowledgePointsByCourse(courseId: number): Promise<KnowledgePoint[]> {
  console.info('[DatabaseHelper] getKnowledgePointsByCourse for courseId: ' + courseId);
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM knowledge_points WHERE course_id = ? ORDER BY id ASC', [courseId], (err, rs) => {
      if (err) {
        console.error('[DatabaseHelper] Query failed: ' + err.message);
        reject(err);
      } else {
        resolve(rs);
      }
    });
  });
  const kps: KnowledgePoint[] = [];
  while (rs.goToNextRow()) {
    kps.push(rowToKP(rs));
  }
  console.info('[DatabaseHelper] Found ' + kps.length + ' knowledge points');
  return kps;
}

export async function getKnowledgePointById(id: number): Promise<KnowledgePoint | null> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM knowledge_points WHERE id = ?', [id], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) return rowToKP(rs);
  return null;
}

export async function getKpCount(courseId: number): Promise<number> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT COUNT(*) as cnt FROM knowledge_points WHERE course_id = ?', [courseId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  rs.goToFirstRow();
  return rs.getLong(rs.getColumnIndex('cnt'));
}

export async function getOrCreateSession(kpId: number, step: string): Promise<number> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT id FROM learning_sessions WHERE knowledge_point_id = ? AND step = ? AND status = 'in_progress' LIMIT 1", [kpId, step], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) {
    return rs.getLong(rs.getColumnIndex('id'));
  }
  await new Promise<void>((resolve, reject) => {
    store.executeSql("INSERT INTO learning_sessions (knowledge_point_id, step, status, started_at, score) VALUES (?, ?, 'in_progress', datetime('now','localtime'), 0)", [kpId, step], (err) => { if (err) reject(err); else resolve(); });
  });
  const rs2 = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT last_insert_rowid() as id', [], (err, rs) => { if (err) reject(err); else resolve(rs); });
  });
  rs2.goToFirstRow();
  return rs2.getLong(rs2.getColumnIndex('id'));
}

export async function getSessionByKpAndStep(kpId: number, step: string): Promise<LearningSession | null> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT * FROM learning_sessions WHERE knowledge_point_id = ? AND step = ? AND status = 'completed' ORDER BY completed_at DESC LIMIT 1", [kpId, step], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) return rowToSession(rs);
  return null;
}

export async function getInProgressSessionsByKP(kpId: number): Promise<LearningSession[]> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT * FROM learning_sessions WHERE knowledge_point_id = ? AND status = 'in_progress'", [kpId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  const sessions: LearningSession[] = [];
  while (rs.goToNextRow()) {
    sessions.push(rowToSession(rs));
  }
  return sessions;
}

export async function getSessionsByKP(kpId: number): Promise<LearningSession[]> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM learning_sessions WHERE knowledge_point_id = ? ORDER BY started_at DESC', [kpId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  const sessions: LearningSession[] = [];
  while (rs.goToNextRow()) {
    sessions.push(rowToSession(rs));
  }
  return sessions;
}

export async function getSessionById(id: number): Promise<LearningSession | null> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM learning_sessions WHERE id = ?', [id], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) return rowToSession(rs);
  return null;
}

export async function updateSessionScore(sessionId: number, score: number, complete: boolean): Promise<void> {
  const store = await getStore();
  if (complete) {
    await new Promise<void>((resolve, reject) => {
      store.executeSql("UPDATE learning_sessions SET score = ?, status = 'completed', completed_at = datetime('now','localtime') WHERE id = ?", [score, sessionId], (err) => { if (err) reject(err); else resolve(); });
    });
  } else {
    await new Promise<void>((resolve, reject) => {
      store.executeSql('UPDATE learning_sessions SET score = ? WHERE id = ?', [score, sessionId], (err) => { if (err) reject(err); else resolve(); });
    });
  }
}

export async function getCompletedSessionCount(kpId: number): Promise<number> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT COUNT(*) as cnt FROM learning_sessions WHERE knowledge_point_id = ? AND status = 'completed' AND score > 0", [kpId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  rs.goToFirstRow();
  return rs.getLong(rs.getColumnIndex('cnt'));
}

export async function getAvgScore(kpId: number): Promise<number> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT AVG(score) as avg_score FROM learning_sessions WHERE knowledge_point_id = ? AND status = 'completed' AND score > 0", [kpId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) {
    return rs.getDouble(rs.getColumnIndex('avg_score'));
  }
  return 0;
}

export async function getCompletedSessionCountByCourse(courseId: number): Promise<number> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT COUNT(*) as cnt FROM learning_sessions ls JOIN knowledge_points kp ON ls.knowledge_point_id = kp.id WHERE kp.course_id = ? AND ls.status = 'completed' AND ls.score > 0", [courseId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  rs.goToFirstRow();
  return rs.getLong(rs.getColumnIndex('cnt'));
}

export async function getAvgScoreByCourse(courseId: number): Promise<number> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT AVG(ls.score) as avg_score FROM learning_sessions ls JOIN knowledge_points kp ON ls.knowledge_point_id = kp.id WHERE kp.course_id = ? AND ls.status = 'completed' AND ls.score > 0", [courseId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) {
    return rs.getDouble(rs.getColumnIndex('avg_score'));
  }
  return 0;
}

export async function addDialogue(sessionId: number, turnIndex: number, userInput: string, aiResponse: string): Promise<void> {
  const store = await getStore();
  await new Promise<void>((resolve, reject) => {
    store.executeSql('INSERT INTO dialogue_records (session_id, turn_index, user_input, ai_response) VALUES (?, ?, ?, ?)', [sessionId, turnIndex, userInput, aiResponse], (err) => { if (err) reject(err); else resolve(); });
  });
}

export async function getDialogues(sessionId: number): Promise<DialogueRecord[]> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM dialogue_records WHERE session_id = ? ORDER BY turn_index ASC', [sessionId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  const records: DialogueRecord[] = [];
  while (rs.goToNextRow()) {
    records.push(rowToDialogue(rs));
  }
  return records;
}

export async function getReviewRecord(kpId: number): Promise<ReviewRecord | null> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM review_records WHERE knowledge_point_id = ? LIMIT 1', [kpId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) return rowToReview(rs);
  return null;
}

export async function saveReviewRecord(kpId: number, easeFactor: number, intervalDays: number, nextReviewDate: string, reviewCount: number, avgScore: number, status: string): Promise<void> {
  const store = await getStore();
  const existing = await getReviewRecord(kpId);
  if (existing) {
    await new Promise<void>((resolve, reject) => {
      store.executeSql("UPDATE review_records SET ease_factor = ?, interval_days = ?, next_review_date = ?, last_reviewed_at = datetime('now','localtime'), review_count = ?, avg_score = ?, status = ? WHERE knowledge_point_id = ?", [easeFactor, intervalDays, nextReviewDate, reviewCount, avgScore, status, kpId], (err) => { if (err) reject(err); else resolve(); });
    });
  } else {
    await new Promise<void>((resolve, reject) => {
      store.executeSql("INSERT INTO review_records (knowledge_point_id, ease_factor, interval_days, next_review_date, last_reviewed_at, review_count, avg_score, status) VALUES (?, ?, ?, ?, datetime('now','localtime'), ?, ?, ?)", [kpId, easeFactor, intervalDays, nextReviewDate, reviewCount, avgScore, status], (err) => { if (err) reject(err); else resolve(); });
    });
  }
}

interface ReviewDueItem {
  id: number;
  knowledge_point_id: number;
  ease_factor: number;
  interval_days: number;
  next_review_date: string;
  review_count: number;
  avg_score: number;
  kp_title: string;
  course_name: string;
}

export async function getReviewsDue(): Promise<ReviewDueItem[]> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT r.*, kp.title as kp_title, c.name as course_name FROM review_records r JOIN knowledge_points kp ON r.knowledge_point_id = kp.id JOIN courses c ON kp.course_id = c.id WHERE r.next_review_date <= datetime('now','localtime') AND r.status = 'pending' ORDER BY r.next_review_date ASC", [], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  const items: ReviewDueItem[] = [];
  while (rs.goToNextRow()) {
    items.push({
      id: rs.getLong(rs.getColumnIndex('id')),
      knowledge_point_id: rs.getLong(rs.getColumnIndex('knowledge_point_id')),
      ease_factor: rs.getDouble(rs.getColumnIndex('ease_factor')),
      interval_days: rs.getLong(rs.getColumnIndex('interval_days')),
      next_review_date: rs.getString(rs.getColumnIndex('next_review_date')),
      review_count: rs.getLong(rs.getColumnIndex('review_count')),
      avg_score: rs.getDouble(rs.getColumnIndex('avg_score')),
      kp_title: rs.getString(rs.getColumnIndex('kp_title')),
      course_name: rs.getString(rs.getColumnIndex('course_name')),
    });
  }
  return items;
}

export async function getPreference(key: string): Promise<string | null> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT value FROM preferences WHERE key = ?', [key], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  if (rs.goToFirstRow()) {
    return rs.getString(rs.getColumnIndex('value'));
  }
  return null;
}

export async function setPreference(key: string, value: string): Promise<void> {
  const store = await getStore();
  await new Promise<void>((resolve, reject) => {
    store.executeSql('INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)', [key, value], (err) => { if (err) reject(err); else resolve(); });
  });
}
