# Tasks: 优化AI评价提示词

## Tasks

### T1: 更新 PROMPT_TEMPLATES["what"] 提示词
- **File**: `backend/services/deepseek_client.py`
- **Action**: 替换"what"步骤的提示词模板，添加四个结构化评分维度（准确性0-30、完整性0-25、条理性0-20、理解深度0-25），要求feedback包含整体评价→各维度表现→改进建议，追问需深入概念某个方面。
- **Check**: 提示词是否包含四个维度的评分标准和权重

### T2: 更新 PROMPT_TEMPLATES["why"] 提示词
- **File**: `backend/services/deepseek_client.py`
- **Action**: 替换"why"步骤的提示词模板，添加四个结构化评分维度（因果逻辑0-30、原理阐述0-25、批判性思维0-25、关联能力0-20），要求feedback结构同上，追问需聚焦原理探讨。
- **Check**: 提示词是否包含四个维度的评分标准和权重

### T3: 更新 PROMPT_TEMPLATES["how"] 提示词
- **File**: `backend/services/deepseek_client.py`
- **Action**: 替换"how"步骤的提示词模板，添加四个结构化评分维度（场景识别0-25、方法掌握0-25、实践性0-25、创新性0-25），要求feedback结构同上，追问需聚焦应用拓展。
- **Check**: 提示词是否包含四个维度的评分标准和权重

### T4: 更新系统消息和温度参数
- **File**: `backend/services/deepseek_client.py`
- **Action**: 
  1. 将 system message 和 evaluate()、evaluate_stream() 中的 temperature 从 0.7 改为 0.8
  2. 更新 system message 中输出格式说明（保持JSON格式不变）
- **Check**: temperature 是否已改，JSON输出说明是否精确

### T5: 编译验证
- **Command**: 在 backend 目录下运行 Python 语法检查
- **Check**: 无语法错误
