#!/usr/bin/env bash
project_name='rescuewill'
PROJECT_PATH="$(cd `dirname $0`; cd ..; pwd)"
echo "cd ${PROJECT_PATH}"
cd ${PROJECT_PATH}

docker build \
        --rm=true \
        -f docker/Dockerfile \
        -t flamedancer/${project_name} . \
        --build-arg project_name=${project_name} \
        && docker push flamedancer/${project_name}