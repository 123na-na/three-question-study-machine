"""
模拟数据加载流程，检查SampleCourseLoader逻辑
"""

import json

# 模拟SampleCourseLoader中的课程数据
SAMPLE_COURSES = [
  {
    "name": "Python 编程入门",
    "description": "学习 Python 编程语言的基础知识，包括变量、数据类型、控制流和函数",
    "knowledgePoints": [
      { "title": "变量与数据类型", "content": "Python 中的变量不需要声明类型..." },
      { "title": "条件语句与循环", "content": "条件语句使用 if/elif/else..." },
      { "title": "函数定义与使用", "content": "函数使用 def 关键字定义..." },
    ]
  },
  {
    "name": "数据结构与算法",
    "description": "掌握常用的数据结构和经典算法",
    "knowledgePoints": [
      { "title": "数组与链表", "content": "数组是连续内存空间..." },
      { "title": "栈与队列", "content": "栈是后进先出(LIFO)..." },
      { "title": "二叉树与遍历", "content": "二叉树每个节点最多有两个子节点..." },
    ]
  },
]

def simulate_data_loading():
    print("=== 模拟数据加载流程 ===\n")
    
    # 模拟课程加载
    for i, course in enumerate(SAMPLE_COURSES, 1):
        print(f"步骤 {i}: 加载课程 '{course['name']}'")
        print(f"  - 描述: {course['description']}")
        print(f"  - 知识点数量: {len(course['knowledgePoints'])}")
        
        # 模拟知识点加载
        for j, kp in enumerate(course['knowledgePoints'], 1):
            print(f"    知识点 {j}: {kp['title']}")
        
        print()
    
    # 总结
    total_courses = len(SAMPLE_COURSES)
    total_kps = sum(len(course['knowledgePoints']) for course in SAMPLE_COURSES)
    
    print("=== 数据加载总结 ===")
    print(f"总课程数: {total_courses}")
    print(f"总知识点数: {total_kps}")
    print(f"平均每课程知识点数: {total_kps / total_courses:.1f}")
    
    return total_courses, total_kps

def check_data_integrity():
    print("\n=== 数据完整性检查 ===\n")
    
    issues = []
    
    for i, course in enumerate(SAMPLE_COURSES, 1):
        # 检查课程名称
        if not course['name'] or len(course['name'].strip()) == 0:
            issues.append(f"课程 {i} 名称为空")
        
        # 检查知识点
        if len(course['knowledgePoints']) == 0:
            issues.append(f"课程 {i} 没有知识点")
        
        for j, kp in enumerate(course['knowledgePoints'], 1):
            if not kp['title'] or len(kp['title'].strip()) == 0:
                issues.append(f"课程 {i} 的知识点 {j} 标题为空")
            if not kp['content'] or len(kp['content'].strip()) == 0:
                issues.append(f"课程 {i} 的知识点 {j} 内容为空")
    
    if issues:
        print("发现以下问题:")
        for issue in issues:
            print(f"  ❌ {issue}")
    else:
        print("✅ 数据完整性检查通过")
    
    return len(issues) == 0

if __name__ == "__main__":
    courses, kps = simulate_data_loading()
    is_valid = check_data_integrity()
    
    print(f"\n{'='*50}")
    print(f"模拟完成: {courses} 门课程, {kps} 个知识点")
    print(f"数据有效性: {'✅ 通过' if is_valid else '❌ 失败'}")
    print(f"{'='*50}")
