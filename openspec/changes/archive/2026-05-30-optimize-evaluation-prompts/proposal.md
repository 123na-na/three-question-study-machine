## Why

当前AI评价提示词仅粗略要求"准确性、完整性、深度"，缺乏结构化评分标准，导致AI反馈不够细致、评分不够精准，学生学习指导价值有限。

## What Changes

- 优化三个学习步骤（是什么/为什么/怎么用）的AI评价提示词，添加结构化评分维度和详细标准
- 提高温度参数以增加反馈多样性
- 增加对回答长度的最低要求提示

## Capabilities

### New Capabilities
- `evaluation-prompt`: AI评价提示词优化，包含结构化评分维度和详细评价标准

### Modified Capabilities
- （无）

## Impact

- `backend/services/deepseek_client.py`: 更新 PROMPT_TEMPLATES 中的三个提示词模板
