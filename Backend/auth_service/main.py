"""
Auth & User Service - Microserviço de Autenticação e Usuários
Sistema de Condomínio
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from config import settings
from database import get_db, engine, Base
from models import User, Group, Function, Permission, Condominium, Unit, Resident
from schemas import (
    Token, LoginRequest, UserCreate, UserUpdate, UserResponse,
    GroupCreate, GroupUpdate, GroupResponse,
    FunctionCreate, FunctionUpdate, FunctionResponse,
    PermissionCreate, PermissionResponse,
    CondominiumCreate, CondominiumUpdate, CondominiumResponse,
    UnitCreate, UnitUpdate, UnitResponse,
    ResidentCreate, ResidentUpdate, ResidentResponse,
    SuccessResponse
)
from auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash, check_permission
)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(
    title="Auth & User Service",
    description="Microserviço de Autenticação e Gerenciamento de Usuários - Sistema de Condomínio",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== Rotas de Autenticação ==========

@app.post("/api/auth/login", response_model=Token, tags=["Autenticação"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login de usuário"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Atualizar último login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Criar token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "group_id": user.group_id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=UserResponse, tags=["Autenticação"])
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Obtém dados do usuário autenticado"""
    return current_user


@app.post("/api/auth/logout", response_model=SuccessResponse, tags=["Autenticação"])
async def logout(current_user: User = Depends(get_current_active_user)):
    """Logout de usuário"""
    return SuccessResponse(message="Logout realizado com sucesso")


# ========== Rotas de Usuários ==========

@app.get("/api/users", response_model=List[UserResponse], tags=["Usuários"])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar usuários"""
    if not check_permission(current_user, "users.list", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["Usuários"])
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obter usuário por ID"""
    if not check_permission(current_user, "users.list", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@app.post("/api/users", response_model=UserResponse, status_code=201, tags=["Usuários"])
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar novo usuário"""
    if not check_permission(current_user, "users.create", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    # Verificar se username já existe
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username já cadastrado")
    
    # Verificar se email já existe
    if user_data.email and db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar usuário
    user = User(
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        email=user_data.email,
        full_name=user_data.full_name,
        phone=user_data.phone,
        group_id=user_data.group_id,
        is_active=user_data.is_active
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.put("/api/users/{user_id}", response_model=UserResponse, tags=["Usuários"])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualizar usuário"""
    if not check_permission(current_user, "users.update", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualizar campos
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@app.delete("/api/users/{user_id}", response_model=SuccessResponse, tags=["Usuários"])
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Excluir usuário"""
    if not check_permission(current_user, "users.delete", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(user)
    db.commit()
    return SuccessResponse(message="Usuário excluído com sucesso")


# ========== Rotas de Grupos ==========

@app.get("/api/groups", response_model=List[GroupResponse], tags=["Grupos"])
async def list_groups(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar grupos"""
    if not check_permission(current_user, "groups.list", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    groups = db.query(Group).offset(skip).limit(limit).all()
    return groups


@app.post("/api/groups", response_model=GroupResponse, status_code=201, tags=["Grupos"])
async def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar novo grupo"""
    if not check_permission(current_user, "groups.list", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    group = Group(**group_data.dict())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


# ========== Rotas de Funções ==========

@app.get("/api/functions", response_model=List[FunctionResponse], tags=["Funções"])
async def list_functions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar funções"""
    functions = db.query(Function).offset(skip).limit(limit).all()
    return functions


@app.post("/api/functions", response_model=FunctionResponse, status_code=201, tags=["Funções"])
async def create_function(
    function_data: FunctionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar nova função"""
    function = Function(**function_data.dict())
    db.add(function)
    db.commit()
    db.refresh(function)
    return function


# ========== Rotas de Permissões ==========

@app.get("/api/permissions", response_model=List[PermissionResponse], tags=["Permissões"])
async def list_permissions(
    group_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar permissões"""
    if not check_permission(current_user, "permissions.manage", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    query = db.query(Permission)
    if group_id:
        query = query.filter(Permission.group_id == group_id)
    
    permissions = query.all()
    return permissions


@app.post("/api/permissions", response_model=PermissionResponse, status_code=201, tags=["Permissões"])
async def create_permission(
    permission_data: PermissionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar nova permissão"""
    if not check_permission(current_user, "permissions.manage", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    permission = Permission(**permission_data.dict())
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


@app.delete("/api/permissions/{permission_id}", response_model=SuccessResponse, tags=["Permissões"])
async def delete_permission(
    permission_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Excluir permissão"""
    if not check_permission(current_user, "permissions.manage", "execute", db):
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
    
    db.delete(permission)
    db.commit()
    return SuccessResponse(message="Permissão excluída com sucesso")


# ========== Rotas de Condomínios ==========

@app.get("/api/condominiums", response_model=List[CondominiumResponse], tags=["Condomínios"])
async def list_condominiums(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar condomínios"""
    condominiums = db.query(Condominium).offset(skip).limit(limit).all()
    return condominiums


@app.post("/api/condominiums", response_model=CondominiumResponse, status_code=201, tags=["Condomínios"])
async def create_condominium(
    condominium_data: CondominiumCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar novo condomínio"""
    condominium = Condominium(**condominium_data.dict())
    db.add(condominium)
    db.commit()
    db.refresh(condominium)
    return condominium


# ========== Rotas de Unidades ==========

@app.get("/api/units", response_model=List[UnitResponse], tags=["Unidades"])
async def list_units(
    condominium_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar unidades"""
    query = db.query(Unit)
    if condominium_id:
        query = query.filter(Unit.condominium_id == condominium_id)
    
    units = query.offset(skip).limit(limit).all()
    return units


@app.post("/api/units", response_model=UnitResponse, status_code=201, tags=["Unidades"])
async def create_unit(
    unit_data: UnitCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar nova unidade"""
    unit = Unit(**unit_data.dict())
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


# ========== Rotas de Moradores ==========

@app.get("/api/residents", response_model=List[ResidentResponse], tags=["Moradores"])
async def list_residents(
    unit_id: int = None,
    user_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar moradores"""
    query = db.query(Resident)
    if unit_id:
        query = query.filter(Resident.unit_id == unit_id)
    if user_id:
        query = query.filter(Resident.user_id == user_id)
    
    residents = query.offset(skip).limit(limit).all()
    return residents


@app.post("/api/residents", response_model=ResidentResponse, status_code=201, tags=["Moradores"])
async def create_resident(
    resident_data: ResidentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar novo morador"""
    resident = Resident(**resident_data.dict())
    db.add(resident)
    db.commit()
    db.refresh(resident)
    return resident


# ========== Health Check ==========

@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verificação de saúde do serviço"""
    return {"status": "healthy", "service": "auth_service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
