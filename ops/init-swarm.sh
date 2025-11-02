#!/bin/bash
# 初始化 Swarm 與節點角色

# 初始化 Swarm (Manager Node 執行)
echo "Initializing Swarm on Manager..."
docker swarm init --advertise-addr $(hostname -I | awk '{print $1}')

# 取得 Worker Join Token
WORKER_TOKEN=$(docker swarm join-token -q worker)
echo "Worker token: $WORKER_TOKEN"

# 提示 Worker 執行 join
echo "Run this on Worker node:"
echo "docker swarm join --token $WORKER_TOKEN <MANAGER_IP>:2377"

# 設定 Manager 節點角色 label
echo "Label Manager node for backend/frontend services..."
docker node update --label-add role_backend=backend $(hostname)
docker node update --label-add role_frontend=frontend $(hostname)

# 設定 Worker 節點角色 label
echo "After Worker joins, run on Manager:"
echo "docker node update --label-add role=db <WORKER_NODE_NAME>"
