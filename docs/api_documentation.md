# Documentação de APIs - Sistema de Condomínio

## 1. Introdução

Este documento apresenta a documentação completa das APIs REST dos três microserviços que compõem o Sistema de Condomínio. Todas as APIs seguem os padrões RESTful e utilizam JSON como formato de dados.

## 2. Informações Gerais

### 2.1. URLs Base

| Microserviço | URL Base | Porta |
|--------------|----------|-------|
| Auth & User Service | http://localhost:8001 | 8001 |
| Management Service | http://localhost:8002 | 8002 |
| Operations Service | http://localhost:8003 | 8003 |

### 2.2. Autenticação

Todas as rotas protegidas requerem autenticação via **JWT (JSON Web Token)**. O token deve ser incluído no header de todas as requisições:

```
Authorization: Bearer <token>
```

### 2.3. Formato de Resposta

**Sucesso:**
```json
{
  "id": 1,
  "field": "value",
  ...
}
```

**Erro:**
```json
{
  "detail": "Mensagem de erro"
}
```

### 2.4. Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Não autenticado |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Recurso não encontrado |
| 500 | Internal Server Error - Erro no servidor |

## 3. Auth & User Service (Porta 8001)

### 3.1. Autenticação

#### POST /api/auth/login

Realiza login e retorna token JWT.

**Request:**
```http
POST /api/auth/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erros:**
- 401: Credenciais inválidas

---

#### GET /api/auth/me

Retorna dados do usuário autenticado.

**Request:**
```http
GET /api/auth/me HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@condominio.com",
  "full_name": "Administrador do Sistema",
  "phone": null,
  "group_id": 1,
  "is_active": true,
  "created_at": "2025-11-26T10:00:00Z",
  "updated_at": "2025-11-26T10:00:00Z",
  "last_login": "2025-11-26T17:30:00Z"
}
```

---

#### POST /api/auth/logout

Realiza logout do usuário.

**Request:**
```http
POST /api/auth/logout HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Logout realizado com sucesso"
}
```

### 3.2. Usuários

#### GET /api/users

Lista todos os usuários (paginado).

**Permissão:** `users.list`

**Parâmetros de Query:**
- `skip` (int, opcional): Número de registros a pular (padrão: 0)
- `limit` (int, opcional): Número máximo de registros (padrão: 100)

**Request:**
```http
GET /api/users?skip=0&limit=10 HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@condominio.com",
    "full_name": "Administrador do Sistema",
    "phone": null,
    "group_id": 1,
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z",
    "last_login": "2025-11-26T17:30:00Z"
  }
]
```

---

#### GET /api/users/{user_id}

Obtém um usuário específico por ID.

**Permissão:** `users.list`

**Request:**
```http
GET /api/users/1 HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@condominio.com",
  "full_name": "Administrador do Sistema",
  "phone": null,
  "group_id": 1,
  "is_active": true,
  "created_at": "2025-11-26T10:00:00Z",
  "updated_at": "2025-11-26T10:00:00Z",
  "last_login": "2025-11-26T17:30:00Z"
}
```

**Erros:**
- 404: Usuário não encontrado

---

#### POST /api/users

Cria um novo usuário.

**Permissão:** `users.create`

**Request:**
```http
POST /api/users HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "joao.silva",
  "password": "senha123",
  "email": "joao.silva@email.com",
  "full_name": "João Silva",
  "phone": "(11) 98765-4321",
  "group_id": 3,
  "is_active": true
}
```

**Response (201):**
```json
{
  "id": 2,
  "username": "joao.silva",
  "email": "joao.silva@email.com",
  "full_name": "João Silva",
  "phone": "(11) 98765-4321",
  "group_id": 3,
  "is_active": true,
  "created_at": "2025-11-26T18:00:00Z",
  "updated_at": "2025-11-26T18:00:00Z",
  "last_login": null
}
```

**Erros:**
- 400: Username ou email já cadastrado

---

#### PUT /api/users/{user_id}

Atualiza um usuário existente.

**Permissão:** `users.update`

**Request:**
```http
PUT /api/users/2 HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "novo.email@email.com",
  "phone": "(11) 91111-2222"
}
```

**Response (200):**
```json
{
  "id": 2,
  "username": "joao.silva",
  "email": "novo.email@email.com",
  "full_name": "João Silva",
  "phone": "(11) 91111-2222",
  "group_id": 3,
  "is_active": true,
  "created_at": "2025-11-26T18:00:00Z",
  "updated_at": "2025-11-26T18:15:00Z",
  "last_login": null
}
```

---

#### DELETE /api/users/{user_id}

Exclui um usuário.

**Permissão:** `users.delete`

**Request:**
```http
DELETE /api/users/2 HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Usuário excluído com sucesso"
}
```

### 3.3. Grupos

#### GET /api/groups

Lista todos os grupos.

**Permissão:** `groups.list`

**Request:**
```http
GET /api/groups HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Administrador",
    "description": "Acesso total ao sistema",
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

---

#### POST /api/groups

Cria um novo grupo.

**Permissão:** `groups.list`

**Request:**
```http
POST /api/groups HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Conselheiro",
  "description": "Membros do conselho do condomínio",
  "is_active": true
}
```

**Response (201):**
```json
{
  "id": 6,
  "name": "Conselheiro",
  "description": "Membros do conselho do condomínio",
  "is_active": true,
  "created_at": "2025-11-26T18:30:00Z",
  "updated_at": "2025-11-26T18:30:00Z"
}
```

### 3.4. Funções

#### GET /api/functions

Lista todas as funções do sistema.

**Request:**
```http
GET /api/functions HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Listar Usuários",
    "code": "users.list",
    "description": "Visualizar lista de usuários",
    "module": "auth",
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z"
  }
]
```

### 3.5. Permissões

#### GET /api/permissions

Lista permissões (opcionalmente filtradas por grupo).

**Permissão:** `permissions.manage`

**Parâmetros de Query:**
- `group_id` (int, opcional): Filtrar por grupo

**Request:**
```http
GET /api/permissions?group_id=3 HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "group_id": 3,
    "function_id": 13,
    "action": "execute",
    "created_at": "2025-11-26T10:00:00Z"
  }
]
```

---

#### POST /api/permissions

Cria uma nova permissão.

**Permissão:** `permissions.manage`

**Request:**
```http
POST /api/permissions HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "group_id": 6,
  "function_id": 1,
  "action": "execute"
}
```

**Response (201):**
```json
{
  "id": 50,
  "group_id": 6,
  "function_id": 1,
  "action": "execute",
  "created_at": "2025-11-26T19:00:00Z"
}
```

### 3.6. Condomínios

#### GET /api/condominiums

Lista todos os condomínios.

**Request:**
```http
GET /api/condominiums HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Condomínio Exemplo",
    "cnpj": "12.345.678/0001-90",
    "address": "Rua Exemplo, 123 - Bairro - Cidade/UF",
    "phone": "(11) 1234-5678",
    "email": "contato@condominioexemplo.com",
    "smtp_host": null,
    "smtp_port": null,
    "smtp_user": null,
    "smtp_password": null,
    "smtp_use_tls": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

### 3.7. Unidades

#### GET /api/units

Lista unidades (opcionalmente filtradas por condomínio).

**Parâmetros de Query:**
- `condominium_id` (int, opcional): Filtrar por condomínio

**Request:**
```http
GET /api/units?condominium_id=1 HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "condominium_id": 1,
    "block": "A",
    "number": "101",
    "floor": 1,
    "type": "Apartamento",
    "area": 75.50,
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

## 4. Management Service (Porta 8002)

### 4.1. Prestadores

#### GET /api/providers

Lista todos os prestadores.

**Request:**
```http
GET /api/providers HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Empresa de Limpeza ABC",
    "cnpj_cpf": "12.345.678/0001-90",
    "service_type": "Limpeza",
    "phone": "(11) 1111-1111",
    "email": "contato@limpezaabc.com",
    "address": null,
    "contact_person": "João Silva",
    "notes": null,
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

---

#### POST /api/providers

Cria um novo prestador.

**Request:**
```http
POST /api/providers HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Elétrica Rápida",
  "cnpj_cpf": "99.888.777/0001-66",
  "service_type": "Elétrica",
  "phone": "(11) 5555-5555",
  "email": "contato@eletricarapida.com",
  "contact_person": "Carlos Eletricista"
}
```

**Response (201):**
```json
{
  "id": 5,
  "name": "Elétrica Rápida",
  "cnpj_cpf": "99.888.777/0001-66",
  "service_type": "Elétrica",
  "phone": "(11) 5555-5555",
  "email": "contato@eletricarapida.com",
  "address": null,
  "contact_person": "Carlos Eletricista",
  "notes": null,
  "is_active": true,
  "created_at": "2025-11-26T19:30:00Z",
  "updated_at": "2025-11-26T19:30:00Z"
}
```

### 4.2. Funcionários

#### GET /api/employees

Lista todos os funcionários.

**Request:**
```http
GET /api/employees HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Carlos Souza",
    "cpf": "123.456.789-00",
    "role": "Porteiro",
    "phone": "(11) 91111-1111",
    "email": null,
    "address": null,
    "hire_date": "2023-01-15",
    "termination_date": null,
    "salary": 2500.00,
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

---

#### GET /api/employees/{employee_id}/history

Obtém histórico de alterações de um funcionário.

**Request:**
```http
GET /api/employees/1/history HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "employee_id": 1,
    "field_name": "salary",
    "old_value": "2300.00",
    "new_value": "2500.00",
    "changed_by": 1,
    "changed_at": "2025-06-01T10:00:00Z"
  }
]
```

### 4.3. Patrimônio

#### GET /api/patrimony

Lista todo o patrimônio.

**Request:**
```http
GET /api/patrimony HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Cortador de Grama Elétrico",
    "description": "Cortador de grama marca XYZ, modelo 2023",
    "category": "Equipamento",
    "location": "Área de serviço",
    "acquisition_date": "2023-01-10",
    "acquisition_value": 1500.00,
    "current_value": 1200.00,
    "condition": "Bom",
    "serial_number": null,
    "notes": null,
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

## 5. Operations Service (Porta 8003)

### 5.1. Áreas Comuns

#### GET /api/areas

Lista todas as áreas comuns.

**Request:**
```http
GET /api/areas HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Salão de Festas",
    "description": "Salão de festas com cozinha equipada",
    "capacity": 100,
    "hourly_rate": 150.00,
    "requires_approval": true,
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

### 5.2. Agendamentos

#### GET /api/schedulings

Lista todos os agendamentos.

**Request:**
```http
GET /api/schedulings HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "area_id": 1,
    "unit_id": 1,
    "user_id": 1,
    "start_datetime": "2025-12-15T14:00:00Z",
    "end_datetime": "2025-12-15T18:00:00Z",
    "status": "pending",
    "purpose": "Festa de aniversário",
    "guests_count": 50,
    "approved_by": null,
    "approved_at": null,
    "notes": null,
    "created_at": "2025-11-26T19:00:00Z",
    "updated_at": "2025-11-26T19:00:00Z"
  }
]
```

---

#### POST /api/schedulings

Cria um novo agendamento.

**Request:**
```http
POST /api/schedulings HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "area_id": 1,
  "unit_id": 1,
  "user_id": 1,
  "start_datetime": "2025-12-20T18:00:00",
  "end_datetime": "2025-12-20T22:00:00",
  "purpose": "Confraternização de fim de ano",
  "guests_count": 30
}
```

**Response (201):**
```json
{
  "id": 2,
  "area_id": 1,
  "unit_id": 1,
  "user_id": 1,
  "start_datetime": "2025-12-20T18:00:00Z",
  "end_datetime": "2025-12-20T22:00:00Z",
  "status": "pending",
  "purpose": "Confraternização de fim de ano",
  "guests_count": 30,
  "approved_by": null,
  "approved_at": null,
  "notes": null,
  "created_at": "2025-11-26T20:00:00Z",
  "updated_at": "2025-11-26T20:00:00Z"
}
```

---

#### PUT /api/schedulings/{scheduling_id}/approve

Aprova um agendamento.

**Request:**
```http
PUT /api/schedulings/2/approve?approved_by=1 HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 2,
  "area_id": 1,
  "unit_id": 1,
  "user_id": 1,
  "start_datetime": "2025-12-20T18:00:00Z",
  "end_datetime": "2025-12-20T22:00:00Z",
  "status": "approved",
  "purpose": "Confraternização de fim de ano",
  "guests_count": 30,
  "approved_by": 1,
  "approved_at": "2025-11-26T20:05:00Z",
  "notes": null,
  "created_at": "2025-11-26T20:00:00Z",
  "updated_at": "2025-11-26T20:05:00Z"
}
```

### 5.3. Orçamentos

#### GET /api/budgets

Lista todos os orçamentos.

**Request:**
```http
GET /api/budgets HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "type": "purchase",
    "title": "Compra de Material de Limpeza",
    "description": "Sabão, desinfetante, vassouras",
    "provider_id": 1,
    "amount": 850.00,
    "status": "pending",
    "requested_by": 1,
    "approved_by": null,
    "requested_at": "2025-11-26T15:00:00Z",
    "approved_at": null,
    "notes": null,
    "created_at": "2025-11-26T15:00:00Z",
    "updated_at": "2025-11-26T15:00:00Z"
  }
]
```

---

#### GET /api/budgets/{budget_id}/history

Obtém histórico de um orçamento.

**Request:**
```http
GET /api/budgets/1/history HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "budget_id": 1,
    "old_status": "draft",
    "new_status": "pending",
    "changed_by": 1,
    "comments": "Enviado para aprovação",
    "changed_at": "2025-11-26T15:00:00Z"
  }
]
```

### 5.4. Avisos

#### GET /api/notices

Lista avisos ativos.

**Request:**
```http
GET /api/notices HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Manutenção Programada - Elevadores",
    "content": "Informamos que no dia 30/11/2025 será realizada manutenção preventiva nos elevadores das 8h às 12h.",
    "type": "Manutenção",
    "priority": "high",
    "published_by": 1,
    "published_at": "2025-11-26T10:00:00Z",
    "expires_at": null,
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

---

#### GET /api/notice-board

Obtém quadro de avisos (avisos ativos e não expirados).

**Request:**
```http
GET /api/notice-board HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 4,
    "title": "Assembleia Extraordinária",
    "content": "Fica convocada assembleia extraordinária para o dia 15/12/2025 às 19h no salão de festas.",
    "type": "Assembleia",
    "priority": "urgent",
    "published_by": 1,
    "published_at": "2025-11-26T10:00:00Z",
    "expires_at": "2025-12-15T23:59:59Z",
    "is_active": true,
    "created_at": "2025-11-26T10:00:00Z",
    "updated_at": "2025-11-26T10:00:00Z"
  }
]
```

### 5.5. Auditoria

#### GET /api/logs

Lista logs de auditoria.

**Parâmetros de Query:**
- `skip` (int, opcional): Número de registros a pular
- `limit` (int, opcional): Número máximo de registros

**Request:**
```http
GET /api/logs?skip=0&limit=50 HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "action": "login",
    "entity_type": null,
    "entity_id": null,
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "request_method": "POST",
    "request_path": "/api/auth/login",
    "request_data": null,
    "response_status": 200,
    "created_at": "2025-11-26T17:30:00Z"
  }
]
```

---

#### GET /api/audit

Obtém dados de auditoria com filtros.

**Parâmetros de Query:**
- `user_id` (int, opcional): Filtrar por usuário
- `action` (str, opcional): Filtrar por ação
- `entity_type` (str, opcional): Filtrar por tipo de entidade
- `skip` (int, opcional): Paginação
- `limit` (int, opcional): Limite de registros

**Request:**
```http
GET /api/audit?user_id=1&action=create&limit=20 HTTP/1.1
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 5,
    "user_id": 1,
    "action": "create",
    "entity_type": "scheduling",
    "entity_id": 2,
    "ip_address": "192.168.1.100",
    "user_agent": "PostmanRuntime/7.32.0",
    "request_method": "POST",
    "request_path": "/api/schedulings",
    "request_data": "{\"area_id\":1,\"unit_id\":1,...}",
    "response_status": 201,
    "created_at": "2025-11-26T20:00:00Z"
  }
]
```

## 6. Documentação Interativa

Cada microserviço possui documentação interativa Swagger/OpenAPI acessível através dos seguintes URLs:

- **Auth Service**: http://localhost:8001/api/docs
- **Management Service**: http://localhost:8002/api/docs
- **Operations Service**: http://localhost:8003/api/docs

A documentação Swagger permite:

- Visualizar todos os endpoints disponíveis
- Testar as APIs diretamente no navegador
- Ver exemplos de requisições e respostas
- Autenticar usando o botão "Authorize"
- Exportar a especificação OpenAPI

## 7. Exemplos de Uso Completo

### 7.1. Fluxo de Agendamento de Área Comum

```bash
# 1. Fazer login
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Resposta: { "access_token": "...", "token_type": "bearer" }

# 2. Listar áreas disponíveis
curl -X GET "http://localhost:8003/api/areas" \
  -H "Authorization: Bearer <token>"

# 3. Criar agendamento
curl -X POST "http://localhost:8003/api/schedulings" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "area_id": 1,
    "unit_id": 1,
    "user_id": 1,
    "start_datetime": "2025-12-25T14:00:00",
    "end_datetime": "2025-12-25T18:00:00",
    "purpose": "Festa de Natal",
    "guests_count": 80
  }'

# 4. Aprovar agendamento (como síndico)
curl -X PUT "http://localhost:8003/api/schedulings/1/approve?approved_by=1" \
  -H "Authorization: Bearer <token>"
```

### 7.2. Fluxo de Criação de Orçamento

```bash
# 1. Listar prestadores
curl -X GET "http://localhost:8002/api/providers" \
  -H "Authorization: Bearer <token>"

# 2. Criar orçamento de serviço
curl -X POST "http://localhost:8003/api/budgets" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "service",
    "title": "Manutenção do Elevador",
    "description": "Manutenção preventiva anual",
    "provider_id": 2,
    "amount": 3500.00,
    "requested_by": 1
  }'

# 3. Consultar histórico do orçamento
curl -X GET "http://localhost:8003/api/budgets/1/history" \
  -H "Authorization: Bearer <token>"
```

## 8. Considerações de Segurança

### 8.1. Proteção de Rotas

Todas as rotas (exceto login e health check) requerem autenticação via JWT.

### 8.2. Validação de Permissões

O Auth Service verifica permissões baseadas em grupos antes de permitir ações.

### 8.3. Logs de Auditoria

Todas as ações importantes são registradas no sistema de logs para auditoria.

### 8.4. Senhas

Senhas são armazenadas com hash bcrypt (12 rounds).

## 9. Limitações e Melhorias Futuras

### Limitações Atuais

- Envio de e-mails não implementado (TODO)
- Upload de arquivos não implementado
- Paginação básica (sem cursor-based pagination)
- Sem rate limiting

### Melhorias Futuras

- Implementar WebSockets para notificações em tempo real
- Adicionar cache com Redis
- Implementar busca full-text
- Adicionar filtros avançados em todas as listagens
- Implementar soft delete
- Adicionar versionamento de API

## 10. Conclusão

Este documento apresentou a documentação completa das APIs do Sistema de Condomínio. Para mais informações, consulte a documentação interativa Swagger de cada microserviço ou entre em contato com a equipe de desenvolvimento.
