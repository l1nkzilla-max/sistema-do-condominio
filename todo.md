# Sistema de Condomínio - TODO

## Estrutura do Projeto
- [x] Criar estrutura de pastas (Script, Frontend, Backend)
- [x] Configurar banco de dados PostgreSQL
- [x] Documentação de arquitetura e modelos de dados

## Backend - Auth & User Service (Microserviço 1)
- [x] Configurar projeto FastAPI
- [x] Implementar modelos de dados (User, Group, Function, Permission, Unit, Resident)
- [x] API de Login (autenticação)
- [x] API de Funções (CRUD)
- [x] API de Grupos (CRUD)
- [x] API de Permissões (CRUD)
- [x] API de Condomínio com configuração de e-mails
- [x] API de Unidades (CRUD)
- [x] API de Usuários/Moradores (CRUD)
- [x] Documentação Swagger/OpenAPI

## Backend - Management Service (Microserviço 2)
- [x] Configurar projeto FastAPI
- [x] Implementar modelos de dados (Provider, Employee, Patrimony)
- [x] API de Prestadores (CRUD)
- [x] API de Funcionários com histórico (CRUD)
- [x] API de Patrimônio com histórico (CRUD)
- [x] Documentação Swagger/OpenAPI

## Backend - Operations Service (Microserviço 3)
- [x] Configurar projeto FastAPI
- [x] Implementar modelos de dados (Scheduling, Area, Budget, Event, Meeting, Minute, Document, Visitor, Notice, Log)
- [x] API de Agendamento e reserva de áreas comuns (CRUD)
- [x] API de Orçamento de compra com histórico (CRUD)
- [x] API de Orçamento de serviço com histórico (CRUD)
- [x] API de Eventos (CRUD)
- [x] API de Reunião com histórico, emissão e envio por e-mail (CRUD)
- [x] API de Ata com histórico, emissão e envio por e-mail (CRUD)
- [x] API de Documento por tipo (CRUD)
- [x] API de Controle de visitante (CRUD)
- [x] API de Avisos com histórico (CRUD)
- [x] API de Quadro de avisos (visualização)
- [x] API de Logs (gravação de ações)
- [x] API de Auditoria (baseado em logs)
- [x] Documentação Swagger/OpenAPI

## Frontend
- [ ] Tela de login (usuário e senha)
- [ ] Tela principal com menus
- [ ] Cadastro de funções
- [ ] Cadastro de grupos
- [ ] Cadastro de permissões
- [ ] Cadastro de condomínio com configuração de e-mails
- [ ] Cadastro de unidades
- [ ] Cadastro de usuários/moradores
- [ ] Cadastro de prestadores
- [ ] Agendamento e reserva de áreas comuns
- [ ] Orçamento de compra com histórico
- [ ] Orçamento de serviço com histórico
- [ ] Cadastro de eventos
- [ ] Cadastro de reunião com histórico, emissão e envio por e-mail
- [ ] Cadastro de ata com histórico, emissão e envio por e-mail
- [ ] Cadastro de funcionário com histórico
- [ ] Cadastro de documento por tipo
- [ ] Controle de visitante
- [ ] Cadastro de patrimônio com histórico
- [ ] Cadastro de aviso com histórico
- [ ] Quadro de aviso
- [ ] Tela de auditoria baseado em logs

## Banco de Dados
- [x] Scripts de criação de tabelas
- [x] Scripts de migração
- [x] Scripts de seed (dados iniciais)

## Documentação
- [x] Documentação de arquitetura
- [x] Documentação de modelos de dados
- [x] Documentação de APIs (Swagger/OpenAPI)
- [x] Documentação de funções
- [x] Documentação de padrões de comunicação
- [x] README com instruções de instalação e execução

## Entrega
- [x] Configurar repositório GitHub
- [x] Organizar estrutura de pastas conforme especificado
- [x] Preparar arquivo com endereço do GitHub
- [x] Verificar que APIs podem ser consumidas via Postman/Swagger


## Frontend - Interface Web Completa
- [x] Configurar serviço de API (axios)
- [x] Criar contexto de autenticação
- [x] Implementar tela de login
- [x] Criar dashboard principal
- [x] Implementar navegação lateral
- [x] Tela de gerenciamento de usuários
- [x] Tela de agendamentos
- [x] Tela de avisos/quadro de avisos
- [x] Tela de visitantes
- [x] Tela de orçamentos
- [x] Integração completa com APIs Python


## Correções
- [x] Corrigir URLs dos microserviços (protocolo http://)

- [x] Implementar dados mockados para demonstração sem microserviços

- [x] Adicionar conta do usuário Dslink82@hotmail.com

- [x] Atualizar conta admin para Guilherme Henrique (l1nkzilla@icloud.com)

- [x] Remover sistema de autenticação

- [x] Adicionar tela de login fictícia (guilherme/admin123)

- [x] Criar Collection do Postman completa para demonstração

- [x] Criar documento de demonstração com capturas de tela e exemplos
