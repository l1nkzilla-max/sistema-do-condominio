import DashboardLayout from '@/components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { DollarSign } from 'lucide-react';

export default function Budgets() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Orçamentos</h1>
          <p className="text-gray-500 mt-1">Gerenciar orçamentos de compra e serviço</p>
        </div>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="h-5 w-5" />
              Orçamentos
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">Funcionalidade em desenvolvimento...</p>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
