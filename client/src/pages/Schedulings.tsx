import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Plus, Loader2, Check, X } from 'lucide-react';
import { schedulingService } from '@/lib/api';
import { mockSchedulingService } from '@/lib/mockData';

const USE_MOCK_DATA = true;
const service = USE_MOCK_DATA ? mockSchedulingService : schedulingService;
import { useAuth } from '@/contexts/AuthContext';

export default function Schedulings() {
  const [schedulings, setSchedulings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    loadSchedulings();
  }, []);

  const loadSchedulings = async () => {
    try {
      setLoading(true);
      const data = await service.list();
      setSchedulings(data);
    } catch (error) {
      console.error('Erro ao carregar agendamentos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: number) => {
    try {
      await service.approve(id, user?.id || 1);
      loadSchedulings();
    } catch (error) {
      console.error('Erro ao aprovar agendamento:', error);
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: Record<string, { label: string; className: string }> = {
      pending: { label: 'Pendente', className: 'bg-yellow-100 text-yellow-800' },
      approved: { label: 'Aprovado', className: 'bg-green-100 text-green-800' },
      rejected: { label: 'Rejeitado', className: 'bg-red-100 text-red-800' },
    };

    const variant = variants[status] || variants.pending;
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
            <h1 className="text-3xl font-bold text-gray-900">Agendamentos</h1>
            <p className="text-gray-500 mt-1">Gerenciar agendamentos de áreas comuns</p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Novo Agendamento
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Lista de Agendamentos</CardTitle>
            <CardDescription>
              {schedulings.length} agendamento(s) registrado(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>ID</TableHead>
                    <TableHead>Área</TableHead>
                    <TableHead>Unidade</TableHead>
                    <TableHead>Data/Hora Início</TableHead>
                    <TableHead>Data/Hora Fim</TableHead>
                    <TableHead>Finalidade</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {schedulings.map((scheduling) => (
                    <TableRow key={scheduling.id}>
                      <TableCell className="font-medium">{scheduling.id}</TableCell>
                      <TableCell>Área {scheduling.area_id}</TableCell>
                      <TableCell>Unidade {scheduling.unit_id}</TableCell>
                      <TableCell>
                        {new Date(scheduling.start_datetime).toLocaleString('pt-BR')}
                      </TableCell>
                      <TableCell>
                        {new Date(scheduling.end_datetime).toLocaleString('pt-BR')}
                      </TableCell>
                      <TableCell>{scheduling.purpose || '-'}</TableCell>
                      <TableCell>{getStatusBadge(scheduling.status)}</TableCell>
                      <TableCell>
                        {scheduling.status === 'pending' && (
                          <Button
                            size="sm"
                            onClick={() => handleApprove(scheduling.id)}
                            className="bg-green-600 hover:bg-green-700"
                          >
                            <Check className="h-4 w-4 mr-1" />
                            Aprovar
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
