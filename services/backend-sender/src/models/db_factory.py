from pony.orm import *
from src.config import DB_PROVIDER, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

db = Database()

db.bind(provider=DB_PROVIDER, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
# print('DB_factory')