# Levantar ActiveMQ con Docker

## Comando para levantar ActiveMQ

```bash
docker run -d --name activemq -p 61616:61616 -p 8161:8161 -p 61613:61613 rmohr/activemq
```

## Comando para bajarte ActiveMQ

```bash
docker stop activemq
```
