import os

## Service config
SERVICE_TYPE = os.environ["SERVICE_TYPE"]

# Mongo config
MONGO = os.environ["MONGO"]
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_USER = os.environ["MONGO_USER"]
MONGO_PASS = os.environ["MONGO_PASS"]

# Rabbit config
RABBIT = os.environ["RABBIT"]
RABBIT_PORT = os.environ.get("RABBIT_PORT", 5672)
RABBIT_USER = os.environ["RABBIT_USER"]
RABBIT_PASS = os.environ["RABBIT_PASS"]
