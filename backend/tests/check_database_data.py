"""
检查数据库中的课程和知识点数据
"""

import sqlite3
import os

# 查找数据库文件路径
db_paths = [
    "entry/.preview/default/intermediates/database/study_machine.db",
    "entry/build/default/intermediates/database/study_machine.db",
]

def check_database():
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("数据库文件未找到，请检查以下路径:")
        for path in db_paths:
            print(f"  - {path}")
        return
    
    print(f"找到数据库文件: {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("数据库表:")
    for table in tables:
        print(f"  - {table[0]}")
    print()
    
    # 检查课程数据
    try:
        cursor.execute("SELECT id, name, description, is_sample FROM courses")
        courses = cursor.fetchall()
        print(f"课程数量: {len(courses)}")
        for course in courses:
            print(f"  ID: {course[0]}, 名称: {course[1]}, 示例课程: {course[3]}")
        print()
    except sqlite3.OperationalError as e:
        print(f"查询courses表失败: {e}\n")
    
    # 检查知识点数据
    try:
        cursor.execute("SELECT id, course_id, title FROM knowledge_points")
        kps = cursor.fetchall()
        print(f"知识点数量: {len(kps)}")
        for kp in kps:
            print(f"  ID: {kp[0]}, 课程ID: {kp[1]}, 标题: {kp[2]}")
        print()
    except sqlite3.OperationalError as e:
        print(f"查询knowledge_points表失败: {e}\n")
    
    # 检查学习会话数据
    try:
        cursor.execute("SELECT id, knowledge_point_id, step, status, score FROM learning_sessions")
        sessions = cursor.fetchall()
        print(f"学习会话数量: {len(sessions)}")
        for session in sessions:
            print(f"  ID: {session[0]}, 知识点ID: {session[1]}, 步骤: {session[2]}, 状态: {session[3]}, 分数: {session[4]}")
        print()
    except sqlite3.OperationalError as e:
        print(f"查询learning_sessions表失败: {e}\n")
    
    conn.close()

if __name__ == "__main__":
    check_database()
