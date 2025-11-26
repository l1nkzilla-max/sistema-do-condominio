# Guia de Uso da Collection do Postman

## 📥 Como Importar a Collection

1. Abra o Postman
2. Clique em **Import** (canto superior esquerdo)
3. Selecione o arquivo `Sistema_Condominio_API.postman_collection.json`
4. A collection será importada com todos os endpoints organizados

## 🚀 Passo a Passo para Demonstração

### 1. Iniciar os Microserviços Python

Antes de testar no Postman, você precisa executar os 3 microserviços:

```bash
# Terminal 1 - Auth Service
cd Backend/auth_service
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Terminal 2 - Management Service
cd Backend/management_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Terminal 3 - Operations Service
cd Backend/operations_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Os serviços estarão rodando em:
- **Auth Service**: http://localhost:8001
- **Management Service**: http://localhost:8002
- **Operations Service**: http://localhost:8003

### 2. Fazer Login e Obter Token

1. Na collection, vá em: **Auth & User Service (8001) → Authentication → Login**
2. Clique em **Send**
3. Copie o valor de `access_token` da resposta
4. Clique com botão direito na Collection → **Edit**
5. Vá na aba **Variables**
6. Cole o token no campo **Current Value** da variável `access_token`
7. Clique em **Save**

Agora todas as requisições autenticadas usarão automaticamente esse token!

### 3. Testar os Endpoints

A collection está organizada por microserviço e funcionalidade:

#### Auth & User Service (8001)
- ✅ **Authentication**: Login e obter usuário atual
- 👥 **Users**: Listar, criar, atualizar e deletar usuários
- 👨‍👩‍👧‍👦 **Groups**: Gerenciar grupos de permissões
- 🏢 **Units**: Gerenciar unidades do condomínio

#### Management Service (8002)
- 🏪 **Providers**: Gerenciar prestadores de serviço
- 👷 **Employees**: Gerenciar funcionários (com histórico)
- 🏛️ **Patrimony**: Gerenciar patrimônio (com histórico)

#### Operations Service (8003)
- 📅 **Schedulings**: Agendamentos de áreas comuns
- 🏊 **Areas**: Áreas comuns disponíveis
- 👤 **Visitors**: Controle de visitantes
- 📢 **Notices**: Avisos e comunicados
- 💰 **Budgets**: Orçamentos de compras e serviços
- 📊 **Logs & Audit**: Logs e auditoria

## 💡 Exemplos de Fluxo para Demonstração

### Fluxo 1: Gerenciamento de Usuários
1. **Login** → Obter token
2. **List Users** → Ver usuários existentes
3. **Create User** → Criar novo morador
4. **Get User by ID** → Buscar usuário criado
5. **Update User** → Atualizar dados
6. **Delete User** → Remover usuário

### Fluxo 2: Agendamento de Área Comum
1. **Login** → Obter token
2. **List Areas** → Ver áreas disponíveis
3. **Create Scheduling** → Agendar salão de festas
4. **List Schedulings** → Ver agendamento criado
5. **Approve Scheduling** → Aprovar agendamento

### Fluxo 3: Controle de Visitantes
1. **Login** → Obter token
2. **Register Visitor** → Registrar entrada
3. **List Visitors** → Ver visitantes no condomínio
4. **Register Exit** → Registrar saída

### Fluxo 4: Gestão de Avisos
1. **Login** → Obter token
2. **Create Notice** → Criar aviso de manutenção
3. **List Notices** → Ver avisos ativos
4. **Get Notice History** → Ver histórico de edições

## 🎯 Dicas para Apresentação

1. **Comece pelo Login**: Sempre mostre primeiro como obter o token de autenticação
2. **Demonstre CRUD completo**: Escolha uma entidade (ex: Usuários) e mostre Create, Read, Update, Delete
3. **Mostre recursos avançados**: Histórico de alterações (Employees, Patrimony, Notices)
4. **Demonstre integração**: Mostre como criar um agendamento que depende de área e usuário existentes
5. **Mostre auditoria**: Liste os logs para demonstrar rastreabilidade

## 📝 Credenciais Padrão

- **Usuário**: admin
- **Senha**: admin123

## ⚠️ Observações Importantes

- Todos os endpoints (exceto Login) requerem autenticação via token JWT
- O token deve ser incluído no header: `Authorization: Bearer {token}`
- A collection já está configurada para usar a variável `{{access_token}}` automaticamente
- Certifique-se de que os 3 microserviços estão rodando antes de testar
- Os dados são armazenados em memória, então serão perdidos ao reiniciar os serviços

## 🔍 Alternativa: Documentação Swagger

Se preferir testar diretamente no navegador sem Postman:

- **Auth Service**: http://localhost:8001/api/docs
- **Management Service**: http://localhost:8002/api/docs
- **Operations Service**: http://localhost:8003/api/docs

O Swagger permite testar todas as APIs de forma interativa!
