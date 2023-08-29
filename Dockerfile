FROM python:3.8 AS build-env
ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY . /build/

RUN apt-get update -y
RUN apt-get update --fix-missing

RUN apt-get install -y \
    g++ \
    make \
    cmake \
    unzip 

WORKDIR /build/
RUN python3.8 -m pip install --requirement requirements.txt

WORKDIR /build/src
ENTRYPOINT [ "/usr/local/bin/python3.8", "-m", "awslambdaric"]
CMD [ "main.handler" ]

