# 开发问题修复总结

> 日期: 2026-05-30
> 项目: 三问高效学习机（问枢）

---

## 1. Mock 评分虚高

**症状**: 随便回答也得 70-99 分。

**根因**: `LearningSessionPage.ets:103` — 后端不可达时走 mock，评分逻辑为 `Math.random()*30 + 70`，导致任何输入都得到高分。

**修复**: 改为基于输入长度分档评分（25-74 分封顶），feedback 明确标注"离线模拟评价"。

```
// 旧代码
score = Math.floor(Math.random() * 30) + 70;

// 新代码：按长度分档
len < 30  → 25-34
len < 50  → 35-44
len < 80  → 45-54
len < 120 → 50-64
≥ 120     → 55-74 (max 74)
```

**文件**: `entry/src/main/ets/pages/LearningSessionPage.ets`

---

## 2. 学习完成后不显示"已完成"

**症状**: 学完知识点返回课程页，仍显示"开始学习"，无完成标记。

**根因**: 
- `CourseDetailPage` 没有 `onPageShow` 生命周期刷新
- `KnowledgePointCard` 无完成状态展示逻辑

**修复**:
- 新增 `onPageShow()` 生命周期 + `refreshCompletionStatus()` 方法
- 新增 `@State completedKpIds` 跟踪完成状态
- `KnowledgePointCard` 新增 `@Prop isCompleted`，完成后标题变绿、显示 `✓ 已完成`、按钮变 `已学习 ✓`

**文件**: `entry/src/main/ets/pages/CourseDetailPage.ets`

---

## 3. 近30天活动图无时间轴

**症状**: 柱状图底部没有日期标签，用户不知道哪天有活动。

**根因**: `buildActivityData` 只存 `day`/`count`，无日期信息。

**修复**:
- 创建 `ActivityDay` 接口（`day`、`count`、`dateLabel`）
- 每项存储 `dateLabel`（M/D 格式，如 `5/1`）
- 渲染时在首、末、每7天处显示日期标签
- 图表高度从 100 增至 120

**文件**: `entry/src/main/ets/pages/ProgressDashboardPage.ets`

---

## 4. 进入知识点直接跳到第二步

**症状**: 点进知识点直接显示"第2步：为什么"，用户疑惑。

**根因**: `checkPreviousSession()` 检测到第1步 session 为 `completed` 就静默跳转，无任何提示。

**修复**:
- 新增 `ResumeDialog` 弹窗，让用户选择"继续上次"或"重新学习"
- 新增 `resetAndRestart()` 方法清理旧 session
- 新增 `DatabaseHelper.deleteSession()` 删除 session 及关联对话记录

**文件**: `entry/src/main/ets/pages/LearningSessionPage.ets`

---

## 5. 编译报错——对象字面量类型

**症状**: 三个 ArkTS 编译错误：
- `arkts-no-obj-literals-as-types` — 对象字面量不能做类型声明
- `arkts-no-untyped-obj-literals` — 对象字面量必须对应显式声明的类或接口
- `arkts-no-noninferrable-arr-literals` — 数组字面量必须包含可推断类型的元素

**根因**: ArkTS 严格模式下不允许内联对象字面量作为类型，必须提取为命名的 interface。

**修复**: 提取接口：
- `AchievementCheck`（替代 `{ id: string; condition: boolean }`）
- `ShareAchievementInfo`、`ShareCertificateInfo`（替代内联参数类型）
- `ActivityDay`（替代 `Record<string, number>`）

**文件**: 
- `entry/src/main/ets/service/AchievementService.ets`
- `entry/src/main/ets/utils/ShareUtil.ets`
- `entry/src/main/ets/pages/ProgressDashboardPage.ets`

---

## 6. 编译报错——startAbility 不在 Context 上

**症状**: `Property 'startAbility' does not exist on type 'Context'`

**根因**: 新版本 HarmonyOS 中 `startAbility` 属于 `UIAbilityContext`，不在基础 `Context` 上。

**修复**: 导入并使用 `common.UIAbilityContext` 进行类型转换：

```typescript
import { common } from '@kit.AbilityKit';
const uiContext: common.UIAbilityContext = context as common.UIAbilityContext;
await uiContext.startAbility({...});
```

**文件**: `entry/src/main/ets/utils/ShareUtil.ets`

---

## 7. 编译报错——justifyContent 不在 FlexAttribute 上

**症状**: `Property 'justifyContent' does not exist on type 'FlexAttribute'`

**根因**: ArkUI 新版中 `Flex` 组件的属性不支持链式调用 `.justifyContent()`。

**修复**: 改为构造函数传参：

```typescript
// 旧
Flex() { ... }
  .justifyContent(FlexAlign.Start)

// 新
Flex({ justifyContent: FlexAlign.Start, wrap: FlexWrap.Wrap }) { ... }
```

**文件**: `entry/src/main/ets/pages/ProgressDashboardPage.ets`

---

## 通用经验

| 类别 | 要点 |
|------|------|
| **ArkTS 类型** | 永远不要用内联对象字面量做类型，提前定义 interface |
| **ArkUI 组件** | 容器属性（justifyContent, alignItems 等）用构造函数传参，不链式调用 |
| **生命周期** | 页面返回刷新用 `onPageShow()`，不是 `aboutToAppear()` |
| **Context 类型** | 高级 Context 操作（startAbility）要用 `common.UIAbilityContext` |
| **Mock 数据** | 永远不要给随机高分，Mock 应当标记清楚并给保守分数 |
| **用户提示** | 静默跳转比错误更糟糕 — 任何状态变更都要给用户明确的视觉反馈 |
