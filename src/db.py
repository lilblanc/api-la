import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Busca a URL do banco
db_url = os.getenv("DATABASE_URL")

# Log de diagnóstico (não exibe a senha por segurança)
if db_url:
    print(f"URL do Banco detectada: {db_url.split('@')[-1]}")
    # Corrige o prefixo para SQLAlchemy 2.0
    SQLALCHEMY_DATABASE_URL = db_url.replace("postgres://", "postgresql://", 1) if db_url.startswith("postgres://") else db_url
else:
    print("ERRO CRÍTICO: DATABASE_URL não encontrada no ambiente!")
    # Se estivermos no Railway (geralmente tem a variável RAILWAY_ENVIRONMENT), não permitimos localhost
    if os.getenv("RAILWAY_ENVIRONMENT"):
        print("Abortando: Não é permitido usar localhost em produção (Railway).")
        sys.exit(1)
    
    print("Usando fallback de desenvolvimento (localhost)...")
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:13467900@localhost:5432/learning-analytics"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()