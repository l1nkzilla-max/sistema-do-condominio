# Instruções de Execução - Sistema de Condomínio

## ⚡ Início Rápido

Este guia fornece instruções passo a passo para executar o Sistema de Condomínio.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- ✅ **Python 3.11+** - [Download](https://www.python.org/downloads/)
- ✅ **PostgreSQL 14+** ou **MySQL/MariaDB** - [Download PostgreSQL](https://www.postgresql.org/download/)
- ✅ **Node.js 18+** - [Download](https://nodejs.org/)
- ✅ **Git** - [Download](https://git-scm.com/)

## 🗄️ Passo 1: Configurar Banco de Dados

### Opção A: PostgreSQL

```bash
# Iniciar PostgreSQL
sudo service postgresql start

# Conectar ao PostgreSQL
psql -U postgres

# Executar scripts SQL
\i /caminho/para/Script/01_create_auth_tables.sql
\i /caminho/para/Script/02_create_management_tables.sql
\i /caminho/para/Script/03_create_operations_tables.sql

# Sair
\q
```

### Opção B: MySQL/MariaDB

```bash
# Iniciar MySQL
sudo service mysql start

# Conectar ao MySQL
mysql -u root -p

# Executar scripts SQL
source /caminho/para/Script/01_create_auth_tables.sql
source /caminho/para/Script/02_create_management_tables.sql
source /caminho/para/Script/03_create_operations_tables.sql

# Sair
exit
```

## 🐍 Passo 2: Executar Microserviços Backend

### Terminal 1: Auth Service (Porta 8001)

```bash
# Navegar para o diretório
cd Backend/auth_service

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env (opcional, ou editar config.py)
echo "DATABASE_URL=mysql+pymysql://root:password@localhost:3306/auth_db" > .env
echo "SECRET_KEY=minha-chave-secreta-123" >> .env

# Executar serviço
python main.py
```

**Saída esperada:**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Terminal 2: Management Service (Porta 8002)

```bash
# Navegar para o diretório
cd Backend/management_service

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
echo "DATABASE_URL=mysql+pymysql://root:password@localhost:3306/management_db" > .env

# Executar serviço
python main.py
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8002
```

### Terminal 3: Operations Service (Porta 8003)

```bash
# Navegar para o diretório
cd Backend/operations_service

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
echo "DATABASE_URL=mysql+pymysql://root:password@localhost:3306/operations_db" > .env

# Executar serviço
python main.py
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8003
```

## 🌐 Passo 3: Executar Frontend (Opcional)

### Terminal 4: React Frontend

```bash
# Navegar para o diretório
cd client

# Instalar dependências
npm install
# ou
pnpm install

# Executar em modo desenvolvimento
npm run dev
# ou
pnpm dev
```

**Saída esperada:**
```
VITE v7.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

## ✅ Passo 4: Verificar Instalação

### Verificar Microserviços

Abra seu navegador e acesse:

1. **Auth Service Docs**: http://localhost:8001/api/docs
2. **Management Service Docs**: http://localhost:8002/api/docs
3. **Operations Service Docs**: http://localhost:8003/api/docs

Você deve ver a documentação interativa Swagger de cada serviço.

### Verificar Health Check

```bash
# Auth Service
curl http://localhost:8001/health

# Management Service
curl http://localhost:8002/health

# Operations Service
curl http://localhost:8003/health
```

**Resposta esperada:**
```json
{"status":"healthy","service":"auth_service"}
```

## 🔐 Passo 5: Fazer Login

### Usando cURL

```bash
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Resposta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usando Swagger UI

1. Acesse http://localhost:8001/api/docs
2. Clique em **POST /api/auth/login**
3. Clique em **Try it out**
4. Preencha:
   - username: `admin`
   - password: `admin123`
5. Clique em **Execute**
6. Copie o `access_token` da resposta

### Autorizar nas Requisições

1. No Swagger UI, clique no botão **Authorize** (cadeado)
2. Cole o token no formato: `Bearer <seu_token>`
3. Clique em **Authorize**
4. Agora você pode testar todas as rotas protegidas

## 🧪 Passo 6: Testar APIs

### Listar Usuários

```bash
# Substitua <TOKEN> pelo token obtido no login
curl -X GET "http://localhost:8001/api/users" \
  -H "Authorization: Bearer <TOKEN>"
```

### Criar Área Comum

```bash
curl -X POST "http://localhost:8003/api/areas" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Salão de Festas",
    "description": "Salão principal com capacidade para 100 pessoas",
    "capacity": 100,
    "hourly_rate": 150.00,
    "requires_approval": true
  }'
```

### Criar Agendamento

```bash
curl -X POST "http://localhost:8003/api/schedulings" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "area_id": 1,
    "unit_id": 1,
    "user_id": 1,
    "start_datetime": "2025-12-15T14:00:00",
    "end_datetime": "2025-12-15T18:00:00",
    "purpose": "Festa de aniversário",
    "guests_count": 50
  }'
```

### Listar Avisos

```bash
curl -X GET "http://localhost:8003/api/notices" \
  -H "Authorization: Bearer <TOKEN>"
```

## 🛠️ Troubleshooting

### Erro: "Connection refused"

**Problema:** Não consegue conectar ao banco de dados.

**Solução:**
1. Verifique se o PostgreSQL/MySQL está rodando:
   ```bash
   sudo service postgresql status
   # ou
   sudo service mysql status
   ```
2. Verifique as credenciais no arquivo `.env` ou `config.py`
3. Teste a conexão:
   ```bash
   psql -U postgres -d auth_db
   # ou
   mysql -u root -p auth_db
   ```

### Erro: "ModuleNotFoundError"

**Problema:** Dependências não instaladas.

**Solução:**
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Port already in use"

**Problema:** Porta já está sendo usada.

**Solução:**
```bash
# Linux/Mac - Encontrar processo usando a porta
lsof -i :8001
kill -9 <PID>

# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Erro: "CORS policy"

**Problema:** Frontend não consegue acessar backend.

**Solução:**
1. Verifique `ALLOWED_ORIGINS` em `config.py`
2. Adicione a URL do frontend:
   ```python
   ALLOWED_ORIGINS: List[str] = [
       "http://localhost:3000",
       "http://localhost:5173",
       "http://localhost:8000"
   ]
   ```

## 📊 Monitoramento

### Logs dos Serviços

Os logs aparecem no terminal onde você executou cada serviço.

### Verificar Banco de Dados

```bash
# PostgreSQL
psql -U postgres

# Listar bancos
\l

# Conectar a um banco
\c auth_db

# Listar tabelas
\dt

# Consultar dados
SELECT * FROM users;

# Sair
\q
```

## 🔄 Reiniciar Serviços

Para reiniciar um serviço:

1. Pressione `Ctrl+C` no terminal do serviço
2. Execute novamente `python main.py`

## 📦 Estrutura de Dados Inicial

Após executar os scripts SQL, você terá:

- **5 Grupos** (Administrador, Síndico, Morador, Porteiro, Zelador)
- **1 Usuário Admin** (username: admin, password: admin123)
- **1 Condomínio Exemplo**
- **5 Unidades Exemplo**
- **20+ Funções/Permissões**
- **Áreas Comuns** (Salão, Churrasqueiras, Quadra, Piscina)
- **Avisos Exemplo**
- **Eventos Exemplo**

## 🎯 Próximos Passos

1. ✅ Explorar a documentação Swagger de cada serviço
2. ✅ Testar as APIs usando Postman ou cURL
3. ✅ Criar novos usuários e grupos
4. ✅ Configurar permissões personalizadas
5. ✅ Implementar funcionalidades adicionais

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs no terminal
2. Consulte a documentação em `docs/`
3. Verifique a configuração do banco de dados
4. Teste as rotas no Swagger UI

---

**Boa sorte com o projeto! 🚀**
