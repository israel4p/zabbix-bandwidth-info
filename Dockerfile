FROM alpine:latest

RUN apk update && \
      apk upgrade && \
      apk add python3-dev

WORKDIR /app

ADD . /app

RUN pip3 install --upgrade pip && \
      pip3 install -r requirements.txt

CMD ["python3", "main.py"]
