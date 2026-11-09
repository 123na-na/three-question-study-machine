# 三问学习机（Three-Question Study Machine）

鸿蒙（HarmonyOS）答题学习 App，采用**三问学习法**（What / Why / How）帮助用户深度学习知识点，并配套 **FastAPI + DeepSeek** 的 AI 评价中间层，支持实时流式评价。

## 功能

- **课程学习**：内置示例课程，分知识点学习，三问引导（是什么 / 为什么 / 怎么做）
- **AI 三问评价**：用户作答后由 DeepSeek 打分并给出中文反馈与追问（`/api/v1/evaluate`）
- **流式输出**：评价结果通过 SSE 实时流式返回（`/api/v1/evaluate/stream`）
- **复习与间隔重复**：SpacedRepetitionService 安排复习计划，强化记忆
- **学习报告与进度看板**：统计答题情况、分数曲线、成就系统
- **知识点搜索**：`/api/v1/search` 由 AI 生成相关知识点
- **登录与本地存储**：AuthService + 本地关系型数据库（RelationalStore）

## 运行截图与演示

| 首页（探索） | 三问学习（是什么/为什么/怎么用） |
| --- | --- |
| ![首页](./assets/01_home.png) | ![三问学习](./assets/04_three_questions.png) |
| **AI 评价结果（打分 + 反馈 + 追问）** | **课程详情（知识点）** |
| ![AI 评价](./assets/05_ai_evaluation.png) | ![课程详情](./assets/03_course_detail.png) |

**AI 评价完整过程录屏**（提交答案 → AI 评价 → 85 分 + 中文反馈 + 追问，14 秒）：

![AI 评价演示](./assets/ai_evaluation_demo.mp4)

> 更多截图见 [`assets/`](./assets)：我的课程、个人中心。

## 技术栈

| 端 | 技术 |
| --- | --- |
| 前端 | HarmonyOS ArkTS（ets）、DevEco Studio |
| 后端 | Python FastAPI、sse-starlette（SSE 流式）、httpx |
| AI | DeepSeek `deepseek-chat`（OpenAI 兼容接口） |
| 部署 | Docker、Docker Compose |

## 目录结构

```
three_question_study_machine/
├── entry/                 # HarmonyOS 应用模块（ArkTS）
│   └── src/main/ets/
│       ├── pages/         # 首页、登录、课程详情、学习会话、复习、报告、进度
│       ├── service/       # AIService / AuthService / 评分 / 间隔重复 / 成就
│       └── component/     # LearnTab / ReviewTab / StatsTab 等
├── assets/                # 运行截图 + AI 评价演示视频
└── backend/               # FastAPI 中间层
    ├── main.py            # 接口入口（evaluate / evaluate/stream / search / health）
    ├── services/deepseek_client.py
    ├── requirements.txt
    ├── .env.example
    ├── Dockerfile
    ├── .dockerignore
    ├── docker-compose.yml
    └── verify-docker.ps1   # 装好 Docker 后一键验证
```

## 启动方式

### 后端（FastAPI 中间层）

```bash
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt      # Windows
# .venv/bin/pip install -r requirements.txt        # macOS/Linux

cp .env.example .env     # 填入 DEEPSEEK_API_KEY
.venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8000
```

健康检查：`http://localhost:8000/api/v1/health`

### Docker 部署

```bash
cd backend
cp .env.example .env     # 填入 DEEPSEEK_API_KEY
docker compose up -d --build
```

**验证状态（已在本机实测通过）**

- 已安装 Docker Desktop（v29.9.2，WSL2 后端），执行 `docker compose up -d --build` 成功构建镜像并启动容器；
- 容器状态 `Up (healthy)`，端口映射 `0.0.0.0:8000->8000`，访问 `/api/v1/health` 返回 `healthy`；
- 容器内 `/api/v1/evaluate` 实测返回真实 AI 评价（打分 + 中文反馈，DeepSeek Key 通过 `.env` 注入），证明容器内应用与模型调用均正常。

> 复现命令（也可直接运行一键脚本 `powershell -ExecutionPolicy Bypass -File .\verify-docker.ps1`）：
>
> ```bash
> docker compose up -d --build
> curl http://localhost:8000/api/v1/health
> ```

> 部署结论：已通过 Docker Compose 完成 FastAPI 后端容器化，健康检查与容器内 AI 评价接口均实测可用。

### 前端（HarmonyOS）

1. 使用 DevEco Studio 打开 `three_question_study_machine` 根目录；
2. 同步构建 `entry` 模块，编译安装到模拟器/真机；
3. 在 `service/AIService.ets` 中配置后端地址（默认 `http://localhost:8000`）。

## 环境变量（backend/.env）

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `DEEPSEEK_API_KEY` | DeepSeek API Key（必填） | - |
| `DEEPSEEK_BASE_URL` | 接口地址 | `https://api.deepseek.com` |
| `DEEPSEEK_MODEL` | 模型名 | `deepseek-chat` |
| `PORT` | 服务端口 | `8000` |
| `CORS_ORIGINS` | 允许跨域来源 | `*` |

## 模型 Key 申请

DeepSeek 开放平台 [platform.deepseek.com](https://platform.deepseek.com)：注册 → 实名认证 → 充值 → 创建 API Key，接口为 OpenAI 兼容格式，即开即用。

## 接口一览

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/v1/health` | GET | 健康检查 |
| `/api/v1/evaluate` | POST | 非流式 AI 评价（score/feedback/追问） |
| `/api/v1/evaluate/stream` | POST | SSE 流式 AI 评价 |
| `/api/v1/search` | POST | AI 生成知识点列表 |
