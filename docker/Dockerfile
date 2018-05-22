FROM flamedancer/base-python3

WORKDIR /${project_name}

ADD ./requirements.txt /requirements.txt

RUN apk update && apk add --upgrade --no-cache --virtual .build-dependencies \
    g++ \
    gcc \
    mariadb-dev \
    && pip install -r /requirements.txt \
    && rm -rf /root/.cache \
    && apk del .build-dependencies \
    && apk add --no-cache mariadb-dev

# 时区设置
RUN apk add --no-cache tzdata \
&& echo "${TIME_ZONE}" > /etc/timezone \
&& ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime