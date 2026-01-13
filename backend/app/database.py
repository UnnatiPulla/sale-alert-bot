from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Later read this from environment variables (.env)
DATABASE_URL = "postgresql+psycopg2://salealert:salealert@localhost:5432/salealertdb"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
