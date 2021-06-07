#!/usr/bin/env bash

project_name='rescuewill'
config_mode='production'
PROJECT_PATH="$(cd `dirname $0`; cd ..; pwd)"

echo "cd ${PROJECT_PATH}"
cd ${PROJECT_PATH}

mkdir -p logs

# 后台运行
docker run \
        -d \
        --name ${project_name} \
        -h ${PROJECT_PATH} \
        -v "${PWD}":/${project_name} \
        -p 5000:5000 \
        -e CONFIG_MODE=${config_mode} \
        -e FLASK_ENV=${config_mode} \
        --link some-mysql \
        --privileged \
        --restart=always \
        -e TZ=Asia/Shanghai \
        flamedancer/${project_name} \
        python ${project_name}/hello.py