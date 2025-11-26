"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date


# ========== Auth Schemas ==========

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# ========== User Schemas ==========

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    group_id: int
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    group_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ========== Group Schemas ==========

class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class GroupResponse(GroupBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========== Function Schemas ==========

class FunctionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    module: str = Field(..., min_length=1, max_length=50)
    is_active: bool = True


class FunctionCreate(FunctionBase):
    pass


class FunctionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class FunctionResponse(FunctionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Permission Schemas ==========

class PermissionBase(BaseModel):
    group_id: int
    function_id: int
    action: str = Field(..., min_length=1, max_length=20)


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Condominium Schemas ==========

class CondominiumBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    cnpj: Optional[str] = Field(None, max_length=18)
    address: str
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    smtp_host: Optional[str] = Field(None, max_length=255)
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = Field(None, max_length=255)
    smtp_password: Optional[str] = Field(None, max_length=255)
    smtp_use_tls: bool = True


class CondominiumCreate(CondominiumBase):
    pass


class CondominiumUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    cnpj: Optional[str] = Field(None, max_length=18)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    smtp_host: Optional[str] = Field(None, max_length=255)
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = Field(None, max_length=255)
    smtp_password: Optional[str] = Field(None, max_length=255)
    smtp_use_tls: Optional[bool] = None


class CondominiumResponse(CondominiumBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========== Unit Schemas ==========

class UnitBase(BaseModel):
    condominium_id: int
    block: Optional[str] = Field(None, max_length=10)
    number: str = Field(..., max_length=10)
    floor: Optional[int] = None
    type: Optional[str] = Field(None, max_length=50)
    area: Optional[float] = None
    is_active: bool = True


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseModel):
    block: Optional[str] = Field(None, max_length=10)
    number: Optional[str] = Field(None, max_length=10)
    floor: Optional[int] = None
    type: Optional[str] = Field(None, max_length=50)
    area: Optional[float] = None
    is_active: Optional[bool] = None


class UnitResponse(UnitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========== Resident Schemas ==========

class ResidentBase(BaseModel):
    user_id: int
    unit_id: int
    relationship: str = Field(..., max_length=50)
    is_owner: bool = False
    is_primary: bool = False
    move_in_date: Optional[date] = None
    move_out_date: Optional[date] = None


class ResidentCreate(ResidentBase):
    pass


class ResidentUpdate(BaseModel):
    relationship: Optional[str] = Field(None, max_length=50)
    is_owner: Optional[bool] = None
    is_primary: Optional[bool] = None
    move_in_date: Optional[date] = None
    move_out_date: Optional[date] = None


class ResidentResponse(ResidentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Response Wrappers ==========

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: dict
