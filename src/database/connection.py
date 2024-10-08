from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:aceit@127.0.0.1:3306/aceit?charset=utf8"

engine = create_engine(DATABASE_URL, echo=True)
# engine = create_engine("mysql+pymysql://[username]:[password]@[host]/[database_name]", echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
