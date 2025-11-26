/**
 * Dados mockados para demonstração do sistema sem microserviços Python
 */

// Simular delay de rede
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Dados de usuários
const mockUsers = [
  {
    id: 1,
    username: 'guilherme',
    email: 'l1nkzilla@icloud.com',
    full_name: 'Guilherme Henrique',
    group_id: 1,
    is_active: true,
    last_login: new Date('2025-11-26T20:08:00').toISOString(),
  },
  {
    id: 2,
    username: 'joao.silva',
    email: 'joao.silva@email.com',
    full_name: 'João Silva',
    group_id: 2,
    is_active: true,
    last_login: new Date('2025-11-25T15:20:00').toISOString(),
  },
  {
    id: 3,
    username: 'maria.santos',
    email: 'maria.santos@email.com',
    full_name: 'Maria Santos',
    group_id: 2,
    is_active: true,
    last_login: new Date('2025-11-24T09:15:00').toISOString(),
  },
  {
    id: 4,
    username: 'pedro.oliveira',
    email: 'pedro.oliveira@email.com',
    full_name: 'Pedro Oliveira',
    group_id: 3,
    is_active: false,
    last_login: new Date('2025-11-20T14:45:00').toISOString(),
  },
];

// Dados de agendamentos
const mockSchedulings = [
  {
    id: 1,
    area_id: 1,
    unit_id: 101,
    user_id: 2,
    start_datetime: new Date('2025-12-01T14:00:00').toISOString(),
    end_datetime: new Date('2025-12-01T18:00:00').toISOString(),
    purpose: 'Festa de aniversário',
    status: 'approved',
    approved_by: 1,
  },
  {
    id: 2,
    area_id: 2,
    unit_id: 205,
    user_id: 3,
    start_datetime: new Date('2025-12-05T10:00:00').toISOString(),
    end_datetime: new Date('2025-12-05T12:00:00').toISOString(),
    purpose: 'Reunião de família',
    status: 'pending',
    approved_by: null,
  },
  {
    id: 3,
    area_id: 1,
    unit_id: 303,
    user_id: 2,
    start_datetime: new Date('2025-12-10T19:00:00').toISOString(),
    end_datetime: new Date('2025-12-10T23:00:00').toISOString(),
    purpose: 'Confraternização',
    status: 'pending',
    approved_by: null,
  },
];

// Dados de avisos
const mockNotices = [
  {
    id: 1,
    title: 'Manutenção do Elevador',
    content: 'Informamos que o elevador do bloco A passará por manutenção preventiva no dia 30/11. Pedimos a compreensão de todos.',
    priority: 'high',
    author_id: 1,
    created_at: new Date('2025-11-20T08:00:00').toISOString(),
    expiration_date: new Date('2025-11-30T23:59:59').toISOString(),
    is_active: true,
  },
  {
    id: 2,
    title: 'Assembleia Geral',
    content: 'Convocamos todos os condôminos para a Assembleia Geral Ordinária que será realizada no dia 15/12 às 19h no salão de festas.',
    priority: 'urgent',
    author_id: 1,
    created_at: new Date('2025-11-22T10:00:00').toISOString(),
    expiration_date: new Date('2025-12-15T23:59:59').toISOString(),
    is_active: true,
  },
  {
    id: 3,
    title: 'Horário da Piscina',
    content: 'A piscina estará aberta de segunda a domingo das 8h às 20h. Lembramos que é obrigatório o uso de touca.',
    priority: 'medium',
    author_id: 1,
    created_at: new Date('2025-11-15T12:00:00').toISOString(),
    expiration_date: null,
    is_active: true,
  },
  {
    id: 4,
    title: 'Coleta Seletiva',
    content: 'A coleta seletiva ocorre todas as terças e quintas-feiras. Separe corretamente seu lixo reciclável.',
    priority: 'low',
    author_id: 1,
    created_at: new Date('2025-11-10T09:00:00').toISOString(),
    expiration_date: null,
    is_active: true,
  },
];

// Dados de visitantes
const mockVisitors = [
  {
    id: 1,
    name: 'Carlos Mendes',
    document: '123.456.789-00',
    unit_id: 101,
    entry_datetime: new Date('2025-11-26T14:30:00').toISOString(),
    exit_datetime: new Date('2025-11-26T17:45:00').toISOString(),
    purpose: 'Visita social',
  },
  {
    id: 2,
    name: 'Ana Paula Costa',
    document: '987.654.321-00',
    unit_id: 205,
    entry_datetime: new Date('2025-11-26T10:15:00').toISOString(),
    exit_datetime: null,
    purpose: 'Entrega de encomenda',
  },
  {
    id: 3,
    name: 'Roberto Lima',
    document: '456.789.123-00',
    unit_id: 303,
    entry_datetime: new Date('2025-11-26T09:00:00').toISOString(),
    exit_datetime: null,
    purpose: 'Manutenção',
  },
];

// Serviços mockados
export const mockAuthService = {
  login: async (username: string, password: string) => {
    await delay(500);
    // Aceitar guilherme, admin ou email como usuário
    const validUsernames = ['guilherme', 'admin', 'l1nkzilla@icloud.com', 'Dslink82@hotmail.com'];
    if (validUsernames.includes(username) && password === 'admin123') {
      return {
        access_token: 'mock-jwt-token-12345',
        token_type: 'bearer',
      };
    }
    throw new Error('Credenciais inválidas');
  },

  getMe: async () => {
    await delay(300);
    return mockUsers[0];
  },

  logout: async () => {
    await delay(200);
    return { success: true };
  },
};

export const mockUserService = {
  list: async () => {
    await delay(400);
    return mockUsers;
  },

  getById: async (id: number) => {
    await delay(300);
    return mockUsers.find(u => u.id === id);
  },

  create: async (data: any) => {
    await delay(500);
    const newUser = {
      id: mockUsers.length + 1,
      ...data,
      is_active: true,
      last_login: null,
    };
    mockUsers.push(newUser);
    return newUser;
  },

  update: async (id: number, data: any) => {
    await delay(400);
    const index = mockUsers.findIndex(u => u.id === id);
    if (index !== -1) {
      mockUsers[index] = { ...mockUsers[index], ...data };
      return mockUsers[index];
    }
    throw new Error('Usuário não encontrado');
  },

  delete: async (id: number) => {
    await delay(300);
    const index = mockUsers.findIndex(u => u.id === id);
    if (index !== -1) {
      mockUsers.splice(index, 1);
      return { success: true };
    }
    throw new Error('Usuário não encontrado');
  },
};

export const mockSchedulingService = {
  list: async () => {
    await delay(400);
    return mockSchedulings;
  },

  create: async (data: any) => {
    await delay(500);
    const newScheduling = {
      id: mockSchedulings.length + 1,
      ...data,
      status: 'pending',
      approved_by: null,
    };
    mockSchedulings.push(newScheduling);
    return newScheduling;
  },

  approve: async (id: number, approvedBy: number) => {
    await delay(400);
    const scheduling = mockSchedulings.find(s => s.id === id);
    if (scheduling) {
      scheduling.status = 'approved';
      scheduling.approved_by = approvedBy;
      return scheduling;
    }
    throw new Error('Agendamento não encontrado');
  },
};

export const mockNoticeService = {
  list: async () => {
    await delay(400);
    return mockNotices;
  },

  getBoard: async () => {
    await delay(400);
    return mockNotices.filter(n => n.is_active);
  },

  create: async (data: any) => {
    await delay(500);
    const newNotice = {
      id: mockNotices.length + 1,
      ...data,
      created_at: new Date().toISOString(),
      is_active: true,
    };
    mockNotices.push(newNotice);
    return newNotice;
  },
};

export const mockVisitorService = {
  list: async () => {
    await delay(400);
    return mockVisitors;
  },

  create: async (data: any) => {
    await delay(500);
    const newVisitor = {
      id: mockVisitors.length + 1,
      ...data,
      entry_datetime: new Date().toISOString(),
      exit_datetime: null,
    };
    mockVisitors.push(newVisitor);
    return newVisitor;
  },

  registerExit: async (id: number) => {
    await delay(400);
    const visitor = mockVisitors.find(v => v.id === id);
    if (visitor) {
      visitor.exit_datetime = new Date().toISOString();
      return visitor;
    }
    throw new Error('Visitante não encontrado');
  },
};
