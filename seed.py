import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.db import SessionLocal
from src.models import Atividade, Evento, Cidade, Escola, Usuario

ferramentas = ["Pequeno Grande Cidadão", "FlagMatch", "BordersQuiz", "Atoms Game"]
tributos = ["ICMS", "IPVA", "IPTU", "ISS"]

dados_geograficos = {
    "Cuiabá": ["Escola Estadual Cuiabá", "Colégio Particular Alpha"],
    "Várzea Grande": ["Escola Municipal VG", "Instituto Federal VG"],
    "Sinop": ["Escola do Norte", "Colégio Sinopse"],
    "Santo Antônio": ["Escola Rural Sto Antônio"]
}

def popular_banco():
    db = SessionLocal()
    
    # Criar cidades e escolas se não existirem
    escolas_objs = []
    for nome_cidade, escolas_lista in dados_geograficos.items():
        cid = db.query(Cidade).filter(Cidade.nome == nome_cidade).first()
        if not cid:
            cid = Cidade(nome=nome_cidade)
            db.add(cid)
            db.commit()
            db.refresh(cid)
        
        for nome_esc in escolas_lista:
            esc = db.query(Escola).filter(Escola.nome == nome_esc).first()
            if not esc:
                esc = Escola(nome=nome_esc, id_cidade=cid.id)
                db.add(esc)
                db.commit()
                db.refresh(esc)
            escolas_objs.append(esc)

    # Gerar 40 usuários distribuídos pelas escolas/cidades
    for i in range(1, 41):
        # Rotaciona as escolas para garantir que todas (e cidades) tenham alunos
        esc_obj = escolas_objs[i % len(escolas_objs)]
        id_u = f"user_{1000 + i}"
        
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_u).first()
        if not usuario:
            usuario = Usuario(
                id_usuario=id_u,
                nome=f"User{1000 + i}",
                id_escola=esc_obj.id,
                id_cidade=esc_obj.id_cidade
            )
            db.add(usuario)
            db.commit()
        
        # Gerar 2 atividades para cada usuário
        for _ in range(2):
            gerar_atividade_para_usuario(db, id_u)
            
    db.commit()
    db.close()
    print("Banco populado com sucesso com nomes anonimizados e dados em todas as cidades!")

def gerar_atividade_para_usuario(db, id_usuario):
    ferramenta_escolhida = random.choice(ferramentas)
    id_atividade = f"sessao_mock_{random.randint(100000, 999999)}"
    
    # Define uma "habilidade" para o usuário para variar as notas
    habilidade = random.uniform(0.5, 1.0)
    
    nova_atividade = Atividade(
        id_atividade=id_atividade,
        id_usuario=id_usuario,
        ferramenta=ferramenta_escolhida,
        dispositivo="desktop",
        data_inicio=datetime.utcnow() - timedelta(days=random.randint(0, 30))
    )
    db.add(nova_atividade)
    db.commit()

    qtd_eventos = random.randint(10, 25) 
    for _ in range(qtd_eventos):
        tipo = "acerto" if random.random() < habilidade else "erro"
        tributo_escolhido = random.choice(tributos)
        
        novo_evento = Evento(
            id_atividade=id_atividade,
            tipo_evento=tipo,
            timestamp=nova_atividade.data_inicio + timedelta(minutes=random.randint(1, 10)),
            dados_especificos={
                "assunto_pedagogico": tributo_escolhido,
                "pontuacao_obtida": 10 if tipo == "acerto" else 0
            }
        )
        db.add(novo_evento)

    # Garantir finalização para a maioria
    if random.random() > 0.2:
        db.add(Evento(
            id_atividade=id_atividade,
            tipo_evento="finalizacao",
            timestamp=nova_atividade.data_inicio + timedelta(minutes=random.randint(15, 30)),
            dados_especificos={"status": "concluido"}
        ))
    db.commit()

if __name__ == "__main__":
    popular_banco()
