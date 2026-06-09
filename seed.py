import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.db import SessionLocal
from src.models import Atividade, Evento, Cidade, Escola, Usuario

ferramentas = ["Pequeno Grande Cidadão", "Aventura Fiscal", "Palavras Cruzadas", "Palavras mágicas"]
tributos = ["ICMS", "IPTU", "IPVA"]
nomes_cidades = ["Cuiabá", "Várzea Grande", "Sinop", "Santo Antônio"]
nomes_escolas = ["Escola Santa Maria", "Colégio Dom Bosco", "CEFET-MT", "Instituto Federal"]

def popular_banco():
    db = SessionLocal()
    
    # Criar Cidades
    cidades_objs = []
    for nome in nomes_cidades:
        cid = db.query(Cidade).filter(Cidade.nome == nome).first()
        if not cid:
            cid = Cidade(nome=nome)
            db.add(cid)
            db.commit()
            db.refresh(cid)
        cidades_objs.append(cid)

    # Criar Escolas
    escolas_objs = []
    for nome in nomes_escolas:
        esc = db.query(Escola).filter(Escola.nome == nome).first()
        if not esc:
            esc = Escola(nome=nome, id_cidade=random.choice(cidades_objs).id)
            db.add(esc)
            db.commit()
            db.refresh(esc)
        escolas_objs.append(esc)

    # Criar Usuários e Atividades
    # Primeiro, garantir que cada escola tenha pelo menos alguns usuários com atividades
    for escola in escolas_objs:
        for i in range(3):  # 3 usuários por escola garantidos
            id_usuario = f"estudante_{escola.id}_{i}"
            usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
            if not usuario:
                usuario = Usuario(
                    id_usuario=id_usuario,
                    nome=f"Aluno {escola.nome} {i+1}",
                    id_escola=escola.id,
                    id_cidade=escola.id_cidade
                )
                db.add(usuario)
                db.commit()
            
            # Adicionar atividades para este usuário
            for _ in range(2):
                gerar_atividade_para_usuario(db, id_usuario)

    # Depois, adicionar mais dados aleatórios
    for i in range(30):
        escola_escolhida = random.choice(escolas_objs)
        id_usuario = f"estudante_random_{random.randint(1000, 9999)}"
        
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            usuario = Usuario(
                id_usuario=id_usuario,
                nome=f"Aluno {id_usuario.split('_')[-1]}",
                id_escola=escola_escolhida.id,
                id_cidade=escola_escolhida.id_cidade
            )
            db.add(usuario)
            db.commit()

        gerar_atividade_para_usuario(db, id_usuario)
            
    db.commit()
    db.close()
    print("Banco populado com sucesso com a nova estrutura!")

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

    # Garantir finalização para a maioria, mas deixar alguns em progresso
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

if __name__ == "__main__":
    popular_banco()