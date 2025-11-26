# Sistema de Condomínio

Sistema completo de gerenciamento de condomínios desenvolvido com **arquitetura de microserviços**, utilizando **Python (FastAPI)** para o backend, **PostgreSQL** como banco de dados e **React** para o frontend.

## 📋 Descrição do Projeto

Este sistema foi desenvolvido como parte da disciplina de Sistemas Distribuídos e implementa uma solução completa para gerenciamento de condomínios, incluindo:

- **Autenticação e Autorização** de usuários
- **Gerenciamento de Moradores e Unidades**
- **Controle de Permissões** baseado em grupos
- **Agendamento de Áreas Comuns**
- **Gestão de Orçamentos** (compras e serviços)
- **Controle de Prestadores e Funcionários**
- **Gerenciamento de Patrimônio**
- **Sistema de Avisos e Notificações**
- **Controle de Visitantes**
- **Eventos e Reuniões**
- **Atas de Reunião**
- **Auditoria e Logs** de todas as ações

## 🏗️ Arquitetura

O sistema utiliza uma **arquitetura de microserviços** com três serviços independentes:

### 1. Auth & User Service (Porta 8001)
- Autenticação e autorização (JWT)
- Gerenciamento de usuários
- Controle de grupos e permissões
- Gerenciamento de condomínios e unidades

### 2. Management Service (Porta 8002)
- Cadastro de prestadores de serviço
- Gerenciamento de funcionários
- Controle de patrimônio
- Históricos de alterações

### 3. Operations Service (Porta 8003)
- Agendamento de áreas comuns
- Orçamentos de compra e serviço
- Eventos e reuniões
- Atas de reunião
- Documentos
- Controle de visitantes
- Sistema de avisos
- Logs e auditoria

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **PyJWT** - Autenticação JWT
- **Bcrypt** - Hash de senhas
- **Uvicorn** - Servidor ASGI

### Frontend
- **React 19**
- **TypeScript**
- **Vite** - Build tool
- **Tailwind CSS** - Framework CSS
- **Axios** - Cliente HTTP

### Banco de Dados
- **PostgreSQL 14+** (ou MySQL/MariaDB)

## 📁 Estrutura do Projeto

```
condominium_system/
├── Backend/
│   ├── auth_service/          # Microserviço de Autenticação
│   │   ├── main.py           # Aplicação principal
│   │   ├── models.py         # Modelos de dados
│   │   ├── schemas.py        # Schemas Pydantic
│   │   ├── auth.py           # Funções de autenticação
│   │   ├── database.py       # Configuração do banco
│   │   ├── config.py         # Configurações
│   │   └── requirements.txt  # Dependências
│   │
│   ├── management_service/    # Microserviço de Gerenciamento
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── config.py
│   │   └── requirements.txt
│   │
│   └── operations_service/    # Microserviço de Operações
│       ├── main.py
│       ├── models.py
│       ├── database.py
│       ├── config.py
│       └── requirements.txt
│
├── Script/                    # Scripts SQL
│   ├── 01_create_auth_tables.sql
│   ├── 02_create_management_tables.sql
│   └── 03_create_operations_tables.sql
│
├── client/                    # Frontend React
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docs/                      # Documentação
│   ├── architecture.md
│   └── data_models.md
│
└── README.md
```

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- Node.js 18 ou superior
- PostgreSQL 14 ou superior (ou MySQL/MariaDB)
- Git

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd condominium_system
```

### 2. Configurar Banco de Dados

Execute os scripts SQL na ordem:

```bash
# Conectar ao PostgreSQL
psql -U postgres

# Executar scripts
\i Script/01_create_auth_tables.sql
\i Script/02_create_management_tables.sql
\i Script/03_create_operations_tables.sql
```

### 3. Configurar Backend

#### Auth Service

```bash
cd Backend/auth_service

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (criar arquivo .env)
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/auth_db
SECRET_KEY=sua-chave-secreta-aqui
API_PORT=8001

# Executar serviço
python main.py
```

#### Management Service

```bash
cd Backend/management_service

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/management_db
API_PORT=8002

# Executar serviço
python main.py
```

#### Operations Service

```bash
cd Backend/operations_service

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/operations_db
API_PORT=8003

# Executar serviço
python main.py
```

### 4. Configurar Frontend

```bash
cd client

# Instalar dependências
pnpm install
# ou
npm install

# Executar em modo desenvolvimento
pnpm dev
# ou
npm run dev
```

## 📖 Documentação da API

Cada microserviço possui documentação interativa Swagger/OpenAPI:

- **Auth Service**: http://localhost:8001/api/docs
- **Management Service**: http://localhost:8002/api/docs
- **Operations Service**: http://localhost:8003/api/docs

## 🔐 Autenticação

O sistema utiliza **JWT (JSON Web Tokens)** para autenticação.

### Login

```bash
POST http://localhost:8001/api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

### Resposta

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usar Token

Incluir o token no header de todas as requisições:

```
Authorization: Bearer <token>
```

## 👥 Usuários Padrão

O sistema vem com os seguintes usuários pré-cadastrados:

| Usuário | Senha | Grupo | Descrição |
|---------|-------|-------|-----------|
| admin | admin123 | Administrador | Acesso total ao sistema |

## 📊 Grupos e Permissões

O sistema possui os seguintes grupos padrão:

1. **Administrador** - Acesso total
2. **Síndico** - Gerenciamento do condomínio
3. **Morador** - Acesso básico (agendamentos, avisos)
4. **Porteiro** - Controle de visitantes
5. **Zelador** - Manutenção e limpeza

## 🧪 Testando as APIs

### Exemplo: Listar Usuários

```bash
curl -X GET "http://localhost:8001/api/users" \
  -H "Authorization: Bearer <seu_token>"
```

### Exemplo: Criar Agendamento

```bash
curl -X POST "http://localhost:8003/api/schedulings" \
  -H "Authorization: Bearer <seu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "area_id": 1,
    "unit_id": 1,
    "user_id": 1,
    "start_datetime": "2025-12-01T14:00:00",
    "end_datetime": "2025-12-01T18:00:00",
    "purpose": "Festa de aniversário"
  }'
```

## 📝 Funcionalidades Principais

### Gerenciamento de Usuários
- ✅ Cadastro de usuários
- ✅ Autenticação JWT
- ✅ Controle de permissões por grupo
- ✅ Vínculo de moradores a unidades

### Agendamentos
- ✅ Reserva de áreas comuns
- ✅ Aprovação de agendamentos
- ✅ Controle de disponibilidade

### Orçamentos
- ✅ Orçamentos de compra
- ✅ Orçamentos de serviço
- ✅ Histórico de alterações
- ✅ Aprovação de orçamentos

### Avisos
- ✅ Publicação de avisos
- ✅ Quadro de avisos
- ✅ Priorização de avisos
- ✅ Expiração automática

### Auditoria
- ✅ Logs de todas as ações
- ✅ Rastreamento de alterações
- ✅ Relatórios de auditoria

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

Cada microserviço pode ser configurado através de variáveis de ambiente:

```env
# Banco de Dados
DATABASE_URL=mysql+pymysql://user:password@host:port/database

# JWT
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_HOST=0.0.0.0
API_PORT=8001
API_RELOAD=True

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🐳 Docker (Opcional)

Para executar com Docker Compose:

```bash
# TODO: Criar docker-compose.yml
docker-compose up -d
```

## 📚 Documentação Adicional

- [Arquitetura do Sistema](docs/architecture.md)
- [Modelos de Dados](docs/data_models.md)

## 🤝 Contribuindo

Este é um projeto acadêmico desenvolvido para a disciplina de Sistemas Distribuídos.

## 📄 Licença

Este projeto é de uso acadêmico.

## 👨‍💻 Autor

Desenvolvido para a disciplina de Sistemas Distribuídos - P2

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação ou entre em contato através do GitHub.

---

**Data de Entrega**: 26/11/2025 às 21:30
