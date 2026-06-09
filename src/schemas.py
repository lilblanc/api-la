from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class AtividadeSchema(BaseModel):
    id_atividade: str
    id_usuario: str
    ferramenta: str
    dispositivo: Optional[str] = None

class EventoSchema(BaseModel):
    tipo_evento: str
    timestamp: datetime
    dados_especificos: Dict[str, Any]

class Payload(BaseModel):
    atividade: AtividadeSchema
    evento: EventoSchema