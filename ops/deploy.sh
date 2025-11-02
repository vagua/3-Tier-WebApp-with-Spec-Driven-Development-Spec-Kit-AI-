#!/bin/bash
# 部署 mcapp stack

STACK_NAME=mcapp
STACK_FILE=swarm/stack.yaml

echo "Deploying stack $STACK_NAME..."
docker stack deploy -c $STACK_FILE $STACK_NAME

echo "Waiting 10s for services to start..."
sleep 10

echo "Stack services:"
docker stack services $STACK_NAME
