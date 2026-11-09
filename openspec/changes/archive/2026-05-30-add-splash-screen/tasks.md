## 1. 改造启动页面

- [x] 1.1 在 Index.ets 加载视图中添加品牌 Logo 图片组件（Image）
- [x] 1.2 保留应用名称"问枢"和标语"是什么 → 为什么 → 怎么用"
- [x] 1.3 保留 LoadingProgress 加载动画和"正在初始化..."文字
- [x] 1.4 保留错误状态视图（错误信息 + 重试按钮）
- [x] 1.5 保留引导页 overlay 逻辑

## 2. 数据预加载

- [x] 2.1 保留数据库初始化逻辑（DatabaseHelper.init）
- [x] 2.2 保留示例课程加载逻辑（SampleCourseLoader.loadSampleCoursesIfNeeded）
- [x] 2.3 保留引导状态检查逻辑（hasCompletedOnboarding）
- [x] 2.4 保留引导完成后跳转到首页的逻辑

## 3. 验证

- [x] 3.1 确认编译通过无错误
- [x] 3.2 确认启动页展示品牌 Logo
- [x] 3.3 确认预加载完成后正确跳转
- [x] 3.4 确认错误状态显示和重试可用
