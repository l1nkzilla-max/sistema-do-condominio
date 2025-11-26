# Arquitetura do Sistema de Condomínio

## 1. Visão Geral

O Sistema de Condomínio foi desenvolvido utilizando uma **arquitetura de microserviços** para garantir escalabilidade, manutenibilidade e separação clara de responsabilidades. A solução é composta por três microserviços backend independentes desenvolvidos em **Python** utilizando o framework **FastAPI**, um banco de dados **PostgreSQL** centralizado, e uma interface web moderna desenvolvida em **React** com **TypeScript**.

## 2. Arquitetura de Microserviços

A arquitetura segue o padrão **MVC** (Model-View-Controller) em cada microserviço, onde os modelos representam as entidades do banco de dados, os controladores (routers) gerenciam a lógica de negócio, e as views são representadas pela interface web que consome as APIs REST.

### 2.1. Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│                    Interface Web do Usuário                  │
└────────────┬────────────────────────────────────────────────┘
             │
             │ HTTP/REST (JSON)
             │
┌────────────┴────────────────────────────────────────────────┐
│                    API Gateway (Nginx)                       │
│              Roteamento e Load Balancing                     │
└────┬──────────────────┬──────────────────┬──────────────────┘
     │                  │                  │
     │                  │                  │
┌────▼──────────┐  ┌───▼──────────┐  ┌───▼──────────────────┐
│ Auth & User   │  │ Management   │  │ Operations           │
│ Service       │  │ Service      │  │ Service              │
│ (Port 8001)   │  │ (Port 8002)  │  │ (Port 8003)          │
│               │  │              │  │                      │
│ - Login       │  │ - Prestadores│  │ - Agendamentos       │
│ - Usuários    │  │ - Funcionários│ │ - Orçamentos         │
│ - Grupos      │  │ - Patrimônio │  │ - Eventos            │
│ - Permissões  │  │              │  │ - Reuniões/Atas      │
│ - Unidades    │  │              │  │ - Documentos         │
│               │  │              │  │ - Visitantes         │
│               │  │              │  │ - Avisos             │
│               │  │              │  │ - Logs/Auditoria     │
└───────┬───────┘  └──────┬───────┘  └──────┬───────────────┘
        │                 │                 │
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                          │
                ┌─────────▼─────────┐
                │   PostgreSQL      │
                │   Database        │
                │                   │
                │ - auth_db         │
                │ - management_db   │
                │ - operations_db   │
                └───────────────────┘
```

### 2.2. Descrição dos Microserviços

#### 2.2.1. Auth & User Service (Porta 8001)

**Responsabilidades:**
- Gerenciamento de autenticação e autorização de usuários
- Controle de acesso baseado em funções e permissões
- Gerenciamento de usuários, moradores e unidades
- Configuração de condomínios

**Tecnologias:**
- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- Pydantic (validação de dados)
- JWT (autenticação)
- Bcrypt (hash de senhas)

**Endpoints Principais:**
- `POST /api/auth/login` - Autenticação de usuário
- `POST /api/auth/logout` - Logout de usuário
- `GET /api/users` - Listar usuários
- `POST /api/users` - Criar usuário
- `GET /api/groups` - Listar grupos
- `POST /api/permissions` - Gerenciar permissões

#### 2.2.2. Management Service (Porta 8002)

**Responsabilidades:**
- Gerenciamento de cadastros estruturais do condomínio
- Controle de prestadores de serviço
- Gerenciamento de funcionários
- Controle de patrimônio

**Tecnologias:**
- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- Pydantic (validação de dados)

**Endpoints Principais:**
- `GET /api/providers` - Listar prestadores
- `POST /api/providers` - Criar prestador
- `GET /api/employees` - Listar funcionários
- `GET /api/employees/{id}/history` - Histórico de funcionário
- `GET /api/patrimony` - Listar patrimônio
- `GET /api/patrimony/{id}/history` - Histórico de patrimônio

#### 2.2.3. Operations Service (Porta 8003)

**Responsabilidades:**
- Gerenciamento de operações diárias do condomínio
- Controle de agendamentos e reservas
- Gerenciamento de orçamentos
- Controle de eventos, reuniões e atas
- Gerenciamento de documentos e visitantes
- Sistema de avisos e notificações
- Auditoria e logs de ações

**Tecnologias:**
- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- Pydantic (validação de dados)
- SMTP (envio de e-mails)

**Endpoints Principais:**
- `GET /api/schedulings` - Listar agendamentos
- `POST /api/schedulings` - Criar agendamento
- `GET /api/budgets` - Listar orçamentos
- `GET /api/budgets/{id}/history` - Histórico de orçamento
- `GET /api/meetings` - Listar reuniões
- `POST /api/meetings/{id}/send-email` - Enviar reunião por e-mail
- `GET /api/notices` - Listar avisos
- `GET /api/logs` - Listar logs
- `GET /api/audit` - Visualizar auditoria

## 3. Padrões de Comunicação

### 3.1. Comunicação Síncrona

Toda a comunicação entre os componentes do sistema é **síncrona** utilizando o protocolo **HTTP** com APIs **RESTful**.

**Frontend → Backend:**
- O frontend React consome as APIs REST dos microserviços
- Utiliza Axios ou Fetch API para requisições HTTP
- Autenticação via JWT Bearer Token
- Formato de dados: JSON

**Inter-Serviços:**
- Comunicação HTTP direta entre microserviços quando necessário
- Exemplo: Operations Service valida usuário no Auth Service
- Utiliza bibliotecas HTTP como `httpx` ou `requests`

### 3.2. Formato de Requisição e Resposta

**Requisição Padrão:**
```json
{
  "data": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "field1": "value1"
  },
  "message": "Operação realizada com sucesso"
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": {
      "field1": ["Campo obrigatório"]
    }
  }
}
```

### 3.3. Autenticação e Autorização

**Fluxo de Autenticação:**

1. Usuário envia credenciais para `POST /api/auth/login`
2. Auth Service valida credenciais no banco de dados
3. Se válido, gera token JWT com informações do usuário e permissões
4. Frontend armazena token em localStorage ou cookie seguro
5. Todas as requisições subsequentes incluem token no header `Authorization: Bearer {token}`
6. Cada microserviço valida o token antes de processar a requisição
7. Microserviço verifica permissões do usuário para a ação solicitada

**Estrutura do Token JWT:**
```json
{
  "user_id": 1,
  "username": "admin",
  "group_id": 1,
  "permissions": ["users.read", "users.write"],
  "exp": 1700000000
}
```

## 4. Banco de Dados

### 4.1. Estratégia de Banco de Dados

O sistema utiliza um único servidor **PostgreSQL** com bancos de dados separados para cada microserviço, garantindo isolamento lógico dos dados.

**Bancos de Dados:**
- `auth_db` - Auth & User Service
- `management_db` - Management Service
- `operations_db` - Operations Service

### 4.2. Vantagens da Abordagem

**Isolamento de Dados:**
- Cada microserviço possui seu próprio esquema de dados
- Mudanças em um banco não afetam outros serviços
- Facilita a manutenção e evolução independente

**Escalabilidade:**
- Possibilidade de migrar bancos para servidores separados no futuro
- Otimização de índices específica para cada serviço

**Segurança:**
- Credenciais de acesso podem ser diferentes para cada serviço
- Princípio do menor privilégio aplicado

## 5. Tecnologias Utilizadas

### 5.1. Backend

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.11+ | Linguagem de programação |
| FastAPI | 0.104+ | Framework web assíncrono |
| SQLAlchemy | 2.0+ | ORM para acesso ao banco |
| Pydantic | 2.0+ | Validação de dados |
| Alembic | 1.12+ | Migrações de banco de dados |
| PyJWT | 2.8+ | Geração e validação de tokens JWT |
| Bcrypt | 4.0+ | Hash de senhas |
| Python-Multipart | 0.0.6+ | Upload de arquivos |
| Python-SMTP | - | Envio de e-mails |
| Uvicorn | 0.24+ | Servidor ASGI |

### 5.2. Frontend

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| React | 19.1+ | Biblioteca UI |
| TypeScript | 5.9+ | Tipagem estática |
| Vite | 7.1+ | Build tool |
| Tailwind CSS | 4.1+ | Framework CSS |
| Wouter | 3.3+ | Roteamento |
| Axios | 1.12+ | Cliente HTTP |
| Shadcn/ui | - | Componentes UI |

### 5.3. Banco de Dados

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| PostgreSQL | 14+ | Banco de dados relacional |

## 6. Segurança

### 6.1. Medidas de Segurança Implementadas

**Autenticação:**
- Senhas armazenadas com hash bcrypt (salt rounds: 12)
- Tokens JWT com expiração configurável
- Refresh tokens para renovação de sessão

**Autorização:**
- Sistema de permissões granulares
- Verificação de permissões em cada endpoint
- Princípio do menor privilégio

**Proteção de Dados:**
- Validação de entrada com Pydantic
- Sanitização de dados
- Proteção contra SQL Injection (uso de ORM)
- Proteção contra XSS (sanitização no frontend)

**Comunicação:**
- HTTPS obrigatório em produção
- CORS configurado adequadamente
- Rate limiting para prevenir ataques de força bruta

**Auditoria:**
- Logs de todas as ações críticas
- Rastreamento de alterações em entidades importantes
- Sistema de auditoria para análise de atividades

## 7. Escalabilidade e Performance

### 7.1. Estratégias de Escalabilidade

**Horizontal:**
- Microserviços podem ser replicados independentemente
- Load balancing via Nginx ou API Gateway
- Stateless design permite múltiplas instâncias

**Vertical:**
- Otimização de queries com índices apropriados
- Cache de dados frequentemente acessados
- Connection pooling no banco de dados

**Banco de Dados:**
- Índices em campos de busca frequente
- Particionamento de tabelas grandes (logs, históricos)
- Read replicas para consultas pesadas

### 7.2. Performance

**Backend:**
- FastAPI assíncrono para alta concorrência
- Lazy loading de relacionamentos
- Paginação em listagens

**Frontend:**
- Code splitting para reduzir bundle inicial
- Lazy loading de rotas
- Memoização de componentes React

## 8. Deployment

### 8.1. Ambiente de Desenvolvimento

```bash
# Backend
cd Backend/auth_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Frontend
cd client
pnpm install
pnpm dev
```

### 8.2. Ambiente de Produção

**Docker Compose:**
- Containerização de cada microserviço
- Orquestração com Docker Compose
- Volumes persistentes para banco de dados

**Variáveis de Ambiente:**
- Configurações sensíveis via `.env`
- Diferentes arquivos para dev/staging/prod
- Secrets gerenciados via Docker Secrets ou Kubernetes Secrets

## 9. Monitoramento e Logs

### 9.1. Logs

**Níveis de Log:**
- DEBUG: Informações detalhadas para debugging
- INFO: Eventos gerais do sistema
- WARNING: Situações inesperadas mas não críticas
- ERROR: Erros que impedem operações
- CRITICAL: Falhas graves do sistema

**Estrutura de Log:**
```json
{
  "timestamp": "2025-11-26T17:30:00Z",
  "level": "INFO",
  "service": "auth_service",
  "user_id": 1,
  "action": "login",
  "ip": "192.168.1.100",
  "details": {}
}
```

### 9.2. Auditoria

**Eventos Auditados:**
- Login/Logout de usuários
- Criação, edição e exclusão de registros
- Alterações de permissões
- Acesso a dados sensíveis
- Falhas de autenticação

## 10. Próximos Passos

1. Implementação dos modelos de dados em cada microserviço
2. Desenvolvimento dos endpoints REST
3. Criação das migrações de banco de dados
4. Desenvolvimento da interface web
5. Testes unitários e de integração
6. Documentação completa com Swagger/OpenAPI
7. Configuração de CI/CD
8. Deploy em ambiente de produção
