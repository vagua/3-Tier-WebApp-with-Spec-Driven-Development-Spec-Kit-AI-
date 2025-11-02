#!/bin/bash
STACK_NAME=mcapp

echo "Removing stack $STACK_NAME..."
docker stack rm $STACK_NAME

sleep 5

echo "Removing DB volume..."
docker volume rm ${STACK_NAME}_db_data ${STACK_NAME}_db_init 2>/dev/null || true

echo "Done. Environment cleaned."
