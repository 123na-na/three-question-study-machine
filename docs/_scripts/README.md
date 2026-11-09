# 开发期临时脚本（归档）

这里放的是开发过程中用过的一次性脚本，原位置在 `backend/tests/`，2026-11 整理仓库时只移动、没有删除，保留排查过程可追溯。

## 这批脚本是什么

- `fix_*.py`（12 个）：修 ArkTS 编译错误、编码问题、SQL 拼接、重复定义等，多数是"改完就退场"的补丁
- `check_*.py`（5 个）：查数据库内容、编码、首页渲染是否正常
- `restore_files_p1.py` ~ `restore_files_p8.py`（8 个）：分片还原被批量改写过的页面文件
- `rewrite_session_page.py`、`simulate_data_loading.py`、`find_tabitems.py`、`inspect_corruption.py`：单次用的重写与定位脚本

## 注意

这些都是历史记录，不是可复用的测试。个别脚本用相对路径读写文件，移位置后按原样可能跑不起来——需要复用时把它们拷回 `backend/tests/` 再执行。

## 真正的测试还在原处

`backend/tests/` 只保留了 4 项：

- `test_core_logic.py`：核心逻辑单元测试
- `validate_sample_courses.py`：示例课程数据校验
- `seed_test_data.py` + `study_machine_preview.db`：测试数据与配套 SQLite 库（两者互相依赖，因此没有移走）
