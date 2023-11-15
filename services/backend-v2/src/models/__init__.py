from .db_factory import *
from .user import *
from .channel import *
from .offer import *
from .post import *
from src.config import DB_DEBUG

db.generate_mapping(create_tables=True)
set_sql_debug(DB_DEBUG)