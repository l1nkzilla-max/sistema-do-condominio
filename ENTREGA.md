# Entrega - Sistema de Condomínio

## Informações do Projeto

**Disciplina:** Sistemas Distribuídos - P2  
**Data de Entrega:** 26/11/2025 às 21:30  
**Repositório GitHub:** https://github.com/vinicius007/condominium_system

## Estrutura do Projeto

O projeto está organizado conforme especificado:

```
condominium_system/
├── Backend/                    # Projeto back-end (3 microserviços)
│   ├── auth_service/          # Microserviço 1: Autenticação e Usuários
│   ├── management_service/    # Microserviço 2: Gerenciamento
│   └── operations_service/    # Microserviço 3: Operações
│
├── client/                     # Projeto front-end (React)
│
├── Script/                     # Banco de dados (Scripts SQL)
│   ├── 01_create_auth_tables.sql
│   ├── 02_create_management_tables.sql
│   └── 03_create_operations_tables.sql
│
└── docs/                       # Documentação
    ├── architecture.md         # Documentação de arquitetura
    ├── data_models.md         # Documentação de modelos de dados
    └── api_documentation.md   # Documentação de APIs e funções
```

## Componentes Entregues

### 1. Projeto Back-end ✅

**3 Microserviços Python/FastAPI:**

- **Auth & User Service** (Porta 8001)
  - Autenticação JWT
  - Gerenciamento de usuários
  - Controle de grupos e permissões
  - Gerenciamento de condomínios e unidades

- **Management Service** (Porta 8002)
  - Cadastro de prestadores de serviço
  - Gerenciamento de funcionários com histórico
  - Controle de patrimônio com histórico

- **Operations Service** (Porta 8003)
  - Agendamento de áreas comuns
  - Orçamentos de compra e serviço
  - Eventos e reuniões
  - Atas de reunião
  - Documentos
  - Controle de visitantes
  - Sistema de avisos
  - Logs e auditoria

### 2. Projeto Front-end ✅

- Framework: React 19 + TypeScript
- Build Tool: Vite
- Estilização: Tailwind CSS
- Estrutura base pronta para consumo das APIs

### 3. Banco de Dados ✅

- **PostgreSQL** (compatível com MySQL/MariaDB)
- 3 Scripts SQL completos:
  - `01_create_auth_tables.sql` - Tabelas de autenticação
  - `02_create_management_tables.sql` - Tabelas de gerenciamento
  - `03_create_operations_tables.sql` - Tabelas de operações
- Dados iniciais (seed data) incluídos

### 4. Documentação ✅

- **README.md** - Instruções completas de instalação e uso
- **INSTRUCOES_EXECUCAO.md** - Guia passo a passo para executar o projeto
- **docs/architecture.md** - Documentação de arquitetura de microserviços
- **docs/data_models.md** - Documentação de modelos de dados
- **docs/api_documentation.md** - Documentação completa de APIs e funções

## Tecnologias Utilizadas

### Backend
- Python 3.11+
- FastAPI (Framework web)
- SQLAlchemy (ORM)
- Pydantic (Validação)
- PyJWT (Autenticação)
- Bcrypt (Segurança)
- Uvicorn (Servidor ASGI)

### Frontend
- React 19
- TypeScript
- Vite
- Tailwind CSS

### Banco de Dados
- PostgreSQL 14+ (ou MySQL/MariaDB)

## Como Executar

### Pré-requisitos
- Python 3.11+
- PostgreSQL 14+ (ou MySQL/MariaDB)
- Node.js 18+

### Passo 1: Banco de Dados
```bash
psql -U postgres
\i Script/01_create_auth_tables.sql
\i Script/02_create_management_tables.sql
\i Script/03_create_operations_tables.sql
```

### Passo 2: Backend (3 terminais)

**Terminal 1 - Auth Service:**
```bash
cd Backend/auth_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Management Service:**
```bash
cd Backend/management_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Terminal 3 - Operations Service:**
```bash
cd Backend/operations_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Passo 3: Frontend (opcional)
```bash
cd client
npm install
npm run dev
```

## Testando as APIs

### Documentação Swagger (Interativa)

- Auth Service: http://localhost:8001/api/docs
- Management Service: http://localhost:8002/api/docs
- Operations Service: http://localhost:8003/api/docs

### Exemplo de Uso via cURL

```bash
# 1. Login
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 2. Listar usuários (usar token obtido)
curl -X GET "http://localhost:8001/api/users" \
  -H "Authorization: Bearer <TOKEN>"

# 3. Criar agendamento
curl -X POST "http://localhost:8003/api/schedulings" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "area_id": 1,
    "unit_id": 1,
    "user_id": 1,
    "start_datetime": "2025-12-15T14:00:00",
    "end_datetime": "2025-12-15T18:00:00",
    "purpose": "Festa de aniversário"
  }'
```

### Teste via Postman

1. Importar coleção (opcional)
2. Fazer login em `/api/auth/login`
3. Copiar o `access_token`
4. Adicionar header: `Authorization: Bearer <token>`
5. Testar todas as rotas

## Arquitetura

### Padrão MVC

Cada microserviço segue o padrão MVC:

- **Models** (`models.py`) - Modelos de dados SQLAlchemy
- **Views** (rotas FastAPI em `main.py`) - Endpoints REST
- **Controllers** (lógica em `main.py` e `auth.py`) - Lógica de negócio

### Comunicação Síncrona

- **HTTP/REST** - Comunicação entre frontend e backend
- **JSON** - Formato de dados
- **JWT** - Autenticação stateless entre serviços

### Microserviços

Cada serviço é independente e pode ser executado separadamente:

- **Banco de dados separado** (ou schemas separados)
- **Porta diferente** (8001, 8002, 8003)
- **Documentação própria** (Swagger/OpenAPI)

## Funcionalidades Implementadas

### Autenticação e Autorização
✅ Login com JWT  
✅ Controle de permissões por grupo  
✅ Gerenciamento de usuários  
✅ Grupos e funções  

### Gerenciamento
✅ Cadastro de prestadores  
✅ Gerenciamento de funcionários  
✅ Controle de patrimônio  
✅ Históricos de alterações  

### Operações
✅ Agendamento de áreas comuns  
✅ Orçamentos com aprovação  
✅ Eventos e reuniões  
✅ Atas de reunião  
✅ Controle de visitantes  
✅ Sistema de avisos  
✅ Logs e auditoria  

## Observações

1. **Usuário padrão:**
   - Username: `admin`
   - Password: `admin123`

2. **Portas utilizadas:**
   - 8001: Auth Service
   - 8002: Management Service
   - 8003: Operations Service
   - 5173: Frontend (opcional)

3. **Banco de dados:**
   - Os scripts SQL criam 3 bancos: `auth_db`, `management_db`, `operations_db`
   - Ou podem usar schemas separados no mesmo banco

4. **Documentação:**
   - Toda a documentação está em `docs/`
   - APIs documentadas com Swagger/OpenAPI
   - README com instruções detalhadas

## Contato

Para dúvidas sobre o projeto, consulte:
- README.md
- INSTRUCOES_EXECUCAO.md
- docs/api_documentation.md

---

**Projeto desenvolvido para a disciplina de Sistemas Distribuídos - P2**  
**Data: 26/11/2025**
