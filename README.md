# Levantar ActiveMQ con Docker

## Comando para levantar ActiveMQ

```bash
docker run -d --name activemq -p 61616:61616 -p 8161:8161 -p 61613:61613 rmohr/activemq
```

## Comando para bajarte ActiveMQ

```bash
docker stop activemq
```

## Contenerizar

```bash
Flask==2.1.1
stomp.py==7.0.0
```

```bash
FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000

CMD ["activemq:61616", "--", "python", "app.py"]
```

```bash
version: '3.8'

services:
  activemq:
    image: rmohr/activemq:5.15.9
    container_name: activemq
    ports:
      - "61616:61616"
      - "8161:8161"
    environment:
      ACTIVEMQ_USER: admin
      ACTIVEMQ_PASSWORD: admin
      ACTIVEMQ_MIN_MEMORY: 512
      ACTIVEMQ_MAX_MEMORY: 2048
      ACTIVEMQ_ENABLE_JMX: 'true'

  flaskapp:
    build: .
    container_name: flaskapp
    ports:
      - "5000:5000"
    depends_on:
      - activemq
    environment:
      ACTIVEMQ_BROKER_URL: tcp://activemq:61616
```

```bash
docker-compose up --build
```
