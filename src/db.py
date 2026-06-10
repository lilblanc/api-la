import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Busca a URL do banco
db_url = os.getenv("DATABASE_URL")

if not db_url:
    # Se não houver DATABASE_URL, assume que estamos em desenvolvimento local
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:13467900@localhost:5432/learning-analytics"
else:
    # Se houver DATABASE_URL, garante que o prefixo esteja correto para o SQLAlchemy 2.0
    SQLALCHEMY_DATABASE_URL = db_url.replace("postgres://", "postgresql://", 1) if db_url.startswith("postgres://") else db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()