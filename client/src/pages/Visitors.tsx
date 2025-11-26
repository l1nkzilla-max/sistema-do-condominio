import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Plus, Loader2 } from 'lucide-react';
import { visitorService } from '@/lib/api';
import { mockVisitorService } from '@/lib/mockData';

const USE_MOCK_DATA = true;
const service = USE_MOCK_DATA ? mockVisitorService : visitorService;

export default function Visitors() {
  const [visitors, setVisitors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVisitors();
  }, []);

  const loadVisitors = async () => {
    try {
      setLoading(true);
      const data = await service.list();
      setVisitors(data);
    } catch (error) {
      console.error('Erro ao carregar visitantes:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Controle de Visitantes</h1>
            <p className="text-gray-500 mt-1">Registro de entrada e saída de visitantes</p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Registrar Visitante
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Lista de Visitantes</CardTitle>
            <CardDescription>{visitors.length} visitante(s) registrado(s)</CardDescription>
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
                    <TableHead>Nome</TableHead>
                    <TableHead>Documento</TableHead>
                    <TableHead>Unidade</TableHead>
                    <TableHead>Entrada</TableHead>
                    <TableHead>Saída</TableHead>
                    <TableHead>Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {visitors.map((visitor) => (
                    <TableRow key={visitor.id}>
                      <TableCell className="font-medium">{visitor.name}</TableCell>
                      <TableCell>{visitor.document}</TableCell>
                      <TableCell>Unidade {visitor.unit_id}</TableCell>
                      <TableCell>{new Date(visitor.entry_datetime).toLocaleString('pt-BR')}</TableCell>
                      <TableCell>
                        {visitor.exit_datetime
                          ? new Date(visitor.exit_datetime).toLocaleString('pt-BR')
                          : '-'}
                      </TableCell>
                      <TableCell>
                        {visitor.exit_datetime ? (
                          <Badge variant="secondary">Saiu</Badge>
                        ) : (
                          <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
                            No condomínio
                          </Badge>
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
