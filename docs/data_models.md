# Modelos de Dados do Sistema de Condomínio

## 1. Introdução

Este documento detalha todos os modelos de dados (entidades) do Sistema de Condomínio, organizados por microserviço. Cada modelo representa uma tabela no banco de dados PostgreSQL e inclui seus atributos, tipos de dados, relacionamentos e regras de negócio.

## 2. Auth & User Service - Modelos

### 2.1. User (Usuário)

Representa os usuários do sistema, incluindo moradores, administradores e síndicos.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| username | VARCHAR(100) | UNIQUE, NOT NULL | Nome de usuário para login |
| password_hash | VARCHAR(255) | NOT NULL | Hash bcrypt da senha |
| email | VARCHAR(255) | UNIQUE | E-mail do usuário |
| full_name | VARCHAR(255) | NOT NULL | Nome completo |
| phone | VARCHAR(20) | | Telefone de contato |
| group_id | INTEGER | FK(groups.id), NOT NULL | Grupo de permissões |
| is_active | BOOLEAN | DEFAULT TRUE | Usuário ativo/inativo |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |
| last_login | TIMESTAMP | | Último login |

**Relacionamentos:**
- Pertence a um `Group` (many-to-one)
- Pode ter múltiplos `Resident` (one-to-many)

**Índices:**
- `idx_user_username` em `username`
- `idx_user_email` em `email`
- `idx_user_group` em `group_id`

### 2.2. Group (Grupo)

Representa grupos de usuários com permissões específicas.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Nome do grupo |
| description | TEXT | | Descrição do grupo |
| is_active | BOOLEAN | DEFAULT TRUE | Grupo ativo/inativo |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Relacionamentos:**
- Possui múltiplos `User` (one-to-many)
- Possui múltiplas `Permission` (one-to-many)

**Exemplos de Grupos:**
- Administrador
- Síndico
- Morador
- Porteiro
- Zelador

### 2.3. Function (Função/Tela)

Representa as funcionalidades/telas do sistema.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Nome da função |
| code | VARCHAR(50) | UNIQUE, NOT NULL | Código único da função |
| description | TEXT | | Descrição da função |
| module | VARCHAR(50) | NOT NULL | Módulo do sistema |
| is_active | BOOLEAN | DEFAULT TRUE | Função ativa/inativa |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |

**Relacionamentos:**
- Possui múltiplas `Permission` (one-to-many)

**Exemplos de Funções:**
- `users.list` - Listar usuários
- `users.create` - Criar usuário
- `schedulings.create` - Criar agendamento
- `budgets.approve` - Aprovar orçamento

### 2.4. Permission (Permissão)

Representa as permissões de acesso de grupos a funções.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| group_id | INTEGER | FK(groups.id), NOT NULL | Grupo |
| function_id | INTEGER | FK(functions.id), NOT NULL | Função |
| action | VARCHAR(20) | NOT NULL | Ação permitida |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |

**Ações Possíveis:**
- `read` - Visualizar
- `create` - Criar
- `update` - Editar
- `delete` - Excluir
- `execute` - Executar ação especial

**Relacionamentos:**
- Pertence a um `Group` (many-to-one)
- Pertence a uma `Function` (many-to-one)

**Constraint Única:**
- `UNIQUE(group_id, function_id, action)`

### 2.5. Condominium (Condomínio)

Representa os dados do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(255) | NOT NULL | Nome do condomínio |
| cnpj | VARCHAR(18) | UNIQUE | CNPJ do condomínio |
| address | TEXT | NOT NULL | Endereço completo |
| phone | VARCHAR(20) | | Telefone |
| email | VARCHAR(255) | | E-mail principal |
| smtp_host | VARCHAR(255) | | Servidor SMTP |
| smtp_port | INTEGER | | Porta SMTP |
| smtp_user | VARCHAR(255) | | Usuário SMTP |
| smtp_password | VARCHAR(255) | | Senha SMTP (criptografada) |
| smtp_use_tls | BOOLEAN | DEFAULT TRUE | Usar TLS |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Relacionamentos:**
- Possui múltiplas `Unit` (one-to-many)

### 2.6. Unit (Unidade)

Representa as unidades/apartamentos do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| condominium_id | INTEGER | FK(condominiums.id), NOT NULL | Condomínio |
| block | VARCHAR(10) | | Bloco |
| number | VARCHAR(10) | NOT NULL | Número da unidade |
| floor | INTEGER | | Andar |
| type | VARCHAR(50) | | Tipo (apartamento, casa, sala) |
| area | DECIMAL(10,2) | | Área em m² |
| is_active | BOOLEAN | DEFAULT TRUE | Unidade ativa/inativa |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Relacionamentos:**
- Pertence a um `Condominium` (many-to-one)
- Possui múltiplos `Resident` (one-to-many)

**Constraint Única:**
- `UNIQUE(condominium_id, block, number)`

### 2.7. Resident (Morador)

Representa o vínculo entre usuários e unidades.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| user_id | INTEGER | FK(users.id), NOT NULL | Usuário |
| unit_id | INTEGER | FK(units.id), NOT NULL | Unidade |
| relationship | VARCHAR(50) | NOT NULL | Tipo de vínculo |
| is_owner | BOOLEAN | DEFAULT FALSE | É proprietário |
| is_primary | BOOLEAN | DEFAULT FALSE | Morador principal |
| move_in_date | DATE | | Data de entrada |
| move_out_date | DATE | | Data de saída |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |

**Tipos de Vínculo:**
- Proprietário
- Inquilino
- Familiar
- Agregado

**Relacionamentos:**
- Pertence a um `User` (many-to-one)
- Pertence a uma `Unit` (many-to-one)

## 3. Management Service - Modelos

### 3.1. Provider (Prestador)

Representa prestadores de serviço do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(255) | NOT NULL | Nome/Razão social |
| cnpj_cpf | VARCHAR(18) | UNIQUE | CNPJ ou CPF |
| service_type | VARCHAR(100) | NOT NULL | Tipo de serviço |
| phone | VARCHAR(20) | | Telefone |
| email | VARCHAR(255) | | E-mail |
| address | TEXT | | Endereço |
| contact_person | VARCHAR(255) | | Pessoa de contato |
| notes | TEXT | | Observações |
| is_active | BOOLEAN | DEFAULT TRUE | Prestador ativo/inativo |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Tipos de Serviço:**
- Manutenção
- Limpeza
- Segurança
- Jardinagem
- Pintura
- Elétrica
- Hidráulica
- Outros

### 3.2. Employee (Funcionário)

Representa funcionários do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(255) | NOT NULL | Nome completo |
| cpf | VARCHAR(14) | UNIQUE, NOT NULL | CPF |
| role | VARCHAR(100) | NOT NULL | Cargo |
| phone | VARCHAR(20) | | Telefone |
| email | VARCHAR(255) | | E-mail |
| address | TEXT | | Endereço |
| hire_date | DATE | NOT NULL | Data de contratação |
| termination_date | DATE | | Data de demissão |
| salary | DECIMAL(10,2) | | Salário |
| is_active | BOOLEAN | DEFAULT TRUE | Funcionário ativo/inativo |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Relacionamentos:**
- Possui múltiplos `EmployeeHistory` (one-to-many)

### 3.3. EmployeeHistory (Histórico de Funcionário)

Registra alterações nos dados de funcionários.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| employee_id | INTEGER | FK(employees.id), NOT NULL | Funcionário |
| field_name | VARCHAR(100) | NOT NULL | Campo alterado |
| old_value | TEXT | | Valor anterior |
| new_value | TEXT | | Novo valor |
| changed_by | INTEGER | FK(users.id) | Usuário que alterou |
| changed_at | TIMESTAMP | DEFAULT NOW() | Data da alteração |

**Relacionamentos:**
- Pertence a um `Employee` (many-to-one)

### 3.4. Patrimony (Patrimônio)

Representa bens patrimoniais do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(255) | NOT NULL | Nome do bem |
| description | TEXT | | Descrição detalhada |
| category | VARCHAR(100) | NOT NULL | Categoria |
| location | VARCHAR(255) | | Localização |
| acquisition_date | DATE | | Data de aquisição |
| acquisition_value | DECIMAL(10,2) | | Valor de aquisição |
| current_value | DECIMAL(10,2) | | Valor atual |
| condition | VARCHAR(50) | | Estado de conservação |
| serial_number | VARCHAR(100) | | Número de série |
| notes | TEXT | | Observações |
| is_active | BOOLEAN | DEFAULT TRUE | Patrimônio ativo/inativo |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Categorias:**
- Equipamento
- Mobília
- Veículo
- Eletrônico
- Ferramenta
- Outros

**Condições:**
- Novo
- Bom
- Regular
- Ruim
- Inutilizado

**Relacionamentos:**
- Possui múltiplos `PatrimonyHistory` (one-to-many)

### 3.5. PatrimonyHistory (Histórico de Patrimônio)

Registra alterações nos dados de patrimônio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| patrimony_id | INTEGER | FK(patrimonies.id), NOT NULL | Patrimônio |
| field_name | VARCHAR(100) | NOT NULL | Campo alterado |
| old_value | TEXT | | Valor anterior |
| new_value | TEXT | | Novo valor |
| changed_by | INTEGER | FK(users.id) | Usuário que alterou |
| changed_at | TIMESTAMP | DEFAULT NOW() | Data da alteração |

**Relacionamentos:**
- Pertence a um `Patrimony` (many-to-one)

## 4. Operations Service - Modelos

### 4.1. Area (Área Comum)

Representa áreas comuns disponíveis para agendamento.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(255) | NOT NULL | Nome da área |
| description | TEXT | | Descrição |
| capacity | INTEGER | | Capacidade de pessoas |
| hourly_rate | DECIMAL(10,2) | | Taxa por hora |
| requires_approval | BOOLEAN | DEFAULT FALSE | Requer aprovação |
| is_active | BOOLEAN | DEFAULT TRUE | Área ativa/inativa |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Exemplos de Áreas:**
- Salão de Festas
- Churrasqueira
- Quadra Esportiva
- Piscina
- Academia
- Sala de Jogos

**Relacionamentos:**
- Possui múltiplos `Scheduling` (one-to-many)

### 4.2. Scheduling (Agendamento)

Representa agendamentos de áreas comuns.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| area_id | INTEGER | FK(areas.id), NOT NULL | Área agendada |
| unit_id | INTEGER | FK(units.id), NOT NULL | Unidade solicitante |
| user_id | INTEGER | FK(users.id), NOT NULL | Usuário solicitante |
| start_datetime | TIMESTAMP | NOT NULL | Data/hora início |
| end_datetime | TIMESTAMP | NOT NULL | Data/hora fim |
| status | VARCHAR(20) | NOT NULL | Status do agendamento |
| purpose | TEXT | | Finalidade |
| guests_count | INTEGER | | Número de convidados |
| approved_by | INTEGER | FK(users.id) | Aprovador |
| approved_at | TIMESTAMP | | Data de aprovação |
| notes | TEXT | | Observações |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Status Possíveis:**
- `pending` - Pendente
- `approved` - Aprovado
- `rejected` - Rejeitado
- `cancelled` - Cancelado
- `completed` - Concluído

**Relacionamentos:**
- Pertence a uma `Area` (many-to-one)
- Pertence a uma `Unit` (many-to-one)
- Pertence a um `User` (many-to-one)

**Constraint:**
- Não permitir sobreposição de horários para mesma área

### 4.3. Budget (Orçamento)

Representa orçamentos de compra ou serviço.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| type | VARCHAR(20) | NOT NULL | Tipo (compra/serviço) |
| title | VARCHAR(255) | NOT NULL | Título do orçamento |
| description | TEXT | | Descrição detalhada |
| provider_id | INTEGER | FK(providers.id) | Prestador |
| amount | DECIMAL(10,2) | NOT NULL | Valor |
| status | VARCHAR(20) | NOT NULL | Status |
| requested_by | INTEGER | FK(users.id), NOT NULL | Solicitante |
| approved_by | INTEGER | FK(users.id) | Aprovador |
| requested_at | TIMESTAMP | DEFAULT NOW() | Data de solicitação |
| approved_at | TIMESTAMP | | Data de aprovação |
| notes | TEXT | | Observações |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Tipos:**
- `purchase` - Compra
- `service` - Serviço

**Status:**
- `draft` - Rascunho
- `pending` - Pendente
- `approved` - Aprovado
- `rejected` - Rejeitado
- `completed` - Concluído

**Relacionamentos:**
- Pode pertencer a um `Provider` (many-to-one)
- Possui múltiplos `BudgetHistory` (one-to-many)

### 4.4. BudgetHistory (Histórico de Orçamento)

Registra alterações de status em orçamentos.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| budget_id | INTEGER | FK(budgets.id), NOT NULL | Orçamento |
| old_status | VARCHAR(20) | | Status anterior |
| new_status | VARCHAR(20) | NOT NULL | Novo status |
| changed_by | INTEGER | FK(users.id), NOT NULL | Usuário que alterou |
| comments | TEXT | | Comentários |
| changed_at | TIMESTAMP | DEFAULT NOW() | Data da alteração |

**Relacionamentos:**
- Pertence a um `Budget` (many-to-one)

### 4.5. Event (Evento)

Representa eventos do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| title | VARCHAR(255) | NOT NULL | Título do evento |
| description | TEXT | | Descrição |
| event_date | DATE | NOT NULL | Data do evento |
| start_time | TIME | | Horário de início |
| end_time | TIME | | Horário de término |
| location | VARCHAR(255) | | Local |
| organizer_id | INTEGER | FK(users.id), NOT NULL | Organizador |
| is_public | BOOLEAN | DEFAULT TRUE | Visível para todos |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Relacionamentos:**
- Pertence a um `User` (many-to-one)

### 4.6. Meeting (Reunião)

Representa reuniões do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| title | VARCHAR(255) | NOT NULL | Título da reunião |
| description | TEXT | | Descrição/Pauta |
| meeting_date | TIMESTAMP | NOT NULL | Data/hora da reunião |
| location | VARCHAR(255) | | Local |
| organizer_id | INTEGER | FK(users.id), NOT NULL | Organizador |
| status | VARCHAR(20) | NOT NULL | Status |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Status:**
- `scheduled` - Agendada
- `in_progress` - Em andamento
- `completed` - Concluída
- `cancelled` - Cancelada

**Relacionamentos:**
- Pertence a um `User` (many-to-one)
- Possui múltiplos `MeetingHistory` (one-to-many)
- Pode ter uma `Minute` (one-to-one)

### 4.7. MeetingHistory (Histórico de Reunião)

Registra alterações em reuniões.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| meeting_id | INTEGER | FK(meetings.id), NOT NULL | Reunião |
| field_name | VARCHAR(100) | NOT NULL | Campo alterado |
| old_value | TEXT | | Valor anterior |
| new_value | TEXT | | Novo valor |
| changed_by | INTEGER | FK(users.id), NOT NULL | Usuário que alterou |
| changed_at | TIMESTAMP | DEFAULT NOW() | Data da alteração |

**Relacionamentos:**
- Pertence a um `Meeting` (many-to-one)

### 4.8. Minute (Ata)

Representa atas de reunião.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| meeting_id | INTEGER | FK(meetings.id), UNIQUE, NOT NULL | Reunião |
| content | TEXT | NOT NULL | Conteúdo da ata |
| attendees | TEXT | | Lista de presentes |
| decisions | TEXT | | Decisões tomadas |
| issued_by | INTEGER | FK(users.id), NOT NULL | Emitido por |
| issued_at | TIMESTAMP | DEFAULT NOW() | Data de emissão |
| sent_at | TIMESTAMP | | Data de envio por e-mail |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Relacionamentos:**
- Pertence a um `Meeting` (one-to-one)
- Possui múltiplos `MinuteHistory` (one-to-many)

### 4.9. MinuteHistory (Histórico de Ata)

Registra alterações em atas.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| minute_id | INTEGER | FK(minutes.id), NOT NULL | Ata |
| field_name | VARCHAR(100) | NOT NULL | Campo alterado |
| old_value | TEXT | | Valor anterior |
| new_value | TEXT | | Novo valor |
| changed_by | INTEGER | FK(users.id), NOT NULL | Usuário que alterou |
| changed_at | TIMESTAMP | DEFAULT NOW() | Data da alteração |

**Relacionamentos:**
- Pertence a um `Minute` (many-to-one)

### 4.10. Document (Documento)

Representa documentos do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| title | VARCHAR(255) | NOT NULL | Título do documento |
| type | VARCHAR(100) | NOT NULL | Tipo de documento |
| description | TEXT | | Descrição |
| file_path | VARCHAR(500) | NOT NULL | Caminho do arquivo |
| file_name | VARCHAR(255) | NOT NULL | Nome do arquivo |
| file_size | INTEGER | | Tamanho em bytes |
| mime_type | VARCHAR(100) | | Tipo MIME |
| uploaded_by | INTEGER | FK(users.id), NOT NULL | Usuário que enviou |
| is_public | BOOLEAN | DEFAULT FALSE | Visível para todos |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de upload |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Tipos de Documento:**
- Contrato
- Comprovante
- Relatório
- Ata
- Regimento
- Outros

**Relacionamentos:**
- Pertence a um `User` (many-to-one)

### 4.11. Visitor (Visitante)

Representa controle de visitantes.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(255) | NOT NULL | Nome do visitante |
| document | VARCHAR(20) | | Documento (RG/CPF) |
| unit_id | INTEGER | FK(units.id), NOT NULL | Unidade visitada |
| entry_time | TIMESTAMP | NOT NULL | Horário de entrada |
| exit_time | TIMESTAMP | | Horário de saída |
| vehicle_plate | VARCHAR(10) | | Placa do veículo |
| purpose | TEXT | | Motivo da visita |
| authorized_by | INTEGER | FK(users.id) | Autorizado por |
| registered_by | INTEGER | FK(users.id), NOT NULL | Registrado por |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |

**Relacionamentos:**
- Pertence a uma `Unit` (many-to-one)

### 4.12. Notice (Aviso)

Representa avisos do condomínio.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| title | VARCHAR(255) | NOT NULL | Título do aviso |
| content | TEXT | NOT NULL | Conteúdo |
| type | VARCHAR(50) | NOT NULL | Tipo de aviso |
| priority | VARCHAR(20) | NOT NULL | Prioridade |
| published_by | INTEGER | FK(users.id), NOT NULL | Publicado por |
| published_at | TIMESTAMP | DEFAULT NOW() | Data de publicação |
| expires_at | TIMESTAMP | | Data de expiração |
| is_active | BOOLEAN | DEFAULT TRUE | Aviso ativo/inativo |
| created_at | TIMESTAMP | DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | DEFAULT NOW() | Data de atualização |

**Tipos de Aviso:**
- Informativo
- Urgente
- Manutenção
- Evento
- Assembleia
- Outros

**Prioridades:**
- `low` - Baixa
- `normal` - Normal
- `high` - Alta
- `urgent` - Urgente

**Relacionamentos:**
- Pertence a um `User` (many-to-one)
- Possui múltiplos `NoticeHistory` (one-to-many)

### 4.13. NoticeHistory (Histórico de Aviso)

Registra alterações em avisos.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| notice_id | INTEGER | FK(notices.id), NOT NULL | Aviso |
| field_name | VARCHAR(100) | NOT NULL | Campo alterado |
| old_value | TEXT | | Valor anterior |
| new_value | TEXT | | Novo valor |
| changed_by | INTEGER | FK(users.id), NOT NULL | Usuário que alterou |
| changed_at | TIMESTAMP | DEFAULT NOW() | Data da alteração |

**Relacionamentos:**
- Pertence a um `Notice` (many-to-one)

### 4.14. Log (Log de Auditoria)

Registra todas as ações realizadas no sistema.

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| user_id | INTEGER | FK(users.id) | Usuário que executou |
| action | VARCHAR(100) | NOT NULL | Ação realizada |
| entity_type | VARCHAR(100) | | Tipo de entidade |
| entity_id | INTEGER | | ID da entidade |
| ip_address | VARCHAR(45) | | Endereço IP |
| user_agent | TEXT | | User agent |
| request_method | VARCHAR(10) | | Método HTTP |
| request_path | VARCHAR(500) | | Caminho da requisição |
| request_data | TEXT | | Dados da requisição (JSON) |
| response_status | INTEGER | | Status HTTP da resposta |
| created_at | TIMESTAMP | DEFAULT NOW() | Data/hora da ação |

**Ações Registradas:**
- `login` - Login de usuário
- `logout` - Logout de usuário
- `create` - Criação de registro
- `update` - Atualização de registro
- `delete` - Exclusão de registro
- `view` - Visualização de registro
- `approve` - Aprovação
- `reject` - Rejeição
- `send_email` - Envio de e-mail

**Relacionamentos:**
- Pode pertencer a um `User` (many-to-one)

**Índices:**
- `idx_log_user` em `user_id`
- `idx_log_action` em `action`
- `idx_log_entity` em `(entity_type, entity_id)`
- `idx_log_created` em `created_at`

## 5. Relacionamentos Entre Microserviços

Embora cada microserviço possua seu próprio banco de dados, existem relacionamentos lógicos entre entidades de diferentes serviços:

### 5.1. Auth Service → Management Service
- `Employee.changed_by` → `User.id`
- `Patrimony.changed_by` → `User.id`

### 5.2. Auth Service → Operations Service
- `Scheduling.user_id` → `User.id`
- `Scheduling.unit_id` → `Unit.id`
- `Budget.requested_by` → `User.id`
- `Meeting.organizer_id` → `User.id`
- `Visitor.unit_id` → `Unit.id`
- `Log.user_id` → `User.id`

### 5.3. Management Service → Operations Service
- `Budget.provider_id` → `Provider.id`

**Nota:** Estes relacionamentos são mantidos via IDs e validados através de chamadas HTTP entre os microserviços quando necessário.

## 6. Estratégias de Integridade

### 6.1. Validações no Nível de Aplicação

Como os microserviços possuem bancos separados, a integridade referencial entre serviços é garantida no nível da aplicação:

**Validação de Existência:**
```python
# Exemplo: Validar se usuário existe antes de criar agendamento
async def validate_user_exists(user_id: int):
    response = await http_client.get(f"{AUTH_SERVICE_URL}/api/users/{user_id}")
    if response.status_code == 404:
        raise ValueError("Usuário não encontrado")
```

**Transações Distribuídas:**
- Padrão Saga para operações que envolvem múltiplos serviços
- Compensação em caso de falha

### 6.2. Índices e Performance

Cada tabela possui índices apropriados para otimizar consultas frequentes:

**Índices em Chaves Estrangeiras:**
- Todas as colunas `*_id` possuem índices
- Índices compostos para queries comuns

**Índices em Campos de Busca:**
- Campos `username`, `email`, `cpf`, `cnpj`
- Campos de data para filtros temporais

**Índices em Campos de Status:**
- Campos `status`, `is_active`, `is_public`
- Utilizados em filtros frequentes

## 7. Convenções de Nomenclatura

### 7.1. Tabelas
- Plural em inglês
- Snake_case
- Exemplo: `users`, `meeting_histories`

### 7.2. Colunas
- Snake_case
- Sufixos descritivos:
  - `*_id` para chaves estrangeiras
  - `*_at` para timestamps
  - `is_*` para booleanos
  - `*_date` para datas
  - `*_time` para horários

### 7.3. Constraints
- `pk_*` para primary keys
- `fk_*` para foreign keys
- `uk_*` para unique constraints
- `ck_*` para check constraints
- `idx_*` para índices

## 8. Migração e Versionamento

### 8.1. Alembic

Cada microserviço utiliza **Alembic** para gerenciar migrações de banco de dados:

```bash
# Criar nova migração
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

### 8.2. Versionamento de Schema

- Cada migração possui um ID único
- Histórico completo de alterações
- Possibilidade de rollback

## 9. Considerações de Segurança

### 9.1. Dados Sensíveis

**Criptografia:**
- Senhas: bcrypt com salt rounds 12
- Configurações SMTP: criptografia AES-256
- Tokens JWT: assinados com HS256

**Proteção de Dados Pessoais (LGPD):**
- Campos sensíveis identificados
- Logs não armazenam dados pessoais completos
- Possibilidade de anonimização

### 9.2. Auditoria

**Rastreabilidade:**
- Todos os registros possuem `created_at` e `updated_at`
- Tabelas de histórico para entidades críticas
- Logs detalhados de ações

## 10. Conclusão

Este documento apresentou todos os modelos de dados do Sistema de Condomínio, organizados por microserviço. A estrutura foi projetada para garantir escalabilidade, manutenibilidade e segurança, seguindo as melhores práticas de desenvolvimento de sistemas distribuídos.
