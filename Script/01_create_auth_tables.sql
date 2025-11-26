-- ============================================
-- Sistema de Condomínio - Auth & User Service
-- Script de Criação de Tabelas
-- ============================================

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS auth_db;
USE auth_db;

-- Tabela: groups
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_group_name (name),
    INDEX idx_group_active (is_active)
);

-- Tabela: users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    group_id BIGINT UNSIGNED NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE RESTRICT,
    INDEX idx_user_username (username),
    INDEX idx_user_email (email),
    INDEX idx_user_group (group_id),
    INDEX idx_user_active (is_active)
);

-- Tabela: functions
CREATE TABLE IF NOT EXISTS functions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    module VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_function_code (code),
    INDEX idx_function_module (module),
    INDEX idx_function_active (is_active)
);

-- Tabela: permissions
CREATE TABLE IF NOT EXISTS permissions (
    id SERIAL PRIMARY KEY,
    group_id BIGINT UNSIGNED NOT NULL,
    function_id BIGINT UNSIGNED NOT NULL,
    action VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (function_id) REFERENCES functions(id) ON DELETE CASCADE,
    UNIQUE KEY uk_permission (group_id, function_id, action),
    INDEX idx_permission_group (group_id),
    INDEX idx_permission_function (function_id)
);

-- Tabela: condominiums
CREATE TABLE IF NOT EXISTS condominiums (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE,
    address TEXT NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    smtp_host VARCHAR(255),
    smtp_port INT,
    smtp_user VARCHAR(255),
    smtp_password VARCHAR(255),
    smtp_use_tls BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_condominium_cnpj (cnpj)
);

-- Tabela: units
CREATE TABLE IF NOT EXISTS units (
    id SERIAL PRIMARY KEY,
    condominium_id BIGINT UNSIGNED NOT NULL,
    block VARCHAR(10),
    number VARCHAR(10) NOT NULL,
    floor INT,
    type VARCHAR(50),
    area DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (condominium_id) REFERENCES condominiums(id) ON DELETE CASCADE,
    UNIQUE KEY uk_unit (condominium_id, block, number),
    INDEX idx_unit_condominium (condominium_id),
    INDEX idx_unit_active (is_active)
);

-- Tabela: residents
CREATE TABLE IF NOT EXISTS residents (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    unit_id BIGINT UNSIGNED NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    is_owner BOOLEAN DEFAULT FALSE,
    is_primary BOOLEAN DEFAULT FALSE,
    move_in_date DATE,
    move_out_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE CASCADE,
    INDEX idx_resident_user (user_id),
    INDEX idx_resident_unit (unit_id)
);

-- ============================================
-- Dados Iniciais (Seed Data)
-- ============================================

-- Inserir grupos padrão
INSERT INTO groups (name, description) VALUES
('Administrador', 'Acesso total ao sistema'),
('Síndico', 'Gerenciamento do condomínio'),
('Morador', 'Acesso básico para moradores'),
('Porteiro', 'Controle de entrada e visitantes'),
('Zelador', 'Manutenção e limpeza');

-- Inserir funções padrão
INSERT INTO functions (name, code, description, module) VALUES
-- Auth Module
('Listar Usuários', 'users.list', 'Visualizar lista de usuários', 'auth'),
('Criar Usuário', 'users.create', 'Criar novo usuário', 'auth'),
('Editar Usuário', 'users.update', 'Editar dados de usuário', 'auth'),
('Excluir Usuário', 'users.delete', 'Excluir usuário', 'auth'),
('Listar Grupos', 'groups.list', 'Visualizar lista de grupos', 'auth'),
('Gerenciar Permissões', 'permissions.manage', 'Gerenciar permissões de grupos', 'auth'),

-- Management Module
('Listar Prestadores', 'providers.list', 'Visualizar prestadores', 'management'),
('Criar Prestador', 'providers.create', 'Cadastrar prestador', 'management'),
('Listar Funcionários', 'employees.list', 'Visualizar funcionários', 'management'),
('Criar Funcionário', 'employees.create', 'Cadastrar funcionário', 'management'),
('Listar Patrimônio', 'patrimony.list', 'Visualizar patrimônio', 'management'),
('Criar Patrimônio', 'patrimony.create', 'Cadastrar patrimônio', 'management'),

-- Operations Module
('Listar Agendamentos', 'schedulings.list', 'Visualizar agendamentos', 'operations'),
('Criar Agendamento', 'schedulings.create', 'Criar agendamento', 'operations'),
('Aprovar Agendamento', 'schedulings.approve', 'Aprovar/Rejeitar agendamento', 'operations'),
('Listar Orçamentos', 'budgets.list', 'Visualizar orçamentos', 'operations'),
('Criar Orçamento', 'budgets.create', 'Criar orçamento', 'operations'),
('Aprovar Orçamento', 'budgets.approve', 'Aprovar/Rejeitar orçamento', 'operations'),
('Listar Avisos', 'notices.list', 'Visualizar avisos', 'operations'),
('Criar Aviso', 'notices.create', 'Publicar aviso', 'operations'),
('Visualizar Auditoria', 'audit.view', 'Acessar logs de auditoria', 'operations');

-- Inserir permissões para Administrador (acesso total)
INSERT INTO permissions (group_id, function_id, action)
SELECT 1, id, 'execute' FROM functions;

-- Inserir permissões para Síndico
INSERT INTO permissions (group_id, function_id, action)
SELECT 2, id, 'execute' FROM functions WHERE code IN (
    'users.list', 'groups.list',
    'providers.list', 'providers.create',
    'employees.list', 'employees.create',
    'patrimony.list', 'patrimony.create',
    'schedulings.list', 'schedulings.approve',
    'budgets.list', 'budgets.create', 'budgets.approve',
    'notices.list', 'notices.create',
    'audit.view'
);

-- Inserir permissões para Morador
INSERT INTO permissions (group_id, function_id, action)
SELECT 3, id, 'execute' FROM functions WHERE code IN (
    'schedulings.list', 'schedulings.create',
    'notices.list'
);

-- Inserir permissões para Porteiro
INSERT INTO permissions (group_id, function_id, action)
SELECT 4, id, 'execute' FROM functions WHERE code IN (
    'notices.list'
);

-- Criar usuário administrador padrão
-- Senha: admin123 (hash bcrypt)
INSERT INTO users (username, password_hash, email, full_name, group_id) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNGz7YPVS', 'admin@condominio.com', 'Administrador do Sistema', 1);

-- Inserir condomínio exemplo
INSERT INTO condominiums (name, cnpj, address, phone, email) VALUES
('Condomínio Exemplo', '12.345.678/0001-90', 'Rua Exemplo, 123 - Bairro - Cidade/UF', '(11) 1234-5678', 'contato@condominioexemplo.com');

-- Inserir unidades exemplo
INSERT INTO units (condominium_id, block, number, floor, type, area) VALUES
(1, 'A', '101', 1, 'Apartamento', 75.50),
(1, 'A', '102', 1, 'Apartamento', 75.50),
(1, 'A', '201', 2, 'Apartamento', 75.50),
(1, 'B', '101', 1, 'Apartamento', 85.00),
(1, 'B', '102', 1, 'Apartamento', 85.00);

-- ============================================
-- Fim do Script
-- ============================================
