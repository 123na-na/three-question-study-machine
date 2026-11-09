# 知识点不显示问题排查指南

## 问题描述
用户在课程详情页点击"学习"标签时，显示"暂无知识点"，无法进入课程进行学习。

## 已完成的修复

### 1. 增强日志输出
已在以下文件中添加详细的日志输出：
- **CourseDetailPage.ets**: 记录课程和知识点加载过程
- **SampleCourseLoader.ets**: 记录样本课程加载过程
- **DatabaseHelper.ets**: 记录数据库初始化和数据操作
- **LoginPage.ets**: 记录登录和初始化流程

### 2. 改进错误处理
所有数据库操作都增加了详细的错误处理和日志记录。

## 诊断步骤

### 步骤1: 运行诊断脚本
```bash
cd backend/tests
python check_database_data.py
```
这将显示数据库中是否有课程和知识点数据。

### 步骤2: 检查日志输出
在DevEco Studio中查看日志，关注以下关键信息：

1. **登录阶段**:
   ```
   [LoginPage] Starting learning with nickname: xxx
   [LoginPage] Loading sample courses...
   [SampleCourseLoader] Checking if sample courses need to be loaded...
   [SampleCourseLoader] Current course count: X
   ```

2. **数据库初始化**:
   ```
   [DatabaseHelper] Initializing database tables...
   [DatabaseHelper] Creating table 1/6
   ...
   [DatabaseHelper] Database tables initialized successfully
   ```

3. **课程加载**:
   ```
   [SampleCourseLoader] Loading course: Python 编程入门
   [DatabaseHelper] Adding course: Python 编程入门
   [DatabaseHelper] Course added with id: 1
   [DatabaseHelper] Adding knowledge point: 变量与数据类型
   [DatabaseHelper] KP added with id: 1
   ```

4. **课程详情页**:
   ```
   [CourseDetailPage] Loading course with id: 1
   [CourseDetailPage] Course loaded: "Python 编程入门" id=1
   [CourseDetailPage] Knowledge points loaded: 3
   [CourseDetailPage] First KP: {"id":1,"course_id":1,"title":"变量与数据类型",...}
   ```

### 步骤3: 常见问题和解决方案

#### 问题1: 课程数量为0
**症状**: `[SampleCourseLoader] Current course count: 0`
**解决方案**: 
- 检查数据库是否正确初始化
- 确认SampleCourseLoader中的课程数据是否正确
- 重新登录应用

#### 问题2: 知识点数量为0
**症状**: `[CourseDetailPage] Knowledge points loaded: 0`
**解决方案**:
- 检查对应的课程ID是否正确
- 确认addKnowledgePoint是否成功执行
- 检查数据库外键约束

#### 问题3: 数据库初始化失败
**症状**: `[DatabaseHelper] Failed to create table: ...`
**解决方案**:
- 检查应用权限
- 清除应用数据后重新安装
- 检查数据库文件路径

## 快速修复方法

### 方法1: 重新初始化应用
1. 卸载应用
2. 重新安装并登录
3. 观察日志输出

### 方法2: 手动清除数据
1. 在设备设置中找到应用
2. 清除应用数据
3. 重新打开应用并登录

### 方法3: 检查模拟器存储
如果是模拟器问题，可能需要：
1. 重启模拟器
2. 清理模拟器缓存
3. 重新部署应用

## 验证修复

修复后应该看到：
1. 登录页面成功加载样本课程
2. 首页显示5门课程
3. 点击课程进入详情页
4. 课程详情页显示知识点列表
5. 点击知识点可以开始学习

## 联系支持
如果问题仍然存在，请提供：
1. 完整的日志输出
2. 诊断脚本的输出结果
3. 设备和系统版本信息
