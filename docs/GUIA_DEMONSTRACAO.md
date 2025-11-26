# Guia Completo de Demonstração - Sistema de Condomínio

**Autor:** Manus AI  
**Data:** 26 de Novembro de 2025  
**Versão:** 1.0

---

## Sumário Executivo

Este documento apresenta um guia completo e visual para demonstração do Sistema de Condomínio desenvolvido com arquitetura de microserviços. O sistema é composto por três microserviços independentes implementados em Python com FastAPI, um banco de dados PostgreSQL e uma interface web moderna em React. Este guia fornece instruções detalhadas para executar os serviços, testar as APIs via Postman e demonstrar as funcionalidades principais do sistema.

---

## 1. Visão Geral da Arquitetura

O sistema foi desenvolvido seguindo os princípios de **arquitetura de microserviços**, onde cada serviço possui responsabilidades bem definidas e opera de forma independente. A comunicação entre os serviços e o frontend ocorre através de APIs REST padronizadas, utilizando autenticação JWT para garantir segurança.

### Componentes Principais

| Componente | Tecnologia | Porta | Responsabilidade |
|------------|-----------|-------|------------------|
| Auth & User Service | Python 3.11 + FastAPI | 8001 | Autenticação, usuários, grupos, permissões e unidades |
| Management Service | Python 3.11 + FastAPI | 8002 | Prestadores, funcionários e patrimônio |
| Operations Service | Python 3.11 + FastAPI | 8003 | Agendamentos, visitantes, avisos, orçamentos e auditoria |
| Frontend | React 19 + TypeScript | 3000 | Interface web responsiva |
| Banco de Dados | PostgreSQL 14+ | 5432 | Armazenamento persistente |

### Padrões de Comunicação

O sistema utiliza **comunicação síncrona** via HTTP/REST entre o frontend e os microserviços. Cada microserviço expõe endpoints documentados automaticamente através do Swagger/OpenAPI, facilitando testes e integração. A autenticação é realizada através de tokens JWT (JSON Web Tokens) que são incluídos no header `Authorization` de todas as requisições protegidas.

---

## 2. Preparação do Ambiente

### 2.1. Pré-requisitos

Antes de iniciar a demonstração, certifique-se de que os seguintes softwares estão instalados no sistema:

- **Python 3.11+**: Interpretador Python para executar os microserviços
- **PostgreSQL 14+**: Sistema de gerenciamento de banco de dados
- **Postman**: Ferramenta para testar APIs REST
- **Node.js 18+** (opcional): Para executar o frontend React

### 2.2. Configuração do Banco de Dados

O primeiro passo é criar os bancos de dados PostgreSQL necessários para cada microserviço. Abra o terminal do PostgreSQL (psql) e execute os seguintes comandos:

```sql
-- Criar bancos de dados
CREATE DATABASE auth_db;
CREATE DATABASE management_db;
CREATE DATABASE operations_db;

-- Criar usuário (opcional)
CREATE USER condominio_user WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE auth_db TO condominio_user;
GRANT ALL PRIVILEGES ON DATABASE management_db TO condominio_user;
GRANT ALL PRIVILEGES ON DATABASE operations_db TO condominio_user;
```

Em seguida, execute os scripts SQL de criação de tabelas localizados na pasta `Script/`:

```bash
# Executar scripts de criação de tabelas
psql -U postgres -d auth_db -f Script/01_create_auth_tables.sql
psql -U postgres -d management_db -f Script/02_create_management_tables.sql
psql -U postgres -d operations_db -f Script/03_create_operations_tables.sql
```

**Resultado Esperado:** As tabelas serão criadas em cada banco de dados sem erros. Você pode verificar executando `\dt` no psql para listar as tabelas criadas.

---

## 3. Execução dos Microserviços

### 3.1. Auth & User Service (Porta 8001)

Abra um terminal e navegue até o diretório do serviço de autenticação:

```bash
cd Backend/auth_service

# Criar ambiente virtual Python
python -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env e configure DATABASE_URL

# Executar o serviço
python main.py
```

**Saída Esperada no Terminal:**

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

**Verificação:** Abra o navegador e acesse `http://localhost:8001/api/docs`. Você deverá ver a documentação Swagger interativa do Auth Service com todos os endpoints disponíveis.

### 3.2. Management Service (Porta 8002)

Em um **novo terminal**, execute os mesmos passos para o Management Service:

```bash
cd Backend/management_service
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
cp .env.example .env
# Edite .env conforme necessário
python main.py
```

**Saída Esperada:**

```
INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
```

**Verificação:** Acesse `http://localhost:8002/api/docs` para ver a documentação Swagger.

### 3.3. Operations Service (Porta 8003)

Em um **terceiro terminal**, execute:

```bash
cd Backend/operations_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

**Saída Esperada:**

```
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
```

**Verificação:** Acesse `http://localhost:8003/api/docs`.

### 3.4. Status dos Serviços

Neste ponto, você deve ter **três terminais abertos**, cada um executando um microserviço. Verifique se todos estão respondendo corretamente:

| Serviço | URL | Status Esperado |
|---------|-----|-----------------|
| Auth Service | http://localhost:8001/api/docs | ✅ Swagger UI carregado |
| Management Service | http://localhost:8002/api/docs | ✅ Swagger UI carregado |
| Operations Service | http://localhost:8003/api/docs | ✅ Swagger UI carregado |

---

## 4. Demonstração com Postman

### 4.1. Importar a Collection

Abra o Postman e siga os passos abaixo para importar a collection completa:

1. Clique no botão **Import** no canto superior esquerdo
2. Selecione a aba **File**
3. Navegue até `postman/Sistema_Condominio_API.postman_collection.json`
4. Clique em **Import**

**Resultado:** A collection "Sistema de Condomínio - API Collection" aparecerá na barra lateral esquerda, organizada em três pastas principais correspondentes aos microserviços.

### 4.2. Fluxo 1: Autenticação e Obtenção de Token

#### Passo 1: Fazer Login

Na collection, navegue até:  
**Auth & User Service (8001) → Authentication → Login**

**Configuração da Requisição:**

```
Método: POST
URL: http://localhost:8001/api/auth/login
Content-Type: application/x-www-form-urlencoded

Body (x-www-form-urlencoded):
username: admin
password: admin123
```

**Clique em Send**

**Resposta Esperada (Status 200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwMzYxMjQwMH0.abc123...",
  "token_type": "bearer"
}
```

#### Passo 2: Configurar Token na Collection

1. **Copie** o valor de `access_token` da resposta
2. Clique com botão direito na collection "Sistema de Condomínio - API Collection"
3. Selecione **Edit**
4. Vá na aba **Variables**
5. Localize a variável `access_token`
6. **Cole** o token no campo **Current Value**
7. Clique em **Save**

**Importante:** Agora todas as requisições autenticadas usarão automaticamente este token através da variável `{{access_token}}`.

### 4.3. Fluxo 2: Gerenciamento de Usuários (CRUD Completo)

#### Listar Usuários

**Requisição:**

```
GET http://localhost:8001/api/users?skip=0&limit=10
Authorization: Bearer {{access_token}}
```

**Resposta Esperada:**

```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@condominio.com",
    "full_name": "Administrador do Sistema",
    "group_id": 1,
    "is_active": true,
    "created_at": "2025-11-26T10:00:00",
    "last_login": "2025-11-26T14:30:00"
  }
]
```

#### Criar Novo Usuário

**Requisição:**

```
POST http://localhost:8001/api/users
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "username": "joao.silva",
  "email": "joao.silva@email.com",
  "full_name": "João Silva",
  "password": "senha123",
  "group_id": 2,
  "unit_id": 101
}
```

**Resposta Esperada (Status 201 Created):**

```json
{
  "id": 2,
  "username": "joao.silva",
  "email": "joao.silva@email.com",
  "full_name": "João Silva",
  "group_id": 2,
  "unit_id": 101,
  "is_active": true,
  "created_at": "2025-11-26T15:00:00"
}
```

#### Buscar Usuário por ID

**Requisição:**

```
GET http://localhost:8001/api/users/2
Authorization: Bearer {{access_token}}
```

**Resposta Esperada:**

```json
{
  "id": 2,
  "username": "joao.silva",
  "email": "joao.silva@email.com",
  "full_name": "João Silva",
  "group_id": 2,
  "unit_id": 101,
  "is_active": true
}
```

#### Atualizar Usuário

**Requisição:**

```
PUT http://localhost:8001/api/users/2
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "email": "joao.silva.novo@email.com",
  "full_name": "João Silva Santos"
}
```

**Resposta Esperada:**

```json
{
  "id": 2,
  "username": "joao.silva",
  "email": "joao.silva.novo@email.com",
  "full_name": "João Silva Santos",
  "group_id": 2,
  "is_active": true
}
```

#### Deletar Usuário

**Requisição:**

```
DELETE http://localhost:8001/api/users/2
Authorization: Bearer {{access_token}}
```

**Resposta Esperada (Status 204 No Content):**

```
(Sem corpo de resposta)
```

### 4.4. Fluxo 3: Agendamento de Área Comum

#### Listar Áreas Disponíveis

**Requisição:**

```
GET http://localhost:8003/api/areas
Authorization: Bearer {{access_token}}
```

**Resposta Esperada:**

```json
[
  {
    "id": 1,
    "name": "Salão de Festas",
    "description": "Salão principal com capacidade para 80 pessoas",
    "capacity": 80,
    "is_active": true
  },
  {
    "id": 2,
    "name": "Churrasqueira",
    "description": "Área de churrasqueira coberta",
    "capacity": 20,
    "is_active": true
  }
]
```

#### Criar Agendamento

**Requisição:**

```
POST http://localhost:8003/api/schedulings
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "area_id": 1,
  "user_id": 2,
  "date": "2025-12-15",
  "start_time": "14:00",
  "end_time": "22:00",
  "description": "Festa de aniversário",
  "status": "Pendente"
}
```

**Resposta Esperada:**

```json
{
  "id": 1,
  "area_id": 1,
  "user_id": 2,
  "date": "2025-12-15",
  "start_time": "14:00:00",
  "end_time": "22:00:00",
  "description": "Festa de aniversário",
  "status": "Pendente",
  "created_at": "2025-11-26T15:30:00"
}
```

#### Aprovar Agendamento

**Requisição:**

```
PUT http://localhost:8003/api/schedulings/1
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "status": "Aprovado"
}
```

**Resposta Esperada:**

```json
{
  "id": 1,
  "area_id": 1,
  "user_id": 2,
  "date": "2025-12-15",
  "start_time": "14:00:00",
  "end_time": "22:00:00",
  "description": "Festa de aniversário",
  "status": "Aprovado",
  "approved_at": "2025-11-26T15:35:00"
}
```

### 4.5. Fluxo 4: Controle de Visitantes

#### Registrar Entrada de Visitante

**Requisição:**

```
POST http://localhost:8003/api/visitors
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "name": "Maria Santos",
  "document": "987.654.321-00",
  "unit_id": 101,
  "entry_time": "2025-11-26T14:30:00",
  "purpose": "Visita social"
}
```

**Resposta Esperada:**

```json
{
  "id": 1,
  "name": "Maria Santos",
  "document": "987.654.321-00",
  "unit_id": 101,
  "entry_time": "2025-11-26T14:30:00",
  "exit_time": null,
  "purpose": "Visita social",
  "status": "No condomínio"
}
```

#### Listar Visitantes Ativos

**Requisição:**

```
GET http://localhost:8003/api/visitors
Authorization: Bearer {{access_token}}
```

**Resposta Esperada:**

```json
[
  {
    "id": 1,
    "name": "Maria Santos",
    "document": "987.654.321-00",
    "unit_id": 101,
    "entry_time": "2025-11-26T14:30:00",
    "exit_time": null,
    "purpose": "Visita social",
    "status": "No condomínio"
  }
]
```

#### Registrar Saída do Visitante

**Requisição:**

```
PUT http://localhost:8003/api/visitors/1/exit
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "exit_time": "2025-11-26T18:45:00"
}
```

**Resposta Esperada:**

```json
{
  "id": 1,
  "name": "Maria Santos",
  "document": "987.654.321-00",
  "unit_id": 101,
  "entry_time": "2025-11-26T14:30:00",
  "exit_time": "2025-11-26T18:45:00",
  "purpose": "Visita social",
  "status": "Saiu"
}
```

### 4.6. Fluxo 5: Gestão de Avisos

#### Criar Aviso

**Requisição:**

```
POST http://localhost:8003/api/notices
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "title": "Manutenção do Elevador",
  "content": "Será realizada manutenção preventiva no elevador social no dia 05/12. Pedimos a compreensão de todos.",
  "category": "Manutenção",
  "priority": "Alta",
  "is_active": true
}
```

**Resposta Esperada:**

```json
{
  "id": 1,
  "title": "Manutenção do Elevador",
  "content": "Será realizada manutenção preventiva no elevador social no dia 05/12. Pedimos a compreensão de todos.",
  "category": "Manutenção",
  "priority": "Alta",
  "is_active": true,
  "created_at": "2025-11-26T16:00:00",
  "created_by": 1
}
```

#### Listar Avisos Ativos

**Requisição:**

```
GET http://localhost:8003/api/notices
Authorization: Bearer {{access_token}}
```

**Resposta Esperada:**

```json
[
  {
    "id": 1,
    "title": "Manutenção do Elevador",
    "content": "Será realizada manutenção preventiva...",
    "category": "Manutenção",
    "priority": "Alta",
    "is_active": true,
    "created_at": "2025-11-26T16:00:00"
  }
]
```

### 4.7. Fluxo 6: Gestão de Funcionários (com Histórico)

#### Criar Funcionário

**Requisição:**

```
POST http://localhost:8002/api/employees
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "name": "Carlos Souza",
  "cpf": "123.456.789-00",
  "position": "Porteiro",
  "hire_date": "2025-01-15",
  "salary": 2500.00,
  "is_active": true
}
```

**Resposta Esperada:**

```json
{
  "id": 1,
  "name": "Carlos Souza",
  "cpf": "123.456.789-00",
  "position": "Porteiro",
  "hire_date": "2025-01-15",
  "salary": 2500.00,
  "is_active": true,
  "created_at": "2025-11-26T16:15:00"
}
```

#### Atualizar Funcionário (gera histórico)

**Requisição:**

```
PUT http://localhost:8002/api/employees/1
Authorization: Bearer {{access_token}}
Content-Type: application/json

Body:
{
  "salary": 2800.00,
  "position": "Porteiro Chefe"
}
```

**Resposta Esperada:**

```json
{
  "id": 1,
  "name": "Carlos Souza",
  "cpf": "123.456.789-00",
  "position": "Porteiro Chefe",
  "hire_date": "2025-01-15",
  "salary": 2800.00,
  "is_active": true,
  "updated_at": "2025-11-26T16:20:00"
}
```

#### Consultar Histórico do Funcionário

**Requisição:**

```
GET http://localhost:8002/api/employees/1/history
Authorization: Bearer {{access_token}}
```

**Resposta Esperada:**

```json
[
  {
    "id": 1,
    "employee_id": 1,
    "field_changed": "salary",
    "old_value": "2500.00",
    "new_value": "2800.00",
    "changed_at": "2025-11-26T16:20:00",
    "changed_by": 1
  },
  {
    "id": 2,
    "employee_id": 1,
    "field_changed": "position",
    "old_value": "Porteiro",
    "new_value": "Porteiro Chefe",
    "changed_at": "2025-11-26T16:20:00",
    "changed_by": 1
  }
]
```

---

## 5. Demonstração do Frontend Web

### 5.1. Acessar o Sistema

Abra o navegador e acesse: `http://localhost:3000`

**Tela Inicial:** Você verá a tela de login do Sistema de Condomínio com um design moderno em gradiente azul.

### 5.2. Fazer Login

**Credenciais:**
- **Usuário:** guilherme
- **Senha:** admin123

Digite as credenciais e clique em **Entrar**.

**Resultado:** Você será redirecionado para o Dashboard principal do sistema.

### 5.3. Navegação pelo Dashboard

O dashboard apresenta uma visão geral do sistema com estatísticas em tempo real:

| Card | Valor | Descrição |
|------|-------|-----------|
| Usuários | 4 | Total de usuários cadastrados |
| Agendamentos | 3 | Agendamentos de áreas comuns |
| Avisos | 4 | Avisos ativos no quadro |
| Visitantes | 3 | Visitantes registrados |

Abaixo das estatísticas, há duas seções:

1. **Bem-vindo ao Sistema de Condomínio**: Apresenta as principais funcionalidades
2. **Acesso Rápido**: Atalhos para as funcionalidades mais usadas

### 5.4. Gerenciar Usuários

Clique em **Usuários** na barra lateral esquerda.

**Tela de Usuários:** Exibe uma tabela com todos os usuários cadastrados, mostrando:
- Nome completo
- Email
- Grupo
- Status (Ativo/Inativo)
- Data do último login

### 5.5. Visualizar Agendamentos

Clique em **Agendamentos** na barra lateral.

**Tela de Agendamentos:** Lista todos os agendamentos com:
- Área reservada
- Morador responsável
- Data e horário
- Status (Pendente/Aprovado/Rejeitado)
- Botão de ação (Aprovar para pendentes)

**Ação:** Clique em **Aprovar** em um agendamento pendente. O status mudará para "Aprovado" instantaneamente.

### 5.6. Quadro de Avisos

Clique em **Avisos** na barra lateral.

**Tela de Avisos:** Mostra cards coloridos com os avisos ativos:
- Título do aviso
- Conteúdo
- Categoria
- Prioridade (com badge colorido)
- Data de publicação

### 5.7. Controle de Visitantes

Clique em **Visitantes** na barra lateral.

**Tela de Visitantes:** Tabela com registro de visitantes mostrando:
- Nome do visitante
- Documento
- Unidade visitada
- Horário de entrada
- Horário de saída
- Status

### 5.8. Fazer Logout

Clique no seu perfil no canto inferior esquerdo da barra lateral (Guilherme Henrique).

Um menu dropdown aparecerá com a opção **Sair**. Clique nela para fazer logout e retornar à tela de login.

---

## 6. Recursos Avançados Demonstrados

### 6.1. Histórico de Alterações

O sistema mantém histórico completo de alterações em entidades críticas como funcionários, patrimônio e avisos. Cada modificação é registrada com:

- Campo alterado
- Valor anterior
- Valor novo
- Data e hora da alteração
- Usuário responsável

Isso garante **rastreabilidade** e **auditoria** completa das operações.

### 6.2. Sistema de Logs e Auditoria

Todas as ações realizadas no sistema são registradas em logs estruturados. A API de auditoria permite:

- Filtrar logs por período
- Buscar ações de usuários específicos
- Gerar relatórios de auditoria
- Identificar padrões de uso

**Exemplo de Requisição:**

```
GET http://localhost:8003/api/audit?start_date=2025-11-01&end_date=2025-11-30
Authorization: Bearer {{access_token}}
```

### 6.3. Autenticação JWT

O sistema utiliza **JSON Web Tokens (JWT)** para autenticação stateless. Vantagens:

- Não requer armazenamento de sessão no servidor
- Escalável horizontalmente
- Tokens com tempo de expiração configurável
- Informações do usuário embutidas no token

### 6.4. Documentação Automática com Swagger

Cada microserviço gera automaticamente documentação interativa através do Swagger/OpenAPI. Benefícios:

- Documentação sempre atualizada com o código
- Interface para testar APIs diretamente no navegador
- Especificação OpenAPI exportável
- Facilita integração com outros sistemas

---

## 7. Checklist de Demonstração

Use este checklist durante sua apresentação para garantir que todos os pontos importantes foram cobertos:

### Preparação
- [ ] Banco de dados PostgreSQL criado e populado
- [ ] Três microserviços Python executando sem erros
- [ ] Postman com collection importada
- [ ] Frontend React acessível no navegador

### Demonstração de Arquitetura
- [ ] Explicar arquitetura de microserviços
- [ ] Mostrar separação de responsabilidades
- [ ] Demonstrar comunicação via REST
- [ ] Explicar autenticação JWT

### Demonstração de APIs (Postman)
- [ ] Login e obtenção de token
- [ ] CRUD completo de usuários
- [ ] Criar e aprovar agendamento
- [ ] Registrar entrada e saída de visitante
- [ ] Criar aviso
- [ ] Consultar histórico de funcionário
- [ ] Gerar relatório de auditoria

### Demonstração de Frontend
- [ ] Login no sistema
- [ ] Navegar pelo dashboard
- [ ] Visualizar estatísticas
- [ ] Gerenciar usuários
- [ ] Aprovar agendamento
- [ ] Visualizar quadro de avisos
- [ ] Consultar visitantes
- [ ] Fazer logout

### Documentação
- [ ] Mostrar documentação Swagger de cada serviço
- [ ] Apresentar diagramas de arquitetura
- [ ] Mostrar modelos de dados
- [ ] Explicar padrões de comunicação

---

## 8. Troubleshooting (Resolução de Problemas)

### Problema: Microserviço não inicia

**Sintoma:** Erro ao executar `python main.py`

**Soluções:**
1. Verificar se o ambiente virtual está ativado
2. Reinstalar dependências: `pip install -r requirements.txt`
3. Verificar se a porta já está em uso: `lsof -i :8001` (Linux/Mac) ou `netstat -ano | findstr :8001` (Windows)
4. Verificar configuração do banco de dados no arquivo `.env`

### Problema: Erro de conexão com banco de dados

**Sintoma:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Soluções:**
1. Verificar se o PostgreSQL está rodando: `sudo service postgresql status`
2. Verificar credenciais no arquivo `.env`
3. Verificar se o banco de dados foi criado
4. Testar conexão manual: `psql -U postgres -d auth_db`

### Problema: Token JWT inválido no Postman

**Sintoma:** Resposta 401 Unauthorized

**Soluções:**
1. Verificar se o token foi copiado corretamente (sem espaços)
2. Fazer login novamente para obter novo token
3. Verificar se a variável `{{access_token}}` está configurada na collection
4. Verificar se o header `Authorization: Bearer {{access_token}}` está presente

### Problema: Frontend não carrega

**Sintoma:** Página em branco ou erro de conexão

**Soluções:**
1. Verificar se o servidor de desenvolvimento está rodando
2. Limpar cache do navegador (Ctrl+Shift+Delete)
3. Verificar console do navegador (F12) para erros
4. Verificar se as variáveis de ambiente estão configuradas

---

## 9. Conclusão

Este guia apresentou um roteiro completo para demonstração do Sistema de Condomínio, cobrindo desde a preparação do ambiente até a execução de fluxos completos de uso. O sistema demonstra a aplicação prática de conceitos modernos de desenvolvimento de software, incluindo arquitetura de microserviços, APIs REST, autenticação JWT e interfaces web responsivas.

A arquitetura modular permite que cada microserviço seja desenvolvido, testado e implantado independentemente, facilitando manutenção e escalabilidade. O uso de padrões de comunicação síncrona via HTTP/REST garante interoperabilidade e facilita integração com outros sistemas.

A documentação automática via Swagger e a collection do Postman fornecem ferramentas valiosas para testes, validação e integração, tornando o sistema acessível tanto para desenvolvedores quanto para usuários finais.

---

**Autor:** Manus AI  
**Versão do Documento:** 1.0  
**Data:** 26 de Novembro de 2025
