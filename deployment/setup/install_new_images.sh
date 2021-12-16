#! /bin/bash

echo "Loading new images"

docker load < dig_mysql_server.tar.gz
docker load < dig_server.tar.gz

echo "done loading new images"