# HarmonyOS 模拟器日志错误参考

> 本文件记录模拟器运行时出现的系统级警告/错误，供开发参考。
> **这些日志不影响应用功能，属于模拟器环境正常现象。**

---

## 一、完全可忽略（系统级，无需处理）

### 1. 沙箱与安全类
```
[sandbox_dec.c:179]open dec file fail.
[ArkCompiler] Can not open xpm proc file, do not check secure memory anymore.
[ffrt] load so[lib_cpuboost.so] fail
```
**原因**: 模拟器环境缺少安全相关文件/库（解密文件、XPM内存保护、CPU加速库）。

### 2. 调度与性能类
```
[CONCUR] apply qos failed, errno = 4  (出现约11次)
[ueaClient-RmeCoreSched] [Init]: do not enabled! ret: -1
```
**原因**: 模拟器的 QoS 调度服务和 RME 资源调度引擎未启用或不支持。

### 3. Ace/ArkUI 框架类
```
[Ace] ConfigXMLParserBase read system file failed (×2)
[Ace] ERROR EACCES (×2)
[AceUIEvent] AceTransform load failed: Error loading shared library ... libtransform_interaction_ext.z.so
```
**原因**: Ace 框架尝试读取系统配置文件或加载 UI 扩展库，模拟器中这些资源不存在或无权限访问。

### 4. 参数订阅服务类
```
[PARAM_WATCHER] Read result failed, code is: 1/3/5 (×8次)
[PARAM_WATCHER] Failed to add watcher for persist.rosen.animationtrace.enabled (×2次)
[PARAM_WATCHER] Failed to add callback for sys.graphic.openTestModeTrace
[BEGET] WatchParameter failed! errNum is -1 / 110
[IMockSessionManager] Read result failed, code is: 3 / 5
```
**原因**: 系统参数订阅服务在应用启动时尚未就绪，或动画追踪/测试模式参数在模拟器不支持。

### 5. 其他系统服务
```
[WMS] SetWindowType: permission denied!
[WMSAttribute] UpdateConfigurationSyncForAll: root is null (×2)
[WMS] GetSingleton: cant get OHOS::Rosen::WindowInfoReporter
[UIAbility] hasSaveData_: false
[accessibility_asacfwk] accessibility service is ready.
[ResourceManager] LoadThemesRes failed, userId = 100
[CompatPolicyDeviceType] deviceType is empty.
```
**原因**: 各系统服务（窗口管理器、资源管理器、兼容性策略等）在模拟器中的初始化行为。

---

## 二、已处理的优化项

### deviceTypes 配置增强
- **原始**: 仅 `"phone"`
- **修改为**: `["phone", "tablet"]`
- **位置**: `entry/src/main/module.json5`
- **目的**: 部分模拟器可能以 tablet 设备类型上报，添加后减少 `deviceType is empty` 警告

---

## 三、判断标准

出现以上日志时，按以下标准判断是否需要处理：

| 判断条件 | 处理方式 |
|---------|---------|
| 来源包含 `com.examp..._machine` 且标签为 `E` | 检查是否为本应用代码抛出 |
| 来源为 `apppool` 或系统服务名 | 忽略，属系统级 |
| 应用功能正常运行 | 忽略，仅 IDE 日志过滤噪音 |
| 应用崩溃或功能异常 | 根据具体堆栈定位 |

---

## 四、IDE 日志过滤建议

在 DevEco Studio 的 Log 面板中，建议设置过滤条件：
- **Tag 过滤**: 输入应用包名或自定义 tag
- **Level 选择**: 选择 `Warn` 以上级别，屏蔽大量系统 Info 日志
- **进程过滤**: 只选择应用进程，过滤 apppool/system 进程
