"""
Modelos de dados do Management Service
"""
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Provider(Base):
    """Modelo de Prestador de Serviço"""
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    cnpj_cpf = Column(String(18), unique=True)
    service_type = Column(String(100), nullable=False, index=True)
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    contact_person = Column(String(255))
    notes = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Employee(Base):
    """Modelo de Funcionário"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    role = Column(String(100), nullable=False, index=True)
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    hire_date = Column(Date, nullable=False)
    termination_date = Column(Date)
    salary = Column(DECIMAL(10, 2))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    history = relationship("EmployeeHistory", back_populates="employee", cascade="all, delete-orphan")


class EmployeeHistory(Base):
    """Modelo de Histórico de Funcionário"""
    __tablename__ = "employee_history"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(Integer)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relacionamentos
    employee = relationship("Employee", back_populates="history")


class Patrimony(Base):
    """Modelo de Patrimônio"""
    __tablename__ = "patrimonies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), nullable=False, index=True)
    location = Column(String(255))
    acquisition_date = Column(Date)
    acquisition_value = Column(DECIMAL(10, 2))
    current_value = Column(DECIMAL(10, 2))
    condition = Column(String(50))
    serial_number = Column(String(100))
    notes = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    history = relationship("PatrimonyHistory", back_populates="patrimony", cascade="all, delete-orphan")


class PatrimonyHistory(Base):
    """Modelo de Histórico de Patrimônio"""
    __tablename__ = "patrimony_history"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patrimony_id = Column(Integer, ForeignKey("patrimonies.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(Integer)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relacionamentos
    patrimony = relationship("Patrimony", back_populates="history")
