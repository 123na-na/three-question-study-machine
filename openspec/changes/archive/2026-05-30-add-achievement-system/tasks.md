## 1. 数据层：新增接口与数据库

- [x] 1.1 在 DataModel.ets 新增 Achievement 和 Certificate 接口
- [x] 1.2 数据存储已完成（使用 preferences JSON 存储成就和证书数据）

## 2. 核心服务

- [x] 2.1 创建 AchievementService.ets — 成就检测、发放、查询逻辑（含证书管理）
- [x] 2.2 创建 ShareUtil.ets — 系统分享面板工具函数

## 3. UI 集成

- [x] 3.1 修改 ProgressDashboardPage.ets — 添加成就展示区域和分享入口
- [x] 3.2 修改 LearningReportPage.ets — 集成证书和分享入口

## 4. 验证

- [x] 4.1 编译通过无错误
- [x] 4.2 功能验证：成就触发、证书生成、分享可用
