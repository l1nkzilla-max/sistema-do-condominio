import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Calendar, Bell, UserCheck } from 'lucide-react';
import { userService, schedulingService, noticeService, visitorService } from '@/lib/api';
import { mockUserService, mockSchedulingService, mockNoticeService, mockVisitorService } from '@/lib/mockData';

// Usar dados mockados para demonstração
const USE_MOCK_DATA = true;
const services = USE_MOCK_DATA ? {
  user: mockUserService,
  scheduling: mockSchedulingService,
  notice: mockNoticeService,
  visitor: mockVisitorService,
} : {
  user: userService,
  scheduling: schedulingService,
  notice: noticeService,
  visitor: visitorService,
};

export default function Dashboard() {
  const [stats, setStats] = useState({
    users: 0,
    schedulings: 0,
    notices: 0,
    visitors: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const [users, schedulings, notices, visitors] = await Promise.all([
          services.user.list(0, 1000),
          services.scheduling.list(),
          services.notice.list(),
          services.visitor.list(),
        ]);

        setStats({
          users: users.length,
          schedulings: schedulings.length,
          notices: notices.length,
          visitors: visitors.length,
        });
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  const cards = [
    {
      title: 'Usuários',
      value: stats.users,
      description: 'Total de usuários cadastrados',
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Agendamentos',
      value: stats.schedulings,
      description: 'Agendamentos de áreas comuns',
      icon: Calendar,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Avisos',
      value: stats.notices,
      description: 'Avisos ativos',
      icon: Bell,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
    },
    {
      title: 'Visitantes',
      value: stats.visitors,
      description: 'Visitantes registrados',
      icon: UserCheck,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">Visão geral do sistema de condomínio</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {cards.map((card) => {
            const Icon = card.icon;
            return (
              <Card key={card.title}>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">
                    {card.title}
                  </CardTitle>
                  <div className={`p-2 rounded-lg ${card.bgColor}`}>
                    <Icon className={`h-5 w-5 ${card.color}`} />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-gray-900">
                    {loading ? '...' : card.value}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{card.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Bem-vindo ao Sistema de Condomínio</CardTitle>
              <CardDescription>
                Gerencie seu condomínio de forma eficiente
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-sm text-gray-600">
                  Este sistema permite gerenciar todos os aspectos do seu condomínio:
                </p>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600" />
                    Controle de usuários e permissões
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600" />
                    Agendamento de áreas comuns
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600" />
                    Sistema de avisos e comunicados
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600" />
                    Controle de visitantes
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600" />
                    Gestão de orçamentos e patrimônio
                  </li>
                </ul>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Acesso Rápido</CardTitle>
              <CardDescription>
                Atalhos para as funcionalidades mais usadas
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-3">
                <a
                  href="/users"
                  className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                >
                  <Users className="h-6 w-6 text-blue-600 mb-2" />
                  <p className="text-sm font-medium">Usuários</p>
                </a>
                <a
                  href="/schedulings"
                  className="p-4 border border-gray-200 rounded-lg hover:border-green-300 hover:bg-green-50 transition-colors"
                >
                  <Calendar className="h-6 w-6 text-green-600 mb-2" />
                  <p className="text-sm font-medium">Agendamentos</p>
                </a>
                <a
                  href="/notices"
                  className="p-4 border border-gray-200 rounded-lg hover:border-yellow-300 hover:bg-yellow-50 transition-colors"
                >
                  <Bell className="h-6 w-6 text-yellow-600 mb-2" />
                  <p className="text-sm font-medium">Avisos</p>
                </a>
                <a
                  href="/visitors"
                  className="p-4 border border-gray-200 rounded-lg hover:border-purple-300 hover:bg-purple-50 transition-colors"
                >
                  <UserCheck className="h-6 w-6 text-purple-600 mb-2" />
                  <p className="text-sm font-medium">Visitantes</p>
                </a>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
