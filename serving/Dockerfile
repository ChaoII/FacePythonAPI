FROM python:3.9-buster as builder-image

### install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


FROM python:3.9-slim-buster

COPY --from=builder-image /usr/local/bin /usr/local/bin
COPY --from=builder-image /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

WORKDIR /opt/code

COPY . .