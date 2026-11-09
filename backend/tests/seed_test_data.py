"""
为本地预览数据库注入测试数据，包含各种完成状态的课程和学习会话。

运行方式：
  python seed_test_data.py

会创建/覆盖以下位置的数据库：
  entry/.preview/default/intermediates/database/study_machine.db

如需指定其他路径：python seed_test_data.py --db-path <path>
"""

import sqlite3
import os
import argparse
from datetime import datetime, timedelta

SAMPLE_COURSES = [
    {
        "name": "Python 编程入门",
        "description": "学习 Python 编程语言的基础知识，包括变量、数据类型、控制流和函数",
        "knowledgePoints": [
            {"title": "变量与数据类型",
             "content": "Python 中的变量不需要声明类型，可以直接赋值。常见数据类型包括整数(int)、浮点数(float)、字符串(str)、布尔值(bool)、列表(list)、元组(tuple)、字典(dict)等。"},
            {"title": "条件语句与循环",
             "content": "条件语句使用 if/elif/else 进行分支判断。循环包括 for 循环（用于遍历可迭代对象）和 while 循环（条件满足时持续执行）。"},
            {"title": "函数定义与使用",
             "content": "函数使用 def 关键字定义。支持位置参数、默认参数、关键字参数和可变参数。"},
        ]
    },
    {
        "name": "数据结构与算法",
        "description": "掌握常用的数据结构和经典算法",
        "knowledgePoints": [
            {"title": "数组与链表",
             "content": "数组是连续内存空间上相同类型元素的集合。链表由节点组成，分为单链表、双链表和循环链表。"},
            {"title": "栈与队列",
             "content": "栈是后进先出(LIFO)的数据结构。队列是先进先出(FIFO)的数据结构。"},
            {"title": "二叉树与遍历",
             "content": "二叉树每个节点最多有两个子节点。遍历方式包括前序、中序、后序和层序遍历。"},
        ]
    },
    {
        "name": "操作系统原理",
        "description": "理解操作系统核心概念：进程管理、内存管理、文件系统和设备管理",
        "knowledgePoints": [
            {"title": "进程与线程",
             "content": "进程是资源分配的基本单位，线程是CPU调度的基本单位。进程间通信方式包括管道、消息队列、共享内存等。"},
            {"title": "内存管理",
             "content": "内存管理包括内存分配与回收、地址转换、内存保护和内存扩充。虚拟内存技术允许程序执行时只将部分内容装入内存。"},
            {"title": "文件系统",
             "content": "文件系统负责管理磁盘上的数据存储和检索。常见的文件系统有FAT32、NTFS、ext4等。"},
        ]
    },
    {
        "name": "计算机网络",
        "description": "学习计算机网络的基本概念、协议体系结构和网络应用",
        "knowledgePoints": [
            {"title": "TCP/IP 协议栈",
             "content": "TCP/IP 协议栈分为应用层、传输层、网络层和网络接口层。传输层有TCP（可靠）和UDP（快速）。"},
            {"title": "HTTP 协议",
             "content": "HTTP是超文本传输协议，基于请求-响应模型。主要方法有GET、POST、PUT和DELETE。"},
            {"title": "网络安全基础",
             "content": "网络安全包括机密性、完整性和可用性三大目标。"},
        ]
    },
    {
        "name": "数据库系统概论",
        "description": "掌握关系数据库的核心概念，SQL语言和数据库设计方法",
        "knowledgePoints": [
            {"title": "关系模型与SQL",
             "content": "关系模型使用二维表表示数据。SQL包括DDL、DML和DCL。基本操作有SELECT、INSERT、UPDATE、DELETE。"},
            {"title": "数据库设计",
             "content": "数据库设计遵循规范化理论：1NF、2NF、3NF。通过ER图进行概念设计，转换为关系模型。"},
            {"title": "事务与并发控制",
             "content": "事务具有ACID特性：原子性、一致性、隔离性和持久性。并发控制主要解决丢失修改、读脏数据和不可重复读问题。"},
        ]
    },
]


def create_tables(cursor):
    """创建与 DatabaseHelper.ets 相同的表结构"""
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            is_sample INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS knowledge_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS learning_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            knowledge_point_id INTEGER NOT NULL,
            step TEXT NOT NULL,
            status TEXT DEFAULT 'in_progress',
            started_at TEXT DEFAULT (datetime('now','localtime')),
            completed_at TEXT,
            score REAL DEFAULT 0,
            FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS dialogue_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            turn_index INTEGER DEFAULT 0,
            user_input TEXT,
            ai_response TEXT,
            timestamp TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (session_id) REFERENCES learning_sessions(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS review_records (
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
        );
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    """)


def seed_data(cursor):
    now = datetime.now()

    # ─── 课程 ID 映射 ───
    inserted_course_ids = []

    for course_data in SAMPLE_COURSES:
        cursor.execute(
            "INSERT INTO courses (name, description, is_sample) VALUES (?, ?, 1)",
            (course_data["name"], course_data["description"]),
        )
        course_id = cursor.lastrowid
        inserted_course_ids.append(course_id)

        # 插入知识点并记录 ID
        kp_ids = []
        for kp in course_data["knowledgePoints"]:
            cursor.execute(
                "INSERT INTO knowledge_points (course_id, title, content) VALUES (?, ?, ?)",
                (course_id, kp["title"], kp["content"]),
            )
            kp_ids.append(cursor.lastrowid)

        # ─── 为不同课程注入不同状态的学习会话 ───
        course_index = len(inserted_course_ids) - 1

        # 课程 1（Python）：第一个知识点全部完成，第二个部分完成，第三个未开始
        if course_index == 0:
            _complete_kp(cursor, kp_ids[0], now, scores=[85, 78, 90])
            _complete_kp(cursor, kp_ids[1], now, scores=[65, None, None])
            # kp_ids[2] — 不创建任何会话 → 未开始

        # 课程 2（数据结构）：全部完成
        elif course_index == 1:
            for kid in kp_ids:
                _complete_kp(cursor, kid, now, scores=[92, 88, 85])

        # 课程 3（操作系统）：部分完成 + 进行中
        elif course_index == 2:
            _complete_kp(cursor, kp_ids[0], now, scores=[70, 65, 80])
            _complete_kp(cursor, kp_ids[1], now, scores=[55, None, None])
            _inprogress_kp(cursor, kp_ids[2], now, steps=["what", "why"])

        # 课程 4（计网）：全是进行中
        elif course_index == 3:
            for kid in kp_ids:
                _inprogress_kp(cursor, kid, now, steps=["what"])

        # 课程 5（数据库）：全部未开始 — 不创建任何会话

    # 插入偏好设置（模拟已登录）
    cursor.execute(
        "INSERT OR REPLACE INTO preferences (key, value) VALUES ('nickname', '测试用户')"
    )


def _complete_kp(cursor, kp_id, now, scores):
    """为一个知识点的三个步骤创建已完成会话"""
    steps = ["what", "why", "how"]
    for i, step in enumerate(steps):
        score = scores[i] if i < len(scores) and scores[i] is not None else 0
        if score == 0:
            continue
        started = now - timedelta(days=len(steps) - i, hours=2)
        completed = started + timedelta(minutes=30)
        cursor.execute(
            """INSERT INTO learning_sessions
               (knowledge_point_id, step, status, started_at, completed_at, score)
               VALUES (?, ?, 'completed', ?, ?, ?)""",
            (kp_id, step, started.strftime("%Y-%m-%d %H:%M:%S"),
             completed.strftime("%Y-%m-%d %H:%M:%S"), score),
        )
        session_id = cursor.lastrowid

        # 添加一些对话记录
        _add_sample_dialogue(cursor, session_id, step, score)

        # 添加复习记录
        cursor.execute(
            """INSERT INTO review_records
               (knowledge_point_id, ease_factor, interval_days, next_review_date, last_reviewed_at,
                review_count, avg_score, status)
               VALUES (?, 2.5, 3, ?, ?, 1, ?, 'pending')""",
            (kp_id,
             (now + timedelta(days=3)).strftime("%Y-%m-%d"),
             completed.strftime("%Y-%m-%d %H:%M:%S"),
             float(score)),
        )


def _inprogress_kp(cursor, kp_id, now, steps):
    """为一个知识点的指定步骤创建进行中会话"""
    for step in steps:
        started = now - timedelta(hours=1)
        cursor.execute(
            """INSERT INTO learning_sessions
               (knowledge_point_id, step, status, started_at, score)
               VALUES (?, ?, 'in_progress', ?, 0)""",
            (kp_id, step, started.strftime("%Y-%m-%d %H:%M:%S")),
        )
        session_id = cursor.lastrowid
        _add_sample_dialogue(cursor, session_id, step, 0)


def _add_sample_dialogue(cursor, session_id, step, score):
    sample_qas = {
        "what": [
            ("这个概念的定义是什么？", "这个概念是指...它的核心定义包括三个方面..."),
            ("能不能举个例子说明？", "当然可以。比如在实际情况中..."),
            ("那么它的主要特点是什么？", "主要特点包括：1. ... 2. ... 3. ..."),
        ],
        "why": [
            ("为什么要学习这个知识点？", "理解这个知识点对后续学习至关重要，因为..."),
            ("它的原理是什么？", "其原理基于...的核心思想，具体来说..."),
            ("有没有实际应用场景？", "在实际应用中，它被广泛用于..."),
        ],
        "how": [
            ("如何在实际中使用？", "使用步骤如下：第一...第二...第三..."),
            ("有什么注意事项吗？", "使用时需要注意以下几点：..."),
        ],
    }
    dialogues = sample_qas.get(step, [])
    for idx, (user_q, ai_a) in enumerate(dialogues):
        cursor.execute(
            """INSERT INTO dialogue_records (session_id, turn_index, user_input, ai_response)
               VALUES (?, ?, ?, ?)""",
            (session_id, idx + 1, user_q, ai_a),
        )


def main():
    parser = argparse.ArgumentParser(description="为预览数据库注入测试数据")
    parser.add_argument(
        "--db-path",
        default=None,
        help="数据库文件路径（默认自动检测预览路径）",
    )
    args = parser.parse_args()

    if args.db_path:
        db_paths = [args.db_path]
    else:
        base = r"entry\.preview\default\intermediates\database"
        db_paths = [
            os.path.join(os.getcwd(), base, "study_machine.db"),
            os.path.join(os.getcwd(), "..", base, "study_machine.db"),
        ]

    db_path = None
    for p in db_paths:
        if os.path.exists(os.path.dirname(p)) or not args.db_path:
            parent = os.path.dirname(p)
            if os.path.exists(parent):
                db_path = p
                break

    if not db_path:
        # 使用当前目录
        db_path = "study_machine_preview.db"
        print(f"[INFO] 未找到预览目录，将在当前目录创建: {db_path}")

    print(f"目标数据库: {db_path}")

    # 确保目录存在
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    # 删除旧库（重新创建完整示例数据）
    if os.path.exists(db_path):
        os.remove(db_path)
        print("已删除旧数据库")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    print("创建表结构...")
    create_tables(cursor)

    print("注入测试数据...")
    seed_data(cursor)

    conn.commit()

    # 验证
    cursor.execute("SELECT COUNT(*) FROM courses")
    course_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM knowledge_points")
    kp_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM learning_sessions")
    session_count = cursor.fetchone()[0]
    cursor.execute("SELECT status, COUNT(*) FROM learning_sessions GROUP BY status")
    status_counts = cursor.fetchall()

    print(f"\n数据注入完成!")
    print(f"  课程数: {course_count}")
    print(f"  知识点数: {kp_count}")
    print(f"  学习会话数: {session_count}")
    for status, count in status_counts:
        print(f"    - {status}: {count}")

    conn.close()
    print(f"\n请将数据库文件复制到模拟器的对应路径: {db_path}")
    print(f"或运行: python check_database_data.py")


if __name__ == "__main__":
    main()
