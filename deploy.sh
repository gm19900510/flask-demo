# 构建镜像
docker build -t flask-demo:latest .
# 创建容器
docker run -itd --restart=always --log-opt max-size=100m --log-opt max-file=2 -p 8881:8881  --name flask-demo  flask-demo:latest
