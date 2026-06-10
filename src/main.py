from fastapi import FastAPI, Depends, HTTPException, APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from src import models, schemas
from src.db import engine, get_db
from datetime import datetime, timedelta
import random


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Learning Analytics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://learning-analytics.vercel.app",
        "https://learning-analytics-git-main-lilblanc.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/eventos", status_code=201)
def registrar_evento(payload: schemas.Payload, db: Session = Depends(get_db)):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.id_usuario == payload.atividade.id_usuario).first()
    if not usuario_db:
        usuario_db = models.Usuario(
            id_usuario=payload.atividade.id_usuario,
            nome=f"Aluno {payload.atividade.id_usuario.split('_')[1]}" if "_" in payload.atividade.id_usuario else payload.atividade.id_usuario
        )
        db.add(usuario_db)
        db.commit()

    atividade_db = db.query(models.Atividade).filter(
        models.Atividade.id_atividade == payload.atividade.id_atividade
    ).first()
    
    if not atividade_db:
        atividade_db = models.Atividade(
            id_atividade=payload.atividade.id_atividade,
            id_usuario=payload.atividade.id_usuario,
            ferramenta=payload.atividade.ferramenta,
            dispositivo=payload.atividade.dispositivo
        )
        db.add(atividade_db)
        db.commit()

    novo_evento = models.Evento(
        id_atividade=atividade_db.id_atividade,
        tipo_evento=payload.evento.tipo_evento,
        timestamp=payload.evento.timestamp,
        dados_especificos=payload.evento.dados_especificos
    )
    
    db.add(novo_evento)
    db.commit()
    
    return {"status": "sucesso", "mensagem": "Evento registrado com sucesso"}



def get_data_inicio(time_range: str):
    hoje = datetime.utcnow()
    if time_range == '7d': return hoje - timedelta(days=7)
    elif time_range == '30d': return hoje - timedelta(days=30)
    elif time_range == '90d': return hoje - timedelta(days=90)
    elif time_range == '1y': return hoje - timedelta(days=365)
    return hoje - timedelta(days=7)


@app.get("/api/dashboard/metricas-gerais")
def get_metricas_gerais(range: str = '7d', db: Session = Depends(get_db)):
    data_corte = get_data_inicio(range)
    
    estudantes = db.query(models.Atividade.id_usuario).filter(
        models.Atividade.data_inicio >= data_corte
    ).distinct().count()
    
    cursos = db.query(models.Atividade.ferramenta).filter(
        models.Atividade.data_inicio >= data_corte
    ).distinct().count()
    
    total_atividades = db.query(models.Atividade).filter(models.Atividade.data_inicio >= data_corte).count()
    concluidas = db.query(models.Evento).join(models.Atividade).filter(
        models.Atividade.data_inicio >= data_corte,
        models.Evento.tipo_evento == "finalizacao"
    ).count()
    
    taxa = (concluidas / total_atividades * 100) if total_atividades > 0 else 0

    return {
        "estudantes": {"valor": str(estudantes), "mudanca": "+12.5%"}, 
        "ferramentas": {"valor": str(cursos), "mudanca": "+2"},
        "conclusao": {"valor": f"{taxa:.1f}%", "mudanca": "+5.2%"}
    }


@app.get("/api/dashboard/engajamento")
def get_engajamento(range: str = '7d', db: Session = Depends(get_db)):
    data_corte = get_data_inicio(range)
    dias_semana = {0: "Dom", 1: "Seg", 2: "Ter", 3: "Qua", 4: "Qui", 5: "Sex", 6: "Sáb"}
    resultado = []
    
    for dow, nome in dias_semana.items():
        ativos = db.query(models.Atividade.id_usuario).filter(
            models.Atividade.data_inicio >= data_corte,
            func.extract('dow', models.Atividade.data_inicio) == dow
        ).distinct().count()
        
        concluidos = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.data_inicio >= data_corte,
            models.Evento.tipo_evento == "finalizacao",
            func.extract('dow', models.Evento.timestamp) == dow
        ).count()
        
        tentativas = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.data_inicio >= data_corte,
            models.Evento.tipo_evento == "tentativa",
            func.extract('dow', models.Evento.timestamp) == dow
        ).count()
        
        resultado.append({
            "data": nome, "ativos": ativos, "concluidos": concluidos, "tentativas": tentativas
        })
    return resultado


@app.get("/api/dashboard/atividade-recente")
def get_atividade_recente(db: Session = Depends(get_db)):
    ultimos = db.query(models.Evento).order_by(desc(models.Evento.timestamp)).limit(5).all()
    resultado = []
    
    for evt in ultimos:
        nome_aluno = evt.atividade.id_usuario if evt.atividade else "Anonymous"
        
        if "estudante" in nome_aluno or "user" in nome_aluno:
            partes = nome_aluno.split("_")
            nome_aluno = f"User{partes[1]}" if len(partes) > 1 else nome_aluno
        elif "aluno" in nome_aluno:
             partes = nome_aluno.split("_")
             nome_aluno = f"User{partes[-1]}" if len(partes) > 1 else nome_aluno

        resultado.append({
            "estudante": nome_aluno,
            "iniciais": nome_aluno[:2].upper(),
            "acao": "Concluiu" if evt.tipo_evento == "acerto" else "Errou" if evt.tipo_evento == "erro" else "Iniciou",
            "aplicacao": evt.atividade.ferramenta if evt.atividade else "Desconhecida",
            "tempo": evt.timestamp.strftime("%H:%M"), 
            "status": "concluido" if evt.tipo_evento == "acerto" else "em-progresso"
        })
    return resultado


@app.get("/api/dashboard/conclusao-atividades")
def get_conclusao_atividades(db: Session = Depends(get_db)):
    ferramentas_sujas = db.query(models.Atividade.ferramenta).distinct().all()
    ferramentas_validas = [f[0] for f in ferramentas_sujas if f[0] and f[0] not in ["string", "jogo_tabela-periodica"]]
    resultado = []

    for f in ferramentas_validas:
        total = db.query(models.Atividade).filter(models.Atividade.ferramenta == f).count()
        concluidos = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.ferramenta == f,
            models.Evento.tipo_evento == "finalizacao"
        ).count()

        resultado.append({
            "aplicacao": f,
            "matriculados": total,
            "completado": concluidos,
            "emProgresso": max(0, total - concluidos)
        })
    return resultado


@app.get("/api/dashboard/tributos")
def get_dados_tributos(db: Session = Depends(get_db)):
    tributos_raw = db.query(models.Evento.dados_especificos['assunto_pedagogico'].astext).distinct().filter(
        models.Evento.tipo_evento.in_(["acerto", "erro"])
    ).all()
    tributos = [t[0] for t in tributos_raw if t[0]]
    
    resultado = []
    for t in tributos:
        acertos = db.query(models.Evento).filter(
            models.Evento.tipo_evento == "acerto",
            models.Evento.dados_especificos['assunto_pedagogico'].astext == str(t)
        ).count()

        erros = db.query(models.Evento).filter(
            models.Evento.tipo_evento == "erro",
            models.Evento.dados_especificos['assunto_pedagogico'].astext == str(t)
        ).count()

        resultado.append({"tributo": str(t), "acerto": acertos, "erro": erros})
    return resultado


@app.get("/api/dashboard/top-cursos")
def get_top_cursos(db: Session = Depends(get_db)):
    ferramentas_sujas = db.query(func.lower(models.Atividade.ferramenta)).distinct().all()
    ferramentas_validas = [f[0] for f in ferramentas_sujas if f[0] and f[0] not in ["string", "jogo_tabela-periodica"]]
    resultado = []

    for nome_lower in ferramentas_validas:
        nome_exibicao = db.query(models.Atividade.ferramenta).filter(func.lower(models.Atividade.ferramenta) == nome_lower).first()[0]
        alunos = db.query(models.Atividade).filter(func.lower(models.Atividade.ferramenta) == nome_lower).count()
        concluidos = db.query(models.Evento).join(models.Atividade).filter(
            func.lower(models.Atividade.ferramenta) == nome_lower, 
            models.Evento.tipo_evento == "finalizacao"
        ).count()

        taxa = int((concluidos / alunos * 100)) if alunos > 0 else 0

        resultado.append({
            "nome": nome_exibicao,
            "estudantes": alunos,
            "avaliacao": round(random.uniform(4.0, 5.0), 1), 
            "taxaConclusao": taxa,
            "tendencia": "up" if taxa > 50 else "down",
            "mudanca": random.randint(2, 15)
        })
    return sorted(resultado, key=lambda x: x['estudantes'], reverse=True)

@app.get("/api/dashboard/escolas")
def get_desempenho_escolas(db: Session = Depends(get_db)):
    escolas = db.query(models.Escola).all()
    resultado = []
    
    for esc in escolas:
        alunos_ids = [u.id_usuario for u in esc.usuarios]
        total_alunos = len(alunos_ids)
        
        if total_alunos == 0:
            resultado.append({
                "escola": esc.nome,
                "estudantes": 0,
                "notaMedia": 0,
                "taxaConclusao": 0
            })
            continue

        concluidos = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.id_usuario.in_(alunos_ids),
            models.Evento.tipo_evento == "finalizacao"
        ).count()
        
        atividades_totais = db.query(models.Atividade).filter(
            models.Atividade.id_usuario.in_(alunos_ids)
        ).count()
        
        taxa = (concluidos / atividades_totais * 100) if atividades_totais > 0 else 0
        
        acertos = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.id_usuario.in_(alunos_ids),
            models.Evento.tipo_evento == "acerto"
        ).count()
        erros = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.id_usuario.in_(alunos_ids),
            models.Evento.tipo_evento == "erro"
        ).count()
        
        nota = (acertos / (acertos + erros) * 100) if (acertos + erros) > 0 else 0

        resultado.append({
            "escola": esc.nome,
            "estudantes": total_alunos,
            "notaMedia": round(nota, 1),
            "taxaConclusao": int(taxa)
        })
    return resultado


@app.get("/api/dashboard/cidades")
def get_desempenho_cidades(db: Session = Depends(get_db)):
    cidades = db.query(models.Cidade).all()
    resultado = []
    
    for cid in cidades:
        alunos_ids = [u.id_usuario for u in cid.usuarios]
        total_alunos = len(alunos_ids)
        
        if total_alunos == 0:
            resultado.append({
                "cidade": cid.nome,
                "estudantes": 0,
                "notaMedia": 0,
                "engajamento": 0,
                "taxaConclusao": 0
            })
            continue

        concluidos = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.id_usuario.in_(alunos_ids),
            models.Evento.tipo_evento == "finalizacao"
        ).count()
        
        atividades_totais = db.query(models.Atividade).filter(
            models.Atividade.id_usuario.in_(alunos_ids)
        ).count()
        
        taxa = (concluidos / atividades_totais * 100) if atividades_totais > 0 else 0
        
        acertos = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.id_usuario.in_(alunos_ids),
            models.Evento.tipo_evento == "acerto"
        ).count()
        erros = db.query(models.Evento).join(models.Atividade).filter(
            models.Atividade.id_usuario.in_(alunos_ids),
            models.Evento.tipo_evento == "erro"
        ).count()
        
        nota = (acertos / (acertos + erros) * 100) if (acertos + erros) > 0 else 0

        resultado.append({
            "cidade": cid.nome,
            "estudantes": total_alunos,
            "notaMedia": round(nota, 1),
            "engajamento": random.randint(70, 95), 
            "taxaConclusao": int(taxa)
        })
    return resultado


@app.get("/api/dashboard/performance")
def get_distribuicao_performance(db: Session = Depends(get_db)):
    # Busca todos os usuários que possuem pelo menos um evento de acerto ou erro
    stats = db.query(
        models.Atividade.id_usuario,
        func.count(models.Evento.id_evento).filter(models.Evento.tipo_evento == "acerto").label("acertos"),
        func.count(models.Evento.id_evento).filter(models.Evento.tipo_evento == "erro").label("erros")
    ).join(models.Evento).group_by(models.Atividade.id_usuario).all()

    dist = {
        "Excelente (90–100%)": 0,
        "Bom (80–89%)": 0,
        "Mediano (70–79%)": 0,
        "Abaixo da média (<70%)": 0
    }
    
    for _, acertos, erros in stats:
        total = acertos + erros
        if total > 0:
            pct = (acertos / total) * 100
            if pct >= 90: dist["Excelente (90–100%)"] += 1
            elif pct >= 80: dist["Bom (80–89%)"] += 1
            elif pct >= 70: dist["Mediano (70–79%)"] += 1
            else: dist["Abaixo da média (<70%)"] += 1

    return [
        {"nome": "Excelente (90–100%)", "valor": dist["Excelente (90–100%)"], "cor": "#10b981"},
        {"nome": "Bom (80–89%)", "valor": dist["Bom (80–89%)"], "cor": "#3b82f6"},
        {"nome": "Mediano (70–79%)", "valor": dist["Mediano (70–79%)"], "cor": "#f59e0b"},
        {"nome": "Abaixo da média (<70%)", "valor": dist["Abaixo da média (<70%)"], "cor": "#ef4444"}
    ]