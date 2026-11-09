## Why

当前应用启动时只有简单的文字和加载动画，缺乏品牌视觉呈现。添加品牌启动页可以提升用户体验，在后台预加载数据的同时展示应用品牌形象。

## What Changes

- 将 `Index.ets` 改造为视觉完整的启动页（Splash Screen），展示品牌Logo和名称
- 启动页在后台预加载数据库、示例课程、引导状态等必要数据
- 预加载完成后自动跳转到首页或引导页
- 添加启动页渐显动画效果

## Capabilities

### New Capabilities
- `splash-screen`: 应用启动页，包含品牌Logo展示、加载状态提示、数据预加载能力

### Modified Capabilities
- （无，当前无已存在的spec）

## Impact

- `entry/src/main/ets/pages/Index.ets`: 改造为完整启动页
- `entry/src/main/resources/base/media/foreground.png`: 已替换为品牌Logo
