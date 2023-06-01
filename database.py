from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config

TEST_DB = "postgresql://" + config().db_user + ":" + config().db_password + "@" + config().db_host + ":" \
          + config().db_port + "/" + config().db_database

engine = create_engine(TEST_DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
