# About
A exchange for insurance services where companies can list their products and customers can apply for them.

# Tehnology

1. Django (backend / frontend)
2. Celery (task queue)
3. RabbitMQ (message broker)
4. Redis (noSQL db)
5. Elasticsearch (search engine)

# Run
### 1. Сreate a file `.env` in the root of the project
### 2. Сreate variables and assign values
   ```
   DJANGO_SECRET_KEY
   ELASTICSEARCH_HOST
   ELASTICSEARCH_PORT
   CELERY_BROKER_HOST
   CELERY_BROKER_PORT
   REDIS_HOST
   REDIS_PORT
   UNISENDER_API_KEY
   ```
### 3. Example `.env`:
   ```
   DJANGO_SECRET_KEY=autogenerate
   ELASTICSEARCH_HOST=elasticsearch
   ELASTICSEARCH_PORT=9200
   CELERY_BROKER_HOST=rabbitmq
   CELERY_BROKER_PORT=5672
   REDIS_HOST=redis
   REDIS_PORT=6379
   UNISENDER_API_KEY=6hnncnaoxqgbnqcsejn1omx467iksgk8mfjbpd7e
   ```
### 4. Run
   #### If you want to get basic data then run:  
   ```
   python manage.py loaddata fixtures/initial_data.json
   docker-compose up --build
   ```
   #### Default run:
   `docker-compose up --build`
