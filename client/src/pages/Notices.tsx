import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Plus, Loader2, Bell } from 'lucide-react';
import { noticeService } from '@/lib/api';
import { mockNoticeService } from '@/lib/mockData';

const USE_MOCK_DATA = true;
const service = USE_MOCK_DATA ? mockNoticeService : noticeService;

export default function Notices() {
  const [notices, setNotices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadNotices();
  }, []);

  const loadNotices = async () => {
    try {
      setLoading(true);
      const data = await service.getBoard();
      setNotices(data);
    } catch (error) {
      console.error('Erro ao carregar avisos:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityBadge = (priority: string) => {
    const variants: Record<string, { label: string; className: string }> = {
      low: { label: 'Baixa', className: 'bg-gray-100 text-gray-800' },
      medium: { label: 'Média', className: 'bg-blue-100 text-blue-800' },
      high: { label: 'Alta', className: 'bg-orange-100 text-orange-800' },
      urgent: { label: 'Urgente', className: 'bg-red-100 text-red-800' },
    };

    const variant = variants[priority] || variants.medium;
    return (
      <Badge className={`${variant.className} hover:${variant.className}`}>
        {variant.label}
      </Badge>
    );
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Quadro de Avisos</h1>
            <p className="text-gray-500 mt-1">Avisos e comunicados do condomínio</p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Novo Aviso
          </Button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {notices.map((notice) => (
              <Card key={notice.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-blue-50 rounded-lg">
                        <Bell className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">{notice.title}</CardTitle>
                        <CardDescription className="mt-1">
                          {new Date(notice.created_at).toLocaleDateString('pt-BR')}
                        </CardDescription>
                      </div>
                    </div>
                    {getPriorityBadge(notice.priority)}
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 whitespace-pre-wrap">
                    {notice.content}
                  </p>
                  <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
                    <span>Autor: Usuário {notice.author_id}</span>
                    {notice.expiration_date && (
                      <span>
                        Expira em: {new Date(notice.expiration_date).toLocaleDateString('pt-BR')}
                      </span>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {!loading && notices.length === 0 && (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Bell className="h-12 w-12 text-gray-300 mb-4" />
              <p className="text-gray-500">Nenhum aviso ativo no momento</p>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
