import DashboardLayout from '@/components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText } from 'lucide-react';

export default function Audit() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Auditoria</h1>
          <p className="text-gray-500 mt-1">Logs e auditoria do sistema</p>
        </div>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Logs de Auditoria
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
