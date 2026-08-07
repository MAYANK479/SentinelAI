"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DollarSign, ShieldCheck, ActivitySquare } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const driftData = [
  { day: 'Mon', psi: 0.02 },
  { day: 'Tue', psi: 0.03 },
  { day: 'Wed', psi: 0.04 },
  { day: 'Thu', psi: 0.08 },
  { day: 'Fri', psi: 0.12 },
  { day: 'Sat', psi: 0.05 },
  { day: 'Sun', psi: 0.04 },
];

export default function BusinessImpactPage() {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <h1 className="text-3xl font-bold tracking-tight">Business Impact & Model Health</h1>

      <Card className="glass border-green-500/30 bg-green-500/5 shadow-xl">
        <CardContent className="p-8 flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground mb-1 uppercase tracking-wider">Estimated ROI</p>
            <h2 className="text-4xl font-bold text-green-500 flex items-center gap-2">
              <DollarSign className="w-8 h-8" />
              1,245,800.00
            </h2>
            <p className="text-sm text-green-500/80 mt-2">Net cost saved (30 days) vs. manual review costs.</p>
          </div>
          <div className="hidden md:block">
            <ShieldCheck className="w-24 h-24 text-green-500/20" />
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="glass shadow-lg border-primary/20">
          <CardHeader>
            <CardTitle>Model Metrics (RandomForest)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <span className="font-medium text-sm">PR-AUC</span>
                <span className="font-mono text-primary">0.942</span>
              </div>
              <div className="w-full bg-card h-2 rounded-full overflow-hidden">
                <div className="bg-primary h-full w-[94.2%]"></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="font-medium text-sm">F2-Score</span>
                <span className="font-mono text-primary">0.891</span>
              </div>
              <div className="w-full bg-card h-2 rounded-full overflow-hidden">
                <div className="bg-primary h-full w-[89.1%]"></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="font-medium text-sm">Precision @ Top 100</span>
                <span className="font-mono text-primary">98.0%</span>
              </div>
              <div className="w-full bg-card h-2 rounded-full overflow-hidden">
                <div className="bg-primary h-full w-[98%]"></div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="glass shadow-lg border-primary/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ActivitySquare className="w-5 h-5 text-primary" />
              Data Drift (PSI)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex justify-between items-center mb-6">
              <div>
                <h3 className="text-3xl font-bold">0.04</h3>
                <p className="text-sm text-muted-foreground">Current PSI</p>
              </div>
              <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20 text-sm px-4 py-1">
                Healthy
              </Badge>
            </div>
            <div className="h-[180px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={driftData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="day" stroke="#666" fontSize={12} tickMargin={10} />
                  <Tooltip contentStyle={{ backgroundColor: '#111', borderColor: '#333' }} />
                  <Line type="monotone" dataKey="psi" stroke="var(--color-primary)" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
