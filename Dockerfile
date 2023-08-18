# 使用官方Python运行时作为父镜像
FROM python:3.8-slim-buster

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的/app中
ADD . /app

# 安装项目需要的包
RUN pip install --no-cache-dir -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -r requirements.txt

# 设置环境变量
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露端口
EXPOSE 3000

# 运行api.py和cleanup.py
CMD ["python", "api.py", "&", "python", "cleanup.py"]
