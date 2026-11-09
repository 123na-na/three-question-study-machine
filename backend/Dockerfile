# 三问学习机 Backend 中间层 Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖（利用 Docker 层缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码（仅中间层本体，不含 tests）
COPY main.py .
COPY services ./services

EXPOSE 8000

# 容器内不使用 reload，避免开发模式进程
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
