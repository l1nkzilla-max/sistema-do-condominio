"""
Modelos de dados do Auth & User Service
"""
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Group(Base):
    """Modelo de Grupo de Usuários"""
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    users = relationship("User", back_populates="group")
    permissions = relationship("Permission", back_populates="group", cascade="all, delete-orphan")


class User(Base):
    """Modelo de Usuário"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relacionamentos
    group = relationship("Group", back_populates="users")
    residents = relationship("Resident", back_populates="user", cascade="all, delete-orphan")


class Function(Base):
    """Modelo de Função/Tela do Sistema"""
    __tablename__ = "functions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    module = Column(String(50), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    permissions = relationship("Permission", back_populates="function", cascade="all, delete-orphan")


class Permission(Base):
    """Modelo de Permissão"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    function_id = Column(Integer, ForeignKey("functions.id"), nullable=False, index=True)
    action = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    group = relationship("Group", back_populates="permissions")
    function = relationship("Function", back_populates="permissions")


class Condominium(Base):
    """Modelo de Condomínio"""
    __tablename__ = "condominiums"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    cnpj = Column(String(18), unique=True, index=True)
    address = Column(Text, nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    smtp_host = Column(String(255))
    smtp_port = Column(Integer)
    smtp_user = Column(String(255))
    smtp_password = Column(String(255))
    smtp_use_tls = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    units = relationship("Unit", back_populates="condominium", cascade="all, delete-orphan")


class Unit(Base):
    """Modelo de Unidade/Apartamento"""
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    condominium_id = Column(Integer, ForeignKey("condominiums.id"), nullable=False, index=True)
    block = Column(String(10))
    number = Column(String(10), nullable=False)
    floor = Column(Integer)
    type = Column(String(50))
    area = Column(DECIMAL(10, 2))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    condominium = relationship("Condominium", back_populates="units")
    residents = relationship("Resident", back_populates="unit", cascade="all, delete-orphan")


class Resident(Base):
    """Modelo de Morador (vínculo usuário-unidade)"""
    __tablename__ = "residents"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
    relationship = Column(String(50), nullable=False)
    is_owner = Column(Boolean, default=False)
    is_primary = Column(Boolean, default=False)
    move_in_date = Column(Date)
    move_out_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="residents")
    unit = relationship("Unit", back_populates="residents")
