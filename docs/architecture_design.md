# Projeto de Arquitetura e Modelos de Dados para Sistema de Condomínio

## 1. Introdução

Este documento detalha a arquitetura de microserviços e os modelos de dados propostos para o Sistema de Condomínio, conforme os requisitos estabelecidos. O sistema será desenvolvido utilizando **Python** para o *backend* e **PostgreSQL** como banco de dados, seguindo o padrão **MVC** (Model-View-Controller) na arquitetura geral e a comunicação síncrona via **APIs REST**.

## 2. Arquitetura de Microserviços

A arquitetura será dividida em três microserviços principais, conforme sugerido, para garantir a separação de responsabilidades, escalabilidade e manutenibilidade.

| Microserviço | Responsabilidades Principais | Tecnologias Sugeridas |
| :--- | :--- | :--- |
| **1. Auth & User Service** | Gerenciamento de usuários, autenticação (Login), autorização (Permissões, Grupos, Funções), e dados básicos de unidades e moradores. | Python (FastAPI/Flask), SQLAlchemy, PostgreSQL |
| **2. Management Service** | Gerenciamento de cadastros e configurações do condomínio: Condomínio, Unidades, Configuração de E-mails, Prestadores, Funcionários, Patrimônio. | Python (FastAPI/Flask), SQLAlchemy, PostgreSQL |
| **3. Operations Service** | Gerenciamento das operações diárias: Agendamentos/Reservas, Orçamentos (Compra e Serviço), Eventos, Reuniões, Atas, Documentos, Controle de Visitantes, Avisos, Logs e Auditoria. | Python (FastAPI/Flask), SQLAlchemy, PostgreSQL |

### 2.1. Padrões de Comunicação Síncrona

A comunicação entre o **Frontend** e os **Microserviços** será estritamente síncrona, utilizando o protocolo **HTTP** com APIs RESTful.

*   **Frontend -> Microserviços:** Todas as requisições do frontend (Web) serão direcionadas aos *endpoints* específicos de cada microserviço.
*   **Comunicação Inter-Serviços:** Para operações que exigem dados de outro serviço (ex: `Operations Service` precisa validar um `User` no `Auth & User Service`), a comunicação será síncrona via chamadas HTTP diretas entre os serviços.

## 3. Modelos de Dados (Esquema Simplificado)

Os modelos de dados serão distribuídos entre os microserviços. A seguir, um esboço das principais entidades e seus atributos.

### 3.1. Auth & User Service

Este serviço gerencia a base de usuários e a estrutura de acesso.

| Entidade | Atributos Chave | Descrição |
| :--- | :--- | :--- |
| **User** | `id`, `username`, `password_hash`, `group_id`, `unit_id`, `is_resident` | Usuários do sistema (moradores, administradores, etc.). |
| **Group** | `id`, `name` | Grupos de usuários (ex: Morador, Síndico, Administrador). |
| **Function** | `id`, `name`, `description` | Funções/Telas do sistema. |
| **Permission** | `id`, `group_id`, `function_id`, `action` | Controle de permissões (qual grupo pode fazer qual ação em qual função/tela). |
| **Unit** | `id`, `block`, `number`, `condominium_id` | Unidades/Apartamentos. |
| **Resident** | `id`, `user_id`, `unit_id`, `apt_number` | Vínculo do usuário como morador a uma unidade. |

### 3.2. Management Service

Este serviço gerencia os cadastros estruturais do condomínio.

| Entidade | Atributos Chave | Descrição |
| :--- | :--- | :--- |
| **Condominium** | `id`, `name`, `email_config` | Dados e configurações gerais do condomínio. |
| **Provider** | `id`, `name`, `contact_info`, `service_type` | Cadastro de prestadores de serviço. |
| **Employee** | `id`, `name`, `role`, `hire_date` | Cadastro de funcionários. |
| **Patrimony** | `id`, `name`, `location`, `acquisition_date` | Cadastro de bens patrimoniais. |

### 3.3. Operations Service

Este serviço gerencia as atividades e registros operacionais.

| Entidade | Atributos Chave | Descrição |
| :--- | :--- | :--- |
| **Scheduling** | `id`, `area_id`, `unit_id`, `date`, `status` | Agendamento de áreas comuns. |
| **Area** | `id`, `name`, `capacity` | Áreas comuns (salão de festas, churrasqueira, etc.). |
| **Budget** | `id`, `type` (`compra`/`serviço`), `description`, `status` | Orçamentos de compra ou serviço. |
| **Event** | `id`, `name`, `date`, `description` | Cadastro de eventos. |
| **Meeting** | `id`, `title`, `date`, `minutes_id` | Reuniões. |
| **Minute** | `id`, `meeting_id`, `content`, `issue_date` | Atas de reunião. |
| **Document** | `id`, `type`, `file_path`, `upload_date` | Documentos por tipo. |
| **Visitor** | `id`, `name`, `entry_time`, `exit_time`, `unit_id` | Controle de visitantes. |
| **Notice** | `id`, `title`, `content`, `post_date` | Avisos para o condomínio. |
| **Log** | `id`, `user_id`, `action`, `timestamp`, `details` | Gravação de logs de ações e auditoria. |

## 4. Próximos Passos

1.  **Inicialização do Projeto:** Criar a estrutura de pastas e inicializar o ambiente de desenvolvimento.
2.  **Configuração do Banco de Dados:** Criar o banco de dados PostgreSQL e aplicar as migrações iniciais para os modelos definidos.
3.  **Desenvolvimento do Backend:** Implementar os *endpoints* RESTful para cada microserviço.
4.  **Desenvolvimento do Frontend:** Criar a interface web para consumir as APIs.
5.  **Documentação:** Gerar a documentação completa.
6.  **Entrega:** Configurar o GitHub e entregar o projeto.
