-- ============================================
-- Sistema de Condomínio - Management Service
-- Script de Criação de Tabelas
-- ============================================

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS management_db;
USE management_db;

-- Tabela: providers
CREATE TABLE IF NOT EXISTS providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cnpj_cpf VARCHAR(18) UNIQUE,
    service_type VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    contact_person VARCHAR(255),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_provider_name (name),
    INDEX idx_provider_type (service_type),
    INDEX idx_provider_active (is_active)
);

-- Tabela: employees
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    role VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    hire_date DATE NOT NULL,
    termination_date DATE,
    salary DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee_name (name),
    INDEX idx_employee_cpf (cpf),
    INDEX idx_employee_role (role),
    INDEX idx_employee_active (is_active)
);

-- Tabela: employee_history
CREATE TABLE IF NOT EXISTS employee_history (
    id SERIAL PRIMARY KEY,
    employee_id BIGINT UNSIGNED NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_by BIGINT UNSIGNED,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    INDEX idx_emp_history_employee (employee_id),
    INDEX idx_emp_history_changed_at (changed_at)
);

-- Tabela: patrimonies
CREATE TABLE IF NOT EXISTS patrimonies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    acquisition_date DATE,
    acquisition_value DECIMAL(10,2),
    current_value DECIMAL(10,2),
    condition VARCHAR(50),
    serial_number VARCHAR(100),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_patrimony_name (name),
    INDEX idx_patrimony_category (category),
    INDEX idx_patrimony_active (is_active)
);

-- Tabela: patrimony_history
CREATE TABLE IF NOT EXISTS patrimony_history (
    id SERIAL PRIMARY KEY,
    patrimony_id BIGINT UNSIGNED NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_by BIGINT UNSIGNED,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patrimony_id) REFERENCES patrimonies(id) ON DELETE CASCADE,
    INDEX idx_pat_history_patrimony (patrimony_id),
    INDEX idx_pat_history_changed_at (changed_at)
);

-- ============================================
-- Dados Iniciais (Seed Data)
-- ============================================

-- Inserir prestadores exemplo
INSERT INTO providers (name, cnpj_cpf, service_type, phone, email, contact_person) VALUES
('Empresa de Limpeza ABC', '12.345.678/0001-90', 'Limpeza', '(11) 1111-1111', 'contato@limpezaabc.com', 'João Silva'),
('Manutenção Predial XYZ', '98.765.432/0001-10', 'Manutenção', '(11) 2222-2222', 'contato@manutencaoxyz.com', 'Maria Santos'),
('Segurança Total', '11.222.333/0001-44', 'Segurança', '(11) 3333-3333', 'contato@segurancatotal.com', 'Pedro Oliveira'),
('Jardinagem Verde', '55.666.777/0001-88', 'Jardinagem', '(11) 4444-4444', 'contato@jardimverde.com', 'Ana Costa');

-- Inserir funcionários exemplo
INSERT INTO employees (name, cpf, role, phone, hire_date, salary) VALUES
('Carlos Souza', '123.456.789-00', 'Porteiro', '(11) 91111-1111', '2023-01-15', 2500.00),
('Fernanda Lima', '987.654.321-00', 'Zeladora', '(11) 92222-2222', '2023-02-01', 2200.00),
('Roberto Santos', '456.789.123-00', 'Zelador', '(11) 93333-3333', '2023-03-10', 2200.00),
('Juliana Alves', '321.654.987-00', 'Porteira', '(11) 94444-4444', '2023-04-05', 2500.00);

-- Inserir patrimônio exemplo
INSERT INTO patrimonies (name, description, category, location, acquisition_date, acquisition_value, current_value, condition) VALUES
('Cortador de Grama Elétrico', 'Cortador de grama marca XYZ, modelo 2023', 'Equipamento', 'Área de serviço', '2023-01-10', 1500.00, 1200.00, 'Bom'),
('Conjunto de Mesas e Cadeiras', '10 mesas e 40 cadeiras para salão de festas', 'Mobília', 'Salão de festas', '2022-06-15', 5000.00, 4000.00, 'Bom'),
('Câmera de Segurança IP', 'Câmera de segurança com visão noturna', 'Eletrônico', 'Portaria', '2023-05-20', 800.00, 750.00, 'Novo'),
('Aspirador Industrial', 'Aspirador de pó industrial 1400W', 'Equipamento', 'Área de serviço', '2023-02-28', 1200.00, 1000.00, 'Bom');

-- ============================================
-- Fim do Script
-- ============================================
