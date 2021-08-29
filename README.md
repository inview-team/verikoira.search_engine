# Search Engine 

## Build
```bash
docker build -t robot .
```

## Compose
```yml
  worker:
    image: rebot
    container_name: bot
    depends_on:
      - mongodb
      - rabbitmq
    environment:
        RABBIT: 
        RABBIT_USER: 
        RABBIT_PASS: 
        MONGO: 
        MONGO_USER: 
        MONGO_PASS: 
        SERVICE_TYPE: patent
```
