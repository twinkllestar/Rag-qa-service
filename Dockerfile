# 基础镜像:slim 版本体积小
# basic image: slim version is small
FROM python:3.12-slim

# do not write .pyc files, and log output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 先只复制依赖文件并安装:这样改代码时,这一层可以用缓存,不用重装
# First copy dependency files and install: this layer can be cached when code changes, no need to reinstall
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制应用代码
# Then copy application code
COPY app ./app

# 不用 root 运行,降低风险
# Do not run as root to reduce risk
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# 0.0.0.0 = 接受容器外的连接 (127.0.0.1 在容器里外面连不进来)
# 0.0.0.0 = accept connections from outside the container 
# (127.0.0.1 is only accessible from within the container)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]