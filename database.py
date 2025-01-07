from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

URL_DATABASE = "mysql+pymysql://root:Root%401234@localhost:3306/BlogApplication"

engine = create_engine(URL_DATABASE,pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine )

Base = declarative_base()
