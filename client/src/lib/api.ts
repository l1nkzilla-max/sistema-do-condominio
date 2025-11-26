/**
 * API Service - Comunicação com microserviços Python/FastAPI
 */
import axios, { AxiosInstance, AxiosError } from 'axios';

// URLs base dos microserviços
const AUTH_SERVICE_URL = import.meta.env.VITE_AUTH_SERVICE_URL || 'http://localhost:8001';
const MANAGEMENT_SERVICE_URL = import.meta.env.VITE_MANAGEMENT_SERVICE_URL || 'http://localhost:8002';
const OPERATIONS_SERVICE_URL = import.meta.env.VITE_OPERATIONS_SERVICE_URL || 'http://localhost:8003';

// Criar instâncias axios para cada microserviço
const createApiInstance = (baseURL: string): AxiosInstance => {
  const instance = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Interceptor para adicionar token JWT
  instance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Interceptor para tratar erros
  instance.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      if (error.response?.status === 401) {
        // Token expirado ou inválido
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );

  return instance;
};

export const authApi = createApiInstance(AUTH_SERVICE_URL);
export const managementApi = createApiInstance(MANAGEMENT_SERVICE_URL);
export const operationsApi = createApiInstance(OPERATIONS_SERVICE_URL);

// ========== Auth Service APIs ==========

export const authService = {
  login: async (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await authApi.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  getMe: async () => {
    const response = await authApi.get('/api/auth/me');
    return response.data;
  },

  logout: async () => {
    const response = await authApi.post('/api/auth/logout');
    return response.data;
  },
};

export const userService = {
  list: async (skip = 0, limit = 100) => {
    const response = await authApi.get('/api/users', { params: { skip, limit } });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await authApi.get(`/api/users/${id}`);
    return response.data;
  },

  create: async (data: any) => {
    const response = await authApi.post('/api/users', data);
    return response.data;
  },

  update: async (id: number, data: any) => {
    const response = await authApi.put(`/api/users/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    const response = await authApi.delete(`/api/users/${id}`);
    return response.data;
  },
};

export const groupService = {
  list: async () => {
    const response = await authApi.get('/api/groups');
    return response.data;
  },

  create: async (data: any) => {
    const response = await authApi.post('/api/groups', data);
    return response.data;
  },
};

export const condominiumService = {
  list: async () => {
    const response = await authApi.get('/api/condominiums');
    return response.data;
  },
};

export const unitService = {
  list: async (condominiumId?: number) => {
    const response = await authApi.get('/api/units', {
      params: condominiumId ? { condominium_id: condominiumId } : {},
    });
    return response.data;
  },
};

// ========== Management Service APIs ==========

export const providerService = {
  list: async () => {
    const response = await managementApi.get('/api/providers');
    return response.data;
  },

  create: async (data: any) => {
    const response = await managementApi.post('/api/providers', data);
    return response.data;
  },

  delete: async (id: number) => {
    const response = await managementApi.delete(`/api/providers/${id}`);
    return response.data;
  },
};

export const employeeService = {
  list: async () => {
    const response = await managementApi.get('/api/employees');
    return response.data;
  },

  create: async (data: any) => {
    const response = await managementApi.post('/api/employees', data);
    return response.data;
  },
};

export const patrimonyService = {
  list: async () => {
    const response = await managementApi.get('/api/patrimony');
    return response.data;
  },

  create: async (data: any) => {
    const response = await managementApi.post('/api/patrimony', data);
    return response.data;
  },
};

// ========== Operations Service APIs ==========

export const areaService = {
  list: async () => {
    const response = await operationsApi.get('/api/areas');
    return response.data;
  },

  create: async (data: any) => {
    const response = await operationsApi.post('/api/areas', data);
    return response.data;
  },
};

export const schedulingService = {
  list: async () => {
    const response = await operationsApi.get('/api/schedulings');
    return response.data;
  },

  create: async (data: any) => {
    const response = await operationsApi.post('/api/schedulings', data);
    return response.data;
  },

  approve: async (id: number, approvedBy: number) => {
    const response = await operationsApi.put(`/api/schedulings/${id}/approve`, null, {
      params: { approved_by: approvedBy },
    });
    return response.data;
  },
};

export const budgetService = {
  list: async () => {
    const response = await operationsApi.get('/api/budgets');
    return response.data;
  },

  create: async (data: any) => {
    const response = await operationsApi.post('/api/budgets', data);
    return response.data;
  },

  getHistory: async (id: number) => {
    const response = await operationsApi.get(`/api/budgets/${id}/history`);
    return response.data;
  },
};

export const noticeService = {
  list: async () => {
    const response = await operationsApi.get('/api/notices');
    return response.data;
  },

  getBoard: async () => {
    const response = await operationsApi.get('/api/notice-board');
    return response.data;
  },

  create: async (data: any) => {
    const response = await operationsApi.post('/api/notices', data);
    return response.data;
  },
};

export const visitorService = {
  list: async () => {
    const response = await operationsApi.get('/api/visitors');
    return response.data;
  },

  create: async (data: any) => {
    const response = await operationsApi.post('/api/visitors', data);
    return response.data;
  },

  registerExit: async (id: number) => {
    const response = await operationsApi.put(`/api/visitors/${id}/exit`);
    return response.data;
  },
};

export const eventService = {
  list: async () => {
    const response = await operationsApi.get('/api/events');
    return response.data;
  },

  create: async (data: any) => {
    const response = await operationsApi.post('/api/events', data);
    return response.data;
  },
};

export const auditService = {
  getLogs: async (skip = 0, limit = 50) => {
    const response = await operationsApi.get('/api/logs', { params: { skip, limit } });
    return response.data;
  },

  getAudit: async (filters: any = {}) => {
    const response = await operationsApi.get('/api/audit', { params: filters });
    return response.data;
  },
};
