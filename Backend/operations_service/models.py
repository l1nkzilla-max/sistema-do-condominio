"""
Modelos de dados do Operations Service
"""
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Area(Base):
    """Modelo de Área Comum"""
    __tablename__ = "areas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    capacity = Column(Integer)
    hourly_rate = Column(DECIMAL(10, 2))
    requires_approval = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    schedulings = relationship("Scheduling", back_populates="area")


class Scheduling(Base):
    """Modelo de Agendamento"""
    __tablename__ = "schedulings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=False, index=True)
    unit_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    start_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    end_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(String(20), nullable=False, default='pending', index=True)
    purpose = Column(Text)
    guests_count = Column(Integer)
    approved_by = Column(Integer)
    approved_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    area = relationship("Area", back_populates="schedulings")


class Budget(Base):
    """Modelo de Orçamento"""
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(20), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    provider_id = Column(Integer, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default='draft', index=True)
    requested_by = Column(Integer, nullable=False, index=True)
    approved_by = Column(Integer)
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    history = relationship("BudgetHistory", back_populates="budget", cascade="all, delete-orphan")


class BudgetHistory(Base):
    """Modelo de Histórico de Orçamento"""
    __tablename__ = "budget_history"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False, index=True)
    old_status = Column(String(20))
    new_status = Column(String(20), nullable=False)
    changed_by = Column(Integer, nullable=False)
    comments = Column(Text)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    budget = relationship("Budget", back_populates="history")


class Event(Base):
    """Modelo de Evento"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    location = Column(String(255))
    organizer_id = Column(Integer, nullable=False, index=True)
    is_public = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Meeting(Base):
    """Modelo de Reunião"""
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    meeting_date = Column(DateTime(timezone=True), nullable=False, index=True)
    location = Column(String(255))
    organizer_id = Column(Integer, nullable=False, index=True)
    status = Column(String(20), nullable=False, default='scheduled', index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    history = relationship("MeetingHistory", back_populates="meeting", cascade="all, delete-orphan")
    minute = relationship("Minute", back_populates="meeting", uselist=False, cascade="all, delete-orphan")


class MeetingHistory(Base):
    """Modelo de Histórico de Reunião"""
    __tablename__ = "meeting_history"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(Integer, nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    meeting = relationship("Meeting", back_populates="history")


class Minute(Base):
    """Modelo de Ata"""
    __tablename__ = "minutes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False, unique=True, index=True)
    content = Column(Text, nullable=False)
    attendees = Column(Text)
    decisions = Column(Text)
    issued_by = Column(Integer, nullable=False, index=True)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    meeting = relationship("Meeting", back_populates="minute")
    history = relationship("MinuteHistory", back_populates="minute", cascade="all, delete-orphan")


class MinuteHistory(Base):
    """Modelo de Histórico de Ata"""
    __tablename__ = "minute_history"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    minute_id = Column(Integer, ForeignKey("minutes.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(Integer, nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    minute = relationship("Minute", back_populates="history")


class Document(Base):
    """Modelo de Documento"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    uploaded_by = Column(Integer, nullable=False, index=True)
    is_public = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Visitor(Base):
    """Modelo de Visitante"""
    __tablename__ = "visitors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    document = Column(String(20))
    unit_id = Column(Integer, nullable=False, index=True)
    entry_time = Column(DateTime(timezone=True), nullable=False, index=True)
    exit_time = Column(DateTime(timezone=True))
    vehicle_plate = Column(String(10))
    purpose = Column(Text)
    authorized_by = Column(Integer)
    registered_by = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notice(Base):
    """Modelo de Aviso"""
    __tablename__ = "notices"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String(50), nullable=False, index=True)
    priority = Column(String(20), nullable=False, default='normal', index=True)
    published_by = Column(Integer, nullable=False, index=True)
    published_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    history = relationship("NoticeHistory", back_populates="notice", cascade="all, delete-orphan")


class NoticeHistory(Base):
    """Modelo de Histórico de Aviso"""
    __tablename__ = "notice_history"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    notice_id = Column(Integer, ForeignKey("notices.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(Integer, nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    notice = relationship("Notice", back_populates="history")


class Log(Base):
    """Modelo de Log de Auditoria"""
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    action = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(100), index=True)
    entity_id = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_method = Column(String(10))
    request_path = Column(String(500))
    request_data = Column(Text)
    response_status = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
