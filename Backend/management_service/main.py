"""
Management Service - Microserviço de Gerenciamento
Sistema de Condomínio
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field
from datetime import date, datetime

from config import settings
from database import get_db, engine, Base
from models import Provider, Employee, EmployeeHistory, Patrimony, PatrimonyHistory

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(
    title="Management Service",
    description="Microserviço de Gerenciamento - Sistema de Condomínio",
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

class ProviderCreate(BaseModel):
    name: str
    cnpj_cpf: str = None
    service_type: str
    phone: str = None
    email: str = None
    address: str = None
    contact_person: str = None
    notes: str = None

class EmployeeCreate(BaseModel):
    name: str
    cpf: str
    role: str
    phone: str = None
    email: str = None
    address: str = None
    hire_date: date
    salary: float = None

class PatrimonyCreate(BaseModel):
    name: str
    description: str = None
    category: str
    location: str = None
    acquisition_date: date = None
    acquisition_value: float = None
    current_value: float = None
    condition: str = None
    serial_number: str = None
    notes: str = None

# ========== Rotas de Prestadores ==========

@app.get("/api/providers", tags=["Prestadores"])
async def list_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar prestadores"""
    providers = db.query(Provider).offset(skip).limit(limit).all()
    return providers

@app.post("/api/providers", status_code=201, tags=["Prestadores"])
async def create_provider(provider_data: ProviderCreate, db: Session = Depends(get_db)):
    """Criar novo prestador"""
    provider = Provider(**provider_data.dict())
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider

@app.get("/api/providers/{provider_id}", tags=["Prestadores"])
async def get_provider(provider_id: int, db: Session = Depends(get_db)):
    """Obter prestador por ID"""
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador não encontrado")
    return provider

@app.delete("/api/providers/{provider_id}", tags=["Prestadores"])
async def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    """Excluir prestador"""
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador não encontrado")
    db.delete(provider)
    db.commit()
    return {"message": "Prestador excluído com sucesso"}

# ========== Rotas de Funcionários ==========

@app.get("/api/employees", tags=["Funcionários"])
async def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar funcionários"""
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees

@app.post("/api/employees", status_code=201, tags=["Funcionários"])
async def create_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):
    """Criar novo funcionário"""
    employee = Employee(**employee_data.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@app.get("/api/employees/{employee_id}", tags=["Funcionários"])
async def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Obter funcionário por ID"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee

@app.get("/api/employees/{employee_id}/history", tags=["Funcionários"])
async def get_employee_history(employee_id: int, db: Session = Depends(get_db)):
    """Obter histórico de funcionário"""
    history = db.query(EmployeeHistory).filter(EmployeeHistory.employee_id == employee_id).all()
    return history

@app.delete("/api/employees/{employee_id}", tags=["Funcionários"])
async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Excluir funcionário"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    db.delete(employee)
    db.commit()
    return {"message": "Funcionário excluído com sucesso"}

# ========== Rotas de Patrimônio ==========

@app.get("/api/patrimony", tags=["Patrimônio"])
async def list_patrimony(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar patrimônio"""
    patrimonies = db.query(Patrimony).offset(skip).limit(limit).all()
    return patrimonies

@app.post("/api/patrimony", status_code=201, tags=["Patrimônio"])
async def create_patrimony(patrimony_data: PatrimonyCreate, db: Session = Depends(get_db)):
    """Criar novo patrimônio"""
    patrimony = Patrimony(**patrimony_data.dict())
    db.add(patrimony)
    db.commit()
    db.refresh(patrimony)
    return patrimony

@app.get("/api/patrimony/{patrimony_id}", tags=["Patrimônio"])
async def get_patrimony(patrimony_id: int, db: Session = Depends(get_db)):
    """Obter patrimônio por ID"""
    patrimony = db.query(Patrimony).filter(Patrimony.id == patrimony_id).first()
    if not patrimony:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return patrimony

@app.get("/api/patrimony/{patrimony_id}/history", tags=["Patrimônio"])
async def get_patrimony_history(patrimony_id: int, db: Session = Depends(get_db)):
    """Obter histórico de patrimônio"""
    history = db.query(PatrimonyHistory).filter(PatrimonyHistory.patrimony_id == patrimony_id).all()
    return history

@app.delete("/api/patrimony/{patrimony_id}", tags=["Patrimônio"])
async def delete_patrimony(patrimony_id: int, db: Session = Depends(get_db)):
    """Excluir patrimônio"""
    patrimony = db.query(Patrimony).filter(Patrimony.id == patrimony_id).first()
    if not patrimony:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    db.delete(patrimony)
    db.commit()
    return {"message": "Patrimônio excluído com sucesso"}

# ========== Health Check ==========

@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verificação de saúde do serviço"""
    return {"status": "healthy", "service": "management_service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=settings.API_RELOAD)
