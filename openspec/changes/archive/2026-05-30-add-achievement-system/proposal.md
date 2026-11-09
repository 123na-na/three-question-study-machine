## Why

学习成就感是持续学习的重要动力。当前应用缺少成就系统，用户完成学习后只能看到分数，缺乏正向激励和可分享的成果展示。

## What Changes

- 新增成就（勋章）系统：学习连续天数、知识点掌握等级、课程完成度等成就
- 新增证书系统：完成课程所有知识点后生成学习证书
- 新增分享功能：将成就、证书或学习报告分享到社交平台
- 在进度看板和报告页展示成就

## Capabilities

### New Capabilities
- `achievement-system`: 勋章/成就系统，包含多种成就类型和追踪逻辑
- `certificate`: 学习证书生成与展示
- `share`: 分享功能，支持分享成就、证书、学习报告到社交平台

### Modified Capabilities
- （无）

## Impact

- 新增 `entry/src/main/ets/service/AchievementService.ets` — 成就逻辑
- 新增 `entry/src/main/ets/utils/ShareUtil.ets` — 分享工具
- 修改 `entry/src/main/ets/service/DatabaseHelper.ets` — 新增成就/证书表
- 修改 `entry/src/main/ets/model/DataModel.ets` — 新增接口定义
- 修改 `entry/src/main/ets/pages/ProgressDashboardPage.ets` — 集成成就展示
- 修改 `entry/src/main/ets/pages/LearningReportPage.ets` — 集成证书与分享
