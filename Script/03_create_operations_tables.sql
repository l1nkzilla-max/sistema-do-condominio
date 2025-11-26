-- ============================================
-- Sistema de Condomínio - Operations Service
-- Script de Criação de Tabelas
-- ============================================

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS operations_db;
USE operations_db;

-- Tabela: areas
CREATE TABLE IF NOT EXISTS areas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    capacity INT,
    hourly_rate DECIMAL(10,2),
    requires_approval BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_area_name (name),
    INDEX idx_area_active (is_active)
);

-- Tabela: schedulings
CREATE TABLE IF NOT EXISTS schedulings (
    id SERIAL PRIMARY KEY,
    area_id BIGINT UNSIGNED NOT NULL,
    unit_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    purpose TEXT,
    guests_count INT,
    approved_by BIGINT UNSIGNED,
    approved_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (area_id) REFERENCES areas(id) ON DELETE RESTRICT,
    INDEX idx_scheduling_area (area_id),
    INDEX idx_scheduling_unit (unit_id),
    INDEX idx_scheduling_user (user_id),
    INDEX idx_scheduling_status (status),
    INDEX idx_scheduling_dates (start_datetime, end_datetime)
);

-- Tabela: budgets
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    provider_id BIGINT UNSIGNED,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    requested_by BIGINT UNSIGNED NOT NULL,
    approved_by BIGINT UNSIGNED,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_budget_type (type),
    INDEX idx_budget_status (status),
    INDEX idx_budget_requested_by (requested_by),
    INDEX idx_budget_provider (provider_id)
);

-- Tabela: budget_history
CREATE TABLE IF NOT EXISTS budget_history (
    id SERIAL PRIMARY KEY,
    budget_id BIGINT UNSIGNED NOT NULL,
    old_status VARCHAR(20),
    new_status VARCHAR(20) NOT NULL,
    changed_by BIGINT UNSIGNED NOT NULL,
    comments TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (budget_id) REFERENCES budgets(id) ON DELETE CASCADE,
    INDEX idx_budget_history_budget (budget_id),
    INDEX idx_budget_history_changed_at (changed_at)
);

-- Tabela: events
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    location VARCHAR(255),
    organizer_id BIGINT UNSIGNED NOT NULL,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_event_date (event_date),
    INDEX idx_event_organizer (organizer_id),
    INDEX idx_event_public (is_public)
);

-- Tabela: meetings
CREATE TABLE IF NOT EXISTS meetings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    meeting_date TIMESTAMP NOT NULL,
    location VARCHAR(255),
    organizer_id BIGINT UNSIGNED NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_meeting_date (meeting_date),
    INDEX idx_meeting_organizer (organizer_id),
    INDEX idx_meeting_status (status)
);

-- Tabela: meeting_history
CREATE TABLE IF NOT EXISTS meeting_history (
    id SERIAL PRIMARY KEY,
    meeting_id BIGINT UNSIGNED NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_by BIGINT UNSIGNED NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE,
    INDEX idx_meeting_history_meeting (meeting_id),
    INDEX idx_meeting_history_changed_at (changed_at)
);

-- Tabela: minutes
CREATE TABLE IF NOT EXISTS minutes (
    id SERIAL PRIMARY KEY,
    meeting_id BIGINT UNSIGNED NOT NULL UNIQUE,
    content TEXT NOT NULL,
    attendees TEXT,
    decisions TEXT,
    issued_by BIGINT UNSIGNED NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE,
    INDEX idx_minute_meeting (meeting_id),
    INDEX idx_minute_issued_by (issued_by)
);

-- Tabela: minute_history
CREATE TABLE IF NOT EXISTS minute_history (
    id SERIAL PRIMARY KEY,
    minute_id BIGINT UNSIGNED NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_by BIGINT UNSIGNED NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (minute_id) REFERENCES minutes(id) ON DELETE CASCADE,
    INDEX idx_minute_history_minute (minute_id),
    INDEX idx_minute_history_changed_at (changed_at)
);

-- Tabela: documents
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    description TEXT,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INT,
    mime_type VARCHAR(100),
    uploaded_by BIGINT UNSIGNED NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_document_type (type),
    INDEX idx_document_uploaded_by (uploaded_by),
    INDEX idx_document_public (is_public)
);

-- Tabela: visitors
CREATE TABLE IF NOT EXISTS visitors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    document VARCHAR(20),
    unit_id BIGINT UNSIGNED NOT NULL,
    entry_time TIMESTAMP NOT NULL,
    exit_time TIMESTAMP,
    vehicle_plate VARCHAR(10),
    purpose TEXT,
    authorized_by BIGINT UNSIGNED,
    registered_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_visitor_unit (unit_id),
    INDEX idx_visitor_entry (entry_time),
    INDEX idx_visitor_registered_by (registered_by)
);

-- Tabela: notices
CREATE TABLE IF NOT EXISTS notices (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL DEFAULT 'normal',
    published_by BIGINT UNSIGNED NOT NULL,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_notice_type (type),
    INDEX idx_notice_priority (priority),
    INDEX idx_notice_published_by (published_by),
    INDEX idx_notice_active (is_active),
    INDEX idx_notice_published_at (published_at)
);

-- Tabela: notice_history
CREATE TABLE IF NOT EXISTS notice_history (
    id SERIAL PRIMARY KEY,
    notice_id BIGINT UNSIGNED NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_by BIGINT UNSIGNED NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (notice_id) REFERENCES notices(id) ON DELETE CASCADE,
    INDEX idx_notice_history_notice (notice_id),
    INDEX idx_notice_history_changed_at (changed_at)
);

-- Tabela: logs
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id BIGINT UNSIGNED,
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_method VARCHAR(10),
    request_path VARCHAR(500),
    request_data TEXT,
    response_status INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_log_user (user_id),
    INDEX idx_log_action (action),
    INDEX idx_log_entity (entity_type, entity_id),
    INDEX idx_log_created (created_at)
);

-- ============================================
-- Dados Iniciais (Seed Data)
-- ============================================

-- Inserir áreas comuns exemplo
INSERT INTO areas (name, description, capacity, hourly_rate, requires_approval) VALUES
('Salão de Festas', 'Salão de festas com cozinha equipada', 100, 150.00, TRUE),
('Churrasqueira 1', 'Churrasqueira coberta com mesas', 20, 50.00, FALSE),
('Churrasqueira 2', 'Churrasqueira coberta com mesas', 20, 50.00, FALSE),
('Quadra Poliesportiva', 'Quadra para futebol, vôlei e basquete', 30, 0.00, FALSE),
('Piscina', 'Piscina adulto e infantil', 50, 0.00, FALSE),
('Sala de Jogos', 'Sala com mesa de sinuca e ping-pong', 15, 0.00, FALSE);

-- Inserir eventos exemplo
INSERT INTO events (title, description, event_date, start_time, end_time, location, organizer_id) VALUES
('Festa Junina do Condomínio', 'Festa junina com comidas típicas e quadrilha', '2025-06-20', '18:00:00', '22:00:00', 'Salão de Festas', 1),
('Campeonato de Futebol', 'Torneio de futebol entre moradores', '2025-07-15', '09:00:00', '17:00:00', 'Quadra Poliesportiva', 1),
('Assembleia Geral Ordinária', 'Assembleia anual de prestação de contas', '2025-03-30', '19:00:00', '21:00:00', 'Salão de Festas', 1);

-- Inserir avisos exemplo
INSERT INTO notices (title, content, type, priority, published_by) VALUES
('Manutenção Programada - Elevadores', 'Informamos que no dia 30/11/2025 será realizada manutenção preventiva nos elevadores das 8h às 12h. Pedimos a compreensão de todos.', 'Manutenção', 'high', 1),
('Horário de Funcionamento da Piscina', 'A piscina estará aberta diariamente das 7h às 20h. Uso obrigatório de touca.', 'Informativo', 'normal', 1),
('Coleta Seletiva', 'Lembramos que a coleta seletiva ocorre todas as terças e quintas-feiras. Separe seu lixo corretamente!', 'Informativo', 'low', 1),
('Assembleia Extraordinária', 'Fica convocada assembleia extraordinária para o dia 15/12/2025 às 19h no salão de festas para discussão sobre obras de reforma.', 'Assembleia', 'urgent', 1);

-- ============================================
-- Fim do Script
-- ============================================
