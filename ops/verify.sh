#!/bin/bash
STACK_NAME=mcapp

echo "=== Stack Services ==="
docker stack services $STACK_NAME

echo
echo "=== Tasks per Service ==="
for svc in $(docker stack services -q $STACK_NAME); do
    docker service ps $svc
done

echo
echo "=== Check DB on Worker ==="
DB_CONTAINER=$(docker ps -q --filter "name=${STACK_NAME}_db")
if [ -n "$DB_CONTAINER" ]; then
    docker exec -it $DB_CONTAINER psql -U postgres -d namesdb -c "\dt"
    docker exec -it $DB_CONTAINER psql -U postgres -d namesdb -c "SELECT * FROM menu_items;"
else
    echo "DB container not found"
fi
