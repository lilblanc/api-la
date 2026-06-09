from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db import Base

class Cidade(Base):
    __tablename__ = "cidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    escolas = relationship("Escola", back_populates="cidade")
    usuarios = relationship("Usuario", back_populates="cidade")

class Escola(Base):
    __tablename__ = "escolas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    id_cidade = Column(Integer, ForeignKey("cidades.id"))
    cidade = relationship("Cidade", back_populates="escolas")
    usuarios = relationship("Usuario", back_populates="escola")

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(String, primary_key=True, index=True)
    nome = Column(String)
    id_escola = Column(Integer, ForeignKey("escolas.id"))
    id_cidade = Column(Integer, ForeignKey("cidades.id"))
    
    escola = relationship("Escola", back_populates="usuarios")
    cidade = relationship("Cidade", back_populates="usuarios")
    atividades = relationship("Atividade", back_populates="usuario")

class Atividade(Base):
    __tablename__ = "atividades"

    id_atividade = Column(String, primary_key=True, index=True)
    id_usuario = Column(String, ForeignKey("usuarios.id_usuario"))
    ferramenta = Column(String)
    dispositivo = Column(String)
    data_inicio = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="atividades")
    eventos = relationship("Evento", back_populates="atividade")

class Evento(Base):
    __tablename__ = "eventos"

    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    id_atividade = Column(String, ForeignKey("atividades.id_atividade"))
    tipo_evento = Column(String, index=True) 
    timestamp = Column(DateTime, default=datetime.utcnow)
    dados_especificos = Column(JSONB) 
    
    atividade = relationship("Atividade", back_populates="eventos")