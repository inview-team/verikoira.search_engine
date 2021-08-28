import os

# Mongo interaction
MONGO = os.environ['MONGO']
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USER = os.environ['MONGO_USER']
MONGO_PASS = os.environ['MONGO_PASS']
MONGO_DB = os.environ['MONGO_DB']

# Keyword
KEYWORD = os.environ['KEYWORD']