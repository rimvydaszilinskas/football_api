import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Build the URL
DB_URL = 'mysql://{username}:{password}@{host}:{port}/{db}'.format(
    username=os.environ.get('MYSQL_USERNAME', 'root'),
    password=os.environ.get('MYSQL_PASSWORD', 'password'),
    host=os.environ.get('MYSQL_HOST', '127.0.0.1'),
    port=os.environ.get('MYSQL_PORT', '3307'),
    db=os.environ.get('MYSQL_DB', 'football'))

engine = create_engine(DB_URL)
# Create database connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
