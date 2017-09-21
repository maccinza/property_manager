FROM alpine:3.6

ENV \
    PYTHONUNBUFFERED=1

RUN \
    apk add --no-cache \
        bash \
        python2 \
        python2-dev \
        mariadb-client \
        mariadb-client-libs

RUN \
    apk add --no-cache \
        ca-certificates \
        openssl && \
    wget -O /tmp/get-pip.py "https://bootstrap.pypa.io/get-pip.py" && \
    python /tmp/get-pip.py && \
    rm -f /tmp/get-pip.py && \
    apk del \
        ca-certificates \
        openssl


RUN mkdir /code
WORKDIR /code
ADD requirements /code/requirements

RUN \
    apk add --no-cache \
        gcc \
        musl-dev \
        linux-headers \
        mariadb-dev && \
    pip install -r requirements/dev.txt && \
    apk del \
        gcc \
        musl-dev \
        linux-headers \
        mariadb-dev

ADD . /code

WORKDIR /code

ENTRYPOINT ["/code/docker/entrypoint.sh"]
