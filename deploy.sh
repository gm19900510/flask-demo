# 构建镜像
docker build -t flask-demo:latest .
# 创建容器
docker run -d -p 8881:8881 flask-demo:latest

