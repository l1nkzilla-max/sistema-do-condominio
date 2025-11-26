"""
Operations Service - Microserviço de Operações
Sistema de Condomínio
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import date, datetime, time

from config import settings
from database import get_db, engine, Base
from models import (Area, Scheduling, Budget, BudgetHistory, Event, Meeting, MeetingHistory,
                    Minute, MinuteHistory, Document, Visitor, Notice, NoticeHistory, Log)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(
    title="Operations Service",
    description="Microserviço de Operações - Sistema de Condomínio",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Schemas ==========

class AreaCreate(BaseModel):
    name: str
    description: str = None
    capacity: int = None
    hourly_rate: float = None
    requires_approval: bool = False

class SchedulingCreate(BaseModel):
    area_id: int
    unit_id: int
    user_id: int
    start_datetime: datetime
    end_datetime: datetime
    purpose: str = None
    guests_count: int = None

class BudgetCreate(BaseModel):
    type: str
    title: str
    description: str = None
    provider_id: int = None
    amount: float
    requested_by: int

class EventCreate(BaseModel):
    title: str
    description: str = None
    event_date: date
    start_time: time = None
    end_time: time = None
    location: str = None
    organizer_id: int

class MeetingCreate(BaseModel):
    title: str
    description: str = None
    meeting_date: datetime
    location: str = None
    organizer_id: int

class MinuteCreate(BaseModel):
    meeting_id: int
    content: str
    attendees: str = None
    decisions: str = None
    issued_by: int

class DocumentCreate(BaseModel):
    title: str
    type: str
    description: str = None
    file_path: str
    file_name: str
    file_size: int = None
    mime_type: str = None
    uploaded_by: int
    is_public: bool = False

class VisitorCreate(BaseModel):
    name: str
    document: str = None
    unit_id: int
    entry_time: datetime
    vehicle_plate: str = None
    purpose: str = None
    registered_by: int

class NoticeCreate(BaseModel):
    title: str
    content: str
    type: str
    priority: str = 'normal'
    published_by: int
    expires_at: datetime = None

# ========== Rotas de Áreas ==========

@app.get("/api/areas", tags=["Áreas Comuns"])
async def list_areas(db: Session = Depends(get_db)):
    return db.query(Area).all()

@app.post("/api/areas", status_code=201, tags=["Áreas Comuns"])
async def create_area(area_data: AreaCreate, db: Session = Depends(get_db)):
    area = Area(**area_data.dict())
    db.add(area)
    db.commit()
    db.refresh(area)
    return area

# ========== Rotas de Agendamentos ==========

@app.get("/api/schedulings", tags=["Agendamentos"])
async def list_schedulings(db: Session = Depends(get_db)):
    return db.query(Scheduling).all()

@app.post("/api/schedulings", status_code=201, tags=["Agendamentos"])
async def create_scheduling(scheduling_data: SchedulingCreate, db: Session = Depends(get_db)):
    scheduling = Scheduling(**scheduling_data.dict())
    db.add(scheduling)
    db.commit()
    db.refresh(scheduling)
    return scheduling

@app.put("/api/schedulings/{scheduling_id}/approve", tags=["Agendamentos"])
async def approve_scheduling(scheduling_id: int, approved_by: int, db: Session = Depends(get_db)):
    scheduling = db.query(Scheduling).filter(Scheduling.id == scheduling_id).first()
    if not scheduling:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    scheduling.status = 'approved'
    scheduling.approved_by = approved_by
    scheduling.approved_at = datetime.utcnow()
    db.commit()
    return scheduling

# ========== Rotas de Orçamentos ==========

@app.get("/api/budgets", tags=["Orçamentos"])
async def list_budgets(db: Session = Depends(get_db)):
    return db.query(Budget).all()

@app.post("/api/budgets", status_code=201, tags=["Orçamentos"])
async def create_budget(budget_data: BudgetCreate, db: Session = Depends(get_db)):
    budget = Budget(**budget_data.dict())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

@app.get("/api/budgets/{budget_id}/history", tags=["Orçamentos"])
async def get_budget_history(budget_id: int, db: Session = Depends(get_db)):
    return db.query(BudgetHistory).filter(BudgetHistory.budget_id == budget_id).all()

# ========== Rotas de Eventos ==========

@app.get("/api/events", tags=["Eventos"])
async def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@app.post("/api/events", status_code=201, tags=["Eventos"])
async def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    event = Event(**event_data.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

# ========== Rotas de Reuniões ==========

@app.get("/api/meetings", tags=["Reuniões"])
async def list_meetings(db: Session = Depends(get_db)):
    return db.query(Meeting).all()

@app.post("/api/meetings", status_code=201, tags=["Reuniões"])
async def create_meeting(meeting_data: MeetingCreate, db: Session = Depends(get_db)):
    meeting = Meeting(**meeting_data.dict())
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting

@app.get("/api/meetings/{meeting_id}/history", tags=["Reuniões"])
async def get_meeting_history(meeting_id: int, db: Session = Depends(get_db)):
    return db.query(MeetingHistory).filter(MeetingHistory.meeting_id == meeting_id).all()

@app.post("/api/meetings/{meeting_id}/send-email", tags=["Reuniões"])
async def send_meeting_email(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    # TODO: Implementar envio de e-mail
    return {"message": "E-mail enviado com sucesso"}

# ========== Rotas de Atas ==========

@app.get("/api/minutes", tags=["Atas"])
async def list_minutes(db: Session = Depends(get_db)):
    return db.query(Minute).all()

@app.post("/api/minutes", status_code=201, tags=["Atas"])
async def create_minute(minute_data: MinuteCreate, db: Session = Depends(get_db)):
    minute = Minute(**minute_data.dict())
    db.add(minute)
    db.commit()
    db.refresh(minute)
    return minute

@app.get("/api/minutes/{minute_id}/history", tags=["Atas"])
async def get_minute_history(minute_id: int, db: Session = Depends(get_db)):
    return db.query(MinuteHistory).filter(MinuteHistory.minute_id == minute_id).all()

@app.post("/api/minutes/{minute_id}/send-email", tags=["Atas"])
async def send_minute_email(minute_id: int, db: Session = Depends(get_db)):
    minute = db.query(Minute).filter(Minute.id == minute_id).first()
    if not minute:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    minute.sent_at = datetime.utcnow()
    db.commit()
    # TODO: Implementar envio de e-mail
    return {"message": "E-mail enviado com sucesso"}

# ========== Rotas de Documentos ==========

@app.get("/api/documents", tags=["Documentos"])
async def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@app.post("/api/documents", status_code=201, tags=["Documentos"])
async def create_document(document_data: DocumentCreate, db: Session = Depends(get_db)):
    document = Document(**document_data.dict())
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

# ========== Rotas de Visitantes ==========

@app.get("/api/visitors", tags=["Visitantes"])
async def list_visitors(db: Session = Depends(get_db)):
    return db.query(Visitor).all()

@app.post("/api/visitors", status_code=201, tags=["Visitantes"])
async def create_visitor(visitor_data: VisitorCreate, db: Session = Depends(get_db)):
    visitor = Visitor(**visitor_data.dict())
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor

@app.put("/api/visitors/{visitor_id}/exit", tags=["Visitantes"])
async def register_exit(visitor_id: int, db: Session = Depends(get_db)):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")
    visitor.exit_time = datetime.utcnow()
    db.commit()
    return visitor

# ========== Rotas de Avisos ==========

@app.get("/api/notices", tags=["Avisos"])
async def list_notices(db: Session = Depends(get_db)):
    return db.query(Notice).filter(Notice.is_active == True).all()

@app.post("/api/notices", status_code=201, tags=["Avisos"])
async def create_notice(notice_data: NoticeCreate, db: Session = Depends(get_db)):
    notice = Notice(**notice_data.dict())
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice

@app.get("/api/notices/{notice_id}/history", tags=["Avisos"])
async def get_notice_history(notice_id: int, db: Session = Depends(get_db)):
    return db.query(NoticeHistory).filter(NoticeHistory.notice_id == notice_id).all()

@app.get("/api/notice-board", tags=["Avisos"])
async def get_notice_board(db: Session = Depends(get_db)):
    """Quadro de avisos - avisos ativos e não expirados"""
    now = datetime.utcnow()
    return db.query(Notice).filter(
        Notice.is_active == True,
        (Notice.expires_at == None) | (Notice.expires_at > now)
    ).order_by(Notice.published_at.desc()).all()

# ========== Rotas de Logs e Auditoria ==========

@app.get("/api/logs", tags=["Auditoria"])
async def list_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Log).order_by(Log.created_at.desc()).offset(skip).limit(limit).all()

@app.get("/api/audit", tags=["Auditoria"])
async def get_audit(
    user_id: int = None,
    action: str = None,
    entity_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Auditoria com filtros"""
    query = db.query(Log)
    if user_id:
        query = query.filter(Log.user_id == user_id)
    if action:
        query = query.filter(Log.action == action)
    if entity_type:
        query = query.filter(Log.entity_type == entity_type)
    return query.order_by(Log.created_at.desc()).offset(skip).limit(limit).all()

# ========== Health Check ==========

@app.get("/health", tags=["Sistema"])
async def health_check():
    return {"status": "healthy", "service": "operations_service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=settings.API_RELOAD)
