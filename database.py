from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


TEST_DB = "postgresql://postgres:postgres@127.0.0.1:5432/postgres"

engine = create_engine(TEST_DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
