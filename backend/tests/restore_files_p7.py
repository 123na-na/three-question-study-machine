"""Part 7: Rewrite services as function-based (most codebase uses this API)"""
import os

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

def write_file(rel_path, content):
    fp = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Restored: {rel_path}')

# ---- DatabaseHelper (function-based, with all methods needed by ProfileTab) ----
write_file('service/DatabaseHelper.ets', """\
import { relationalStore } from '@kit.ArkData';
import { Course, KnowledgePoint, LearningSession, DialogueRecord, ReviewRecord } from '../model/DataModel';

let rdbStore: relationalStore.RdbStore | null = null;

function getStore(): Promise<relationalStore.RdbStore> {
  return new Promise<relationalStore.RdbStore>((resolve, reject) => {
    if (rdbStore) {
      resolve(rdbStore);
      return;
    }
    const context = getContext(this);
    relationalStore.getRdbStore(context, {
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
  for (const sql of sqls) {
    await new Promise<void>((resolve, reject) => {
      store.executeSql(sql, [], () => resolve(), (err) => reject(err));
    });
  }
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

export async function getKnowledgePointsByCourse(courseId: number): Promise<KnowledgePoint[]> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT * FROM knowledge_points WHERE course_id = ? ORDER BY id ASC', [courseId], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  const kps: KnowledgePoint[] = [];
  while (rs.goToNextRow()) {
    kps.push(rowToKP(rs));
  }
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
    store.executeSql("INSERT INTO learning_sessions (knowledge_point_id, step, status, started_at, score) VALUES (?, ?, 'in_progress', datetime('now','localtime'), 0)", [kpId, step], () => resolve(), (err) => reject(err));
  });
  const rs2 = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql('SELECT last_insert_rowid() as id', [], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
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
      store.executeSql("UPDATE learning_sessions SET score = ?, status = 'completed', completed_at = datetime('now','localtime') WHERE id = ?", [score, sessionId], () => resolve(), (err) => reject(err));
    });
  } else {
    await new Promise<void>((resolve, reject) => {
      store.executeSql('UPDATE learning_sessions SET score = ? WHERE id = ?', [score, sessionId], () => resolve(), (err) => reject(err));
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

export async function addDialogue(sessionId: number, turnIndex: number, userInput: string, aiResponse: string): Promise<void> {
  const store = await getStore();
  await new Promise<void>((resolve, reject) => {
    store.executeSql('INSERT INTO dialogue_records (session_id, turn_index, user_input, ai_response) VALUES (?, ?, ?, ?)', [sessionId, turnIndex, userInput, aiResponse], () => resolve(), (err) => reject(err));
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
      store.executeSql("UPDATE review_records SET ease_factor = ?, interval_days = ?, next_review_date = ?, last_reviewed_at = datetime('now','localtime'), review_count = ?, avg_score = ?, status = ? WHERE knowledge_point_id = ?", [easeFactor, intervalDays, nextReviewDate, reviewCount, avgScore, status, kpId], () => resolve(), (err) => reject(err));
    });
  } else {
    await new Promise<void>((resolve, reject) => {
      store.executeSql("INSERT INTO review_records (knowledge_point_id, ease_factor, interval_days, next_review_date, last_reviewed_at, review_count, avg_score, status) VALUES (?, ?, ?, ?, datetime('now','localtime'), ?, ?, ?)", [kpId, easeFactor, intervalDays, nextReviewDate, reviewCount, avgScore, status], () => resolve(), (err) => reject(err));
    });
  }
}

export async function getReviewsDue(): Promise<any[]> {
  const store = await getStore();
  const rs = await new Promise<relationalStore.ResultSet>((resolve, reject) => {
    store.querySql("SELECT r.*, kp.title as kp_title, c.name as course_name FROM review_records r JOIN knowledge_points kp ON r.knowledge_point_id = kp.id JOIN courses c ON kp.course_id = c.id WHERE r.next_review_date <= datetime('now','localtime') AND r.status = 'pending' ORDER BY r.next_review_date ASC", [], (err, rs) => {
      if (err) reject(err); else resolve(rs);
    });
  });
  const items: any[] = [];
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
    store.executeSql('INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)', [key, value], () => resolve(), (err) => reject(err));
  });
}
""")

# ---- AuthService (function-based) ----
write_file('service/AuthService.ets', """\
import { getPreference, setPreference } from './DatabaseHelper';

export async function getNickname(): Promise<string | null> {
  return await getPreference('nickname');
}

export async function setNickname(name: string): Promise<void> {
  await setPreference('nickname', name);
}

export async function getUserId(): Promise<string | null> {
  let uid = await getPreference('user_id');
  if (!uid) {
    uid = 'user_' + Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
    await setPreference('user_id', uid);
  }
  return uid;
}

export async function isLoggedIn(): Promise<boolean> {
  const name = await getNickname();
  return name !== null && name.length > 0;
}
""")

# ---- AIService (function-based with setBaseUrl + initFromPreferences) ----
write_file('service/AIService.ets', """\
import http from '@ohos.net.http';
import { API_CONFIG } from '../constants/AppConstants';
import { AIEvaluationResponse } from '../model/DataModel';
import { getPreference, setPreference } from './DatabaseHelper';

const PREF_BACKEND_URL = 'backend_url';

export async function getBaseUrl(): Promise<string> {
  const saved = await getPreference(PREF_BACKEND_URL);
  return saved || API_CONFIG.BASE_URL;
}

export async function setBaseUrl(url: string): Promise<void> {
  await setPreference(PREF_BACKEND_URL, url);
  API_CONFIG.BASE_URL = url;
}

export async function initFromPreferences(): Promise<void> {
  const saved = await getPreference(PREF_BACKEND_URL);
  if (saved) {
    API_CONFIG.BASE_URL = saved;
  }
}

export async function evaluateWithAI(question: string, userAnswer: string, step: string): Promise<AIEvaluationResponse> {
  const baseUrl = await getBaseUrl();
  const url = baseUrl + API_CONFIG.ENDPOINTS.EVALUATE;
  const httpRequest = http.createHttp();
  const body = { question, user_answer: userAnswer, step };
  const extraOpts: http.HttpRequestOptions = {
    method: http.RequestMethod.POST,
    header: { 'Content-Type': 'application/json' },
    extraData: JSON.stringify(body),
    connectTimeout: API_CONFIG.TIMEOUT,
    readTimeout: API_CONFIG.TIMEOUT,
  };
  return new Promise<AIEvaluationResponse>((resolve, reject) => {
    httpRequest.request(url, extraOpts, (err, data) => {
      httpRequest.destroy();
      if (err) {
        reject(new Error('HTTP ' + err.code + ': ' + err.message));
        return;
      }
      const code = data.responseCode;
      if (code !== 200) {
        reject(new Error('Server error: ' + code));
        return;
      }
      try {
        const result: AIEvaluationResponse = JSON.parse(data.result as string);
        resolve(result);
      } catch (e) {
        reject(new Error('Failed to parse AI response'));
      }
    });
  });
}

export function evaluateWithAIStream(onData: (chunk: string) => void, onDone: () => void, onError: (err: Error) => void): void {
  setTimeout(() => {
    onDone();
  }, 100);
}
""")

# ---- SpacedRepetitionService (function-based with loop fix) ----
write_file('service/SpacedRepetitionService.ets', """\
import { ReviewRecord } from '../model/DataModel';
import { getReviewRecord, saveReviewRecord } from './DatabaseHelper';

const MIN_INTERVAL = 1;
const MAX_INTERVAL = 365;
const EASE_FACTOR_MIN = 1.3;
const EASE_FACTOR_MAX = 3.5;
const EASE_FACTOR_INITIAL = 2.5;

export function calculateNextReview(score: number, currentEaseFactor: number, currentInterval: number, currentReviewCount: number): {
  easeFactor: number;
  intervalDays: number;
  nextReviewDate: string;
} {
  let newEaseFactor = currentEaseFactor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02));
  newEaseFactor = Math.max(EASE_FACTOR_MIN, Math.min(EASE_FACTOR_MAX, newEaseFactor));

  let newInterval: number;
  if (currentReviewCount === 0) {
    newInterval = MIN_INTERVAL;
  } else if (currentReviewCount === 1) {
    newInterval = 6;
  } else {
    newInterval = Math.round(currentInterval * newEaseFactor);
  }
  newInterval = Math.max(MIN_INTERVAL, Math.min(MAX_INTERVAL, newInterval));

  const now = new Date();
  const nextDate = new Date(now.getTime() + newInterval * 24 * 60 * 60 * 1000);
  const nextReviewDate = nextDate.getFullYear() + '-' +
    String(nextDate.getMonth() + 1).padStart(2, '0') + '-' +
    String(nextDate.getDate()).padStart(2, '0');

  return { easeFactor: newEaseFactor, intervalDays: newInterval, nextReviewDate };
}

export async function processReviewResult(kpId: number, score: number): Promise<void> {
  const normalizedScore = Math.round(score / 20);
  let review: ReviewRecord | null = null;
  try {
    review = await getReviewRecord(kpId);
  } catch (_) {
    review = null;
  }
  const easeFactor = review ? review.ease_factor : EASE_FACTOR_INITIAL;
  const intervalDays = review ? review.interval_days : 0;
  const reviewCount = review ? review.review_count : 0;
  const avgScore = review ? review.avg_score : 0;

  const result = calculateNextReview(normalizedScore, easeFactor, intervalDays, reviewCount);
  const newAvgScore = reviewCount > 0 ? (avgScore * reviewCount + score) / (reviewCount + 1) : score;
  let newStatus = 'pending';
  if (score >= 80) {
    newStatus = 'mastered';
  } else if (normalizedScore < 3) {
    newStatus = 'overdue';
  }
  await saveReviewRecord(kpId, result.easeFactor, result.intervalDays, result.nextReviewDate, reviewCount + 1, newAvgScore, newStatus);
}
""")

# ---- SampleCourseLoader (function-based) ----
write_file('service/SampleCourseLoader.ets', """\
import { getCourseCount, addCourse, addKnowledgePoint } from './DatabaseHelper';

const SAMPLE_COURSES = [
  {
    name: 'Python 编程入门',
    description: '学习 Python 编程语言的基础知识，包括变量、数据类型、控制流和函数',
    knowledgePoints: [
      { title: '变量与数据类型', content: 'Python 中的变量不需要声明类型，可以直接赋值。常见数据类型包括整数(int)、浮点数(float)、字符串(str)、布尔值(bool)、列表(list)、元组(tuple)、字典(dict)等。' },
      { title: '条件语句与循环', content: '条件语句使用 if/elif/else 进行分支判断。循环包括 for 循环（用于遍历可迭代对象）和 while 循环（条件满足时持续执行）。' },
      { title: '函数定义与使用', content: '函数使用 def 关键字定义。支持位置参数、默认参数、关键字参数和可变参数。函数可以返回值，也可以返回多个值（实际是元组）。' },
    ]
  },
  {
    name: '数据结构与算法',
    description: '掌握常用的数据结构和经典算法，提升编程解决问题的能力',
    knowledgePoints: [
      { title: '数组与链表', content: '数组是连续内存空间上相同类型元素的集合，支持随机访问。链表由节点组成，每个节点包含数据和指向下一个节点的指针，分为单链表、双链表和循环链表。' },
      { title: '栈与队列', content: '栈是后进先出(LIFO)的数据结构，主要操作有入栈(push)和出栈(pop)。队列是先进先出(FIFO)的数据结构，主要操作有入队(enqueue)和出队(dequeue)。' },
      { title: '二叉树与遍历', content: '二叉树每个节点最多有两个子节点。遍历方式包括前序遍历(根左右)、中序遍历(左根右)、后序遍历(左右根)和层序遍历。' },
    ]
  },
  {
    name: '操作系统原理',
    description: '理解操作系统核心概念：进程管理、内存管理、文件系统和设备管理',
    knowledgePoints: [
      { title: '进程与线程', content: '进程是资源分配的基本单位，线程是CPU调度的基本单位。进程间通信方式包括管道、消息队列、共享内存、信号量和套接字。多线程编程需要注意同步与互斥问题。' },
      { title: '内存管理', content: '内存管理包括内存分配与回收、地址转换、内存保护和内存扩充。虚拟内存技术允许程序执行时只将部分内容装入内存，通过页面置换算法管理。' },
      { title: '文件系统', content: '文件系统负责管理磁盘上的数据存储和检索。常见的文件系统有FAT32、NTFS、ext4等。文件系统采用目录树结构组织文件，支持文件的创建、读写、删除等操作。' },
    ]
  },
  {
    name: '计算机网络',
    description: '学习计算机网络的基本概念、协议体系结构和网络应用',
    knowledgePoints: [
      { title: 'TCP/IP 协议栈', content: 'TCP/IP 协议栈分为应用层、传输层、网络层和网络接口层。应用层协议包括HTTP、FTP、SMTP等，传输层有TCP（可靠）和UDP（快速），网络层核心是IP协议。' },
      { title: 'HTTP 协议', content: 'HTTP是超文本传输协议，基于请求-响应模型。主要方法有GET（获取资源）、POST（提交数据）、PUT（更新资源）和DELETE（删除资源）。状态码分为1xx信息、2xx成功、3xx重定向、4xx客户端错误、5xx服务器错误。' },
      { title: '网络安全基础', content: '网络安全包括机密性、完整性和可用性三大目标。常见安全技术有对称加密（AES）、非对称加密（RSA）、数字签名、数字证书、SSL/TLS协议和防火墙。' },
    ]
  },
  {
    name: '数据库系统概论',
    description: '掌握关系数据库的核心概念，SQL语言和数据库设计方法',
    knowledgePoints: [
      { title: '关系模型与SQL', content: '关系模型使用二维表表示数据，每行是一条记录，每列是一个属性。SQL包括数据定义语言(DDL)、数据操纵语言(DML)和数据控制语言(DCL)。基本操作有SELECT、INSERT、UPDATE、DELETE。' },
      { title: '数据库设计', content: '数据库设计遵循规范化理论：第一范式(1NF)要求属性不可分，第二范式(2NF)消除部分依赖，第三范式(3NF)消除传递依赖。通过ER图进行概念设计，转换为关系模型。' },
      { title: '事务与并发控制', content: '事务具有ACID特性：原子性、一致性、隔离性和持久性。并发控制主要解决丢失修改、读脏数据和不可重复读问题。封锁协议包括共享锁和排他锁，隔离级别从低到高包括READ UNCOMMITTED到SERIALIZABLE。' },
    ]
  },
];

export async function loadSampleCoursesIfNeeded(): Promise<void> {
  try {
    const count = await getCourseCount();
    if (count > 0) {
      return;
    }
    for (const course of SAMPLE_COURSES) {
      const courseId = await addCourse(course.name, course.description, true);
      for (const kp of course.knowledgePoints) {
        await addKnowledgePoint(courseId, kp.title, kp.content);
      }
    }
    console.info('[SampleCourseLoader] Sample courses loaded successfully');
  } catch (err) {
    console.error('[SampleCourseLoader] Failed to load sample courses: ' + JSON.stringify(err));
  }
}
""")

print('Part 7: All services unified to function-based API')
print('Run part 8 for ProfileTab.ets with function-based API')
