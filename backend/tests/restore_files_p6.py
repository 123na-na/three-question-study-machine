"""Part 6: Restore DatabaseHelper and AuthService to original class-based API
AND write ProfileTab.ets with the correct API
"""
import os

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

def write_file(rel_path, content):
    fp = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Restored: {rel_path}')

# ---- DatabaseHelper (class-based original that compiled successfully) ----
write_file('service/DatabaseHelper.ets', """\
import { relationalStore } from '@kit.ArkData';
import { Course, KnowledgePoint, LearningSession, DialogueRecord, ReviewRecord } from '../model/DataModel';

export class DatabaseHelper {
  private store: relationalStore.RdbStore | null = null;
  private context: Context;

  constructor(context: Context) {
    this.context = context;
  }

  async init(): Promise<void> {
    const config: relationalStore.StoreConfig = {
      name: 'study_machine.db',
      securityLevel: relationalStore.SecurityLevel.S1,
    };
    this.store = await new Promise<relationalStore.RdbStore>((resolve, reject) => {
      relationalStore.getRdbStore(this.context, config, (err, store) => {
        if (err) reject(err);
        else resolve(store);
      });
    });
    await this.createTables();
  }

  private async createTables(): Promise<void> {
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
        this.store!.executeSql(sql, [], () => resolve(), (err) => reject(err));
      });
    }
  }

  async getAllCourses(): Promise<Course[]> {
    const rs = await this.query('SELECT * FROM courses ORDER BY created_at DESC');
    const courses: Course[] = [];
    while (rs.goToNextRow()) {
      courses.push(this.rowToCourse(rs));
    }
    return courses;
  }

  async getCourseById(id: number): Promise<Course | null> {
    const rs = await this.query('SELECT * FROM courses WHERE id = ?', [id]);
    if (rs.goToFirstRow()) return this.rowToCourse(rs);
    return null;
  }

  async addCourse(name: string, description: string, isSample: boolean): Promise<number> {
    await this.execute('INSERT INTO courses (name, description, is_sample) VALUES (?, ?, ?)', [name, description, isSample ? 1 : 0]);
    return await this.lastInsertId();
  }

  async deleteCourse(id: number): Promise<void> {
    await this.execute('DELETE FROM knowledge_points WHERE course_id = ?', [id]);
    await this.execute('DELETE FROM courses WHERE id = ?', [id]);
  }

  async getCourseCount(): Promise<number> {
    const rs = await this.query('SELECT COUNT(*) as cnt FROM courses');
    rs.goToFirstRow();
    return rs.getLong(rs.getColumnIndex('cnt'));
  }

  async getKnowledgePointsByCourse(courseId: number): Promise<KnowledgePoint[]> {
    const rs = await this.query('SELECT * FROM knowledge_points WHERE course_id = ? ORDER BY id ASC', [courseId]);
    const kps: KnowledgePoint[] = [];
    while (rs.goToNextRow()) {
      kps.push(this.rowToKP(rs));
    }
    return kps;
  }

  async getKnowledgePointById(id: number): Promise<KnowledgePoint | null> {
    const rs = await this.query('SELECT * FROM knowledge_points WHERE id = ?', [id]);
    if (rs.goToFirstRow()) return this.rowToKP(rs);
    return null;
  }

  async getKpCount(courseId: number): Promise<number> {
    const rs = await this.query('SELECT COUNT(*) as cnt FROM knowledge_points WHERE course_id = ?', [courseId]);
    rs.goToFirstRow();
    return rs.getLong(rs.getColumnIndex('cnt'));
  }

  async addKnowledgePoint(courseId: number, title: string, content: string): Promise<number> {
    await this.execute('INSERT INTO knowledge_points (course_id, title, content) VALUES (?, ?, ?)', [courseId, title, content]);
    return await this.lastInsertId();
  }

  async deleteKnowledgePoint(id: number): Promise<void> {
    await this.execute('DELETE FROM knowledge_points WHERE id = ?', [id]);
  }

  async getOrCreateSession(kpId: number, step: string): Promise<number> {
    const rs = await this.query("SELECT id FROM learning_sessions WHERE knowledge_point_id = ? AND step = ? AND status = 'in_progress' LIMIT 1", [kpId, step]);
    if (rs.goToFirstRow()) {
      return rs.getLong(rs.getColumnIndex('id'));
    }
    await this.execute("INSERT INTO learning_sessions (knowledge_point_id, step, status, started_at, score) VALUES (?, ?, 'in_progress', datetime('now','localtime'), 0)", [kpId, step]);
    return await this.lastInsertId();
  }

  async getSessionByKpAndStep(kpId: number, step: string): Promise<LearningSession | null> {
    const rs = await this.query("SELECT * FROM learning_sessions WHERE knowledge_point_id = ? AND step = ? AND status = 'completed' ORDER BY completed_at DESC LIMIT 1", [kpId, step]);
    if (rs.goToFirstRow()) return this.rowToSession(rs);
    return null;
  }

  async getSessionsByKP(kpId: number): Promise<LearningSession[]> {
    const rs = await this.query('SELECT * FROM learning_sessions WHERE knowledge_point_id = ? ORDER BY started_at DESC', [kpId]);
    const sessions: LearningSession[] = [];
    while (rs.goToNextRow()) {
      sessions.push(this.rowToSession(rs));
    }
    return sessions;
  }

  async getSessionById(id: number): Promise<LearningSession | null> {
    const rs = await this.query('SELECT * FROM learning_sessions WHERE id = ?', [id]);
    if (rs.goToFirstRow()) return this.rowToSession(rs);
    return null;
  }

  async updateSessionScore(sessionId: number, score: number, complete: boolean): Promise<void> {
    if (complete) {
      await this.execute("UPDATE learning_sessions SET score = ?, status = 'completed', completed_at = datetime('now','localtime') WHERE id = ?", [score, sessionId]);
    } else {
      await this.execute('UPDATE learning_sessions SET score = ? WHERE id = ?', [score, sessionId]);
    }
  }

  async getCompletedSessionCount(kpId: number): Promise<number> {
    const rs = await this.query("SELECT COUNT(*) as cnt FROM learning_sessions WHERE knowledge_point_id = ? AND status = 'completed' AND score > 0", [kpId]);
    rs.goToFirstRow();
    return rs.getLong(rs.getColumnIndex('cnt'));
  }

  async getAvgScore(kpId: number): Promise<number> {
    const rs = await this.query("SELECT AVG(score) as avg_score FROM learning_sessions WHERE knowledge_point_id = ? AND status = 'completed' AND score > 0", [kpId]);
    if (rs.goToFirstRow()) {
      return rs.getDouble(rs.getColumnIndex('avg_score'));
    }
    return 0;
  }

  async addDialogue(sessionId: number, turnIndex: number, userInput: string, aiResponse: string): Promise<void> {
    await this.execute('INSERT INTO dialogue_records (session_id, turn_index, user_input, ai_response) VALUES (?, ?, ?, ?)', [sessionId, turnIndex, userInput, aiResponse]);
  }

  async getDialogues(sessionId: number): Promise<DialogueRecord[]> {
    const rs = await this.query('SELECT * FROM dialogue_records WHERE session_id = ? ORDER BY turn_index ASC', [sessionId]);
    const records: DialogueRecord[] = [];
    while (rs.goToNextRow()) {
      records.push(this.rowToDialogue(rs));
    }
    return records;
  }

  async getReviewRecord(kpId: number): Promise<ReviewRecord | null> {
    const rs = await this.query('SELECT * FROM review_records WHERE knowledge_point_id = ? LIMIT 1', [kpId]);
    if (rs.goToFirstRow()) return this.rowToReview(rs);
    return null;
  }

  async saveReviewRecord(kpId: number, easeFactor: number, intervalDays: number, nextReviewDate: string, reviewCount: number, avgScore: number, status: string): Promise<void> {
    const existing = await this.getReviewRecord(kpId);
    if (existing) {
      await this.execute('UPDATE review_records SET ease_factor = ?, interval_days = ?, next_review_date = ?, last_reviewed_at = datetime(\'now\',\'localtime\'), review_count = ?, avg_score = ?, status = ? WHERE knowledge_point_id = ?', [easeFactor, intervalDays, nextReviewDate, reviewCount, avgScore, status, kpId]);
    } else {
      await this.execute("INSERT INTO review_records (knowledge_point_id, ease_factor, interval_days, next_review_date, last_reviewed_at, review_count, avg_score, status) VALUES (?, ?, ?, ?, datetime('now','localtime'), ?, ?, ?)", [kpId, easeFactor, intervalDays, nextReviewDate, reviewCount, avgScore, status]);
    }
  }

  async getReviewsDue(): Promise<any[]> {
    const rs = await this.query("SELECT r.*, kp.title as kp_title, c.name as course_name FROM review_records r JOIN knowledge_points kp ON r.knowledge_point_id = kp.id JOIN courses c ON kp.course_id = c.id WHERE r.next_review_date <= datetime('now','localtime') AND r.status = 'pending' ORDER BY r.next_review_date ASC");
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

  async getPreference(key: string): Promise<string | null> {
    const rs = await this.query('SELECT value FROM preferences WHERE key = ?', [key]);
    if (rs.goToFirstRow()) {
      return rs.getString(rs.getColumnIndex('value'));
    }
    return null;
  }

  async setPreference(key: string, value: string): Promise<void> {
    await this.execute('INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)', [key, value]);
  }

  async close(): Promise<void> {
    if (this.store) {
      await new Promise<void>((resolve, reject) => {
        this.store!.close();
        resolve();
      });
      this.store = null;
    }
  }

  private async query(sql: string, params: any[] = []): Promise<relationalStore.ResultSet> {
    return new Promise((resolve, reject) => {
      this.store!.querySql(sql, params, (err, rs) => {
        if (err) reject(err);
        else resolve(rs);
      });
    });
  }

  private async execute(sql: string, params: any[] = []): Promise<void> {
    return new Promise((resolve, reject) => {
      this.store!.executeSql(sql, params, () => resolve(), (err) => reject(err));
    });
  }

  private async lastInsertId(): Promise<number> {
    const rs = await this.query('SELECT last_insert_rowid() as id');
    rs.goToFirstRow();
    return rs.getLong(rs.getColumnIndex('id'));
  }

  private rowToCourse(rs: relationalStore.ResultSet): Course {
    return {
      id: rs.getLong(rs.getColumnIndex('id')),
      name: rs.getString(rs.getColumnIndex('name')),
      description: rs.getString(rs.getColumnIndex('description')),
      is_sample: rs.getLong(rs.getColumnIndex('is_sample')) === 1,
      created_at: rs.getString(rs.getColumnIndex('created_at')),
    };
  }

  private rowToKP(rs: relationalStore.ResultSet): KnowledgePoint {
    return {
      id: rs.getLong(rs.getColumnIndex('id')),
      course_id: rs.getLong(rs.getColumnIndex('course_id')),
      title: rs.getString(rs.getColumnIndex('title')),
      content: rs.getString(rs.getColumnIndex('content')),
      created_at: rs.getString(rs.getColumnIndex('created_at')),
    };
  }

  private rowToSession(rs: relationalStore.ResultSet): LearningSession {
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

  private rowToDialogue(rs: relationalStore.ResultSet): DialogueRecord {
    return {
      id: rs.getLong(rs.getColumnIndex('id')),
      session_id: rs.getLong(rs.getColumnIndex('session_id')),
      turn_index: rs.getLong(rs.getColumnIndex('turn_index')),
      user_input: rs.getString(rs.getColumnIndex('user_input')),
      ai_response: rs.getString(rs.getColumnIndex('ai_response')),
      timestamp: rs.getString(rs.getColumnIndex('timestamp')),
    };
  }

  private rowToReview(rs: relationalStore.ResultSet): ReviewRecord {
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
}
""")

# ---- AuthService (class-based original) ----
write_file('service/AuthService.ets', """\
import { DatabaseHelper } from './DatabaseHelper';

export class AuthService {
  static async getUserName(context: Context): Promise<string> {
    const db = new DatabaseHelper(context);
    await db.init();
    const name = await db.getPreference('nickname');
    return name || '同学';
  }

  static async setUserName(context: Context, name: string): Promise<void> {
    const db = new DatabaseHelper(context);
    await db.init();
    await db.setPreference('nickname', name);
  }

  static async getUserId(context: Context): Promise<string> {
    const db = new DatabaseHelper(context);
    await db.init();
    let uid = await db.getPreference('user_id');
    if (!uid) {
      uid = 'user_' + Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
      await db.setPreference('user_id', uid);
    }
    return uid;
  }

  static async isLoggedIn(context: Context): Promise<boolean> {
    const name = await AuthService.getUserName(context);
    return name.length > 0;
  }
}
""")

# ---- AIService (class-based original + setBaseUrl + initFromPreferences) ----
write_file('service/AIService.ets', """\
import http from '@ohos.net.http';
import { API_CONFIG } from '../constants/AppConstants';
import { AIEvaluationResponse } from '../model/DataModel';
import { DatabaseHelper } from './DatabaseHelper';

export class AIService {
  static currentBaseUrl: string = API_CONFIG.BASE_URL;

  static async initFromPreferences(context: Context): Promise<void> {
    const db = new DatabaseHelper(context);
    await db.init();
    const saved = await db.getPreference('backend_url');
    if (saved) {
      AIService.currentBaseUrl = saved;
      API_CONFIG.BASE_URL = saved;
    }
  }

  static async getBaseUrl(context: Context): Promise<string> {
    const db = new DatabaseHelper(context);
    await db.init();
    const saved = await db.getPreference('backend_url');
    return saved || API_CONFIG.BASE_URL;
  }

  static async setBaseUrl(context: Context, url: string): Promise<void> {
    const db = new DatabaseHelper(context);
    await db.init();
    await db.setPreference('backend_url', url);
    AIService.currentBaseUrl = url;
    API_CONFIG.BASE_URL = url;
  }

  static async evaluateWithAI(question: string, userAnswer: string, step: string): Promise<AIEvaluationResponse> {
    const url = AIService.currentBaseUrl + API_CONFIG.ENDPOINTS.EVALUATE;
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

  static evaluateWithAIStream(onData: (chunk: string) => void, onDone: () => void, onError: (err: Error) => void): void {
    setTimeout(() => {
      onDone();
    }, 100);
  }
}
""")

# ---- SpacedRepetitionService (class-based original + loop fix) ----
write_file('service/SpacedRepetitionService.ets', """\
import { DatabaseHelper } from './DatabaseHelper';
import { ReviewRecord } from '../model/DataModel';

const MIN_INTERVAL = 1;
const MAX_INTERVAL = 365;
const EASE_FACTOR_MIN = 1.3;
const EASE_FACTOR_MAX = 3.5;
const EASE_FACTOR_INITIAL = 2.5;

export class SpacedRepetitionService {
  static calculateNextReview(score: number, currentEaseFactor: number, currentInterval: number, currentReviewCount: number): {
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

  static async processReviewResult(context: Context, kpId: number, score: number): Promise<void> {
    const normalizedScore = Math.round(score / 20);
    const db = new DatabaseHelper(context);
    await db.init();
    let review: ReviewRecord | null = null;
    try {
      review = await db.getReviewRecord(kpId);
    } catch (_) {
      review = null;
    }
    const easeFactor = review ? review.ease_factor : EASE_FACTOR_INITIAL;
    const intervalDays = review ? review.interval_days : 0;
    const reviewCount = review ? review.review_count : 0;
    const avgScore = review ? review.avg_score : 0;

    const result = SpacedRepetitionService.calculateNextReview(normalizedScore, easeFactor, intervalDays, reviewCount);
    const newAvgScore = reviewCount > 0 ? (avgScore * reviewCount + score) / (reviewCount + 1) : score;
    let newStatus = 'pending';
    if (score >= 80) {
      newStatus = 'mastered';
    } else if (normalizedScore < 3) {
      newStatus = 'overdue';
    }
    await db.saveReviewRecord(kpId, result.easeFactor, result.intervalDays, result.nextReviewDate, reviewCount + 1, newAvgScore, newStatus);
  }
}
""")

print('Part 6: DatabaseHelper, AuthService, AIService, SpacedRepetitionService reverted to class-based')
print('Run part 7 for ProfileTab.ets and remaining fixes')
