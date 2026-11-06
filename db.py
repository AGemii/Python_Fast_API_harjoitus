
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'sqlite:///lainaamo.db'

# engine luodaan kerran koko sovelluksen eliniäksi
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kaikki model-luokat perivät tämän
Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        # jos SessionLocal() epäonnistui, db on yhä None eikä suljettavaa ole
        if db is not None:
            db.close()