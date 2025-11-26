import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '@/lib/api';
import { mockAuthService } from '@/lib/mockData';

// Usar dados mockados para demonstração
const USE_MOCK_DATA = true;
const authServiceToUse = USE_MOCK_DATA ? mockAuthService : authService;

interface User {
  id: number;
  username: string;
  email: string | null;
  full_name: string;
  group_id: number;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar se há token salvo e carregar dados do usuário
    const loadUser = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const userData = await authServiceToUse.getMe();
          setUser(userData);
        } catch (error) {
          console.error('Erro ao carregar usuário:', error);
          localStorage.removeItem('access_token');
        }
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const response = await authServiceToUse.login(username, password);
      localStorage.setItem('access_token', response.access_token);
      
      // Carregar dados do usuário
      const userData = await authServiceToUse.getMe();
      setUser(userData);
    } catch (error: any) {
      console.error('Erro no login:', error);
      throw new Error(error.response?.data?.detail || 'Erro ao fazer login');
    }
  };

  const logout = async () => {
    try {
      await authServiceToUse.logout();
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    } finally {
      localStorage.removeItem('access_token');
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
