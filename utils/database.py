from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

import urllib

host_server = os.environ.get('mota_db_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('mota_db_server_port', '5432')))
database_name = os.environ.get('mota_db', 'mota_db')
db_username = urllib.parse.quote_plus(str(os.environ.get('mota_db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('mota_db_password', 'postgres')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode', 'prefer')))

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(db_username, db_password, host_server, db_server_port,
                                                               database_name)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
