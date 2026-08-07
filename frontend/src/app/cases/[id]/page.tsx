"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowLeft, ShieldAlert, CheckCircle2, AlertTriangle, ExternalLink } from "lucide-react";
import Link from "next/link";
import { ReactFlow, Background, Controls } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

const initialNodes = [
  { id: '1', position: { x: 250, y: 50 }, data: { label: 'Customer: CUST_0481' }, style: { background: 'var(--color-primary)', color: 'white', borderRadius: '8px', padding: '10px 20px', boxShadow: '0 4px 15px rgba(0,0,0,0.5)', border: 'none' } },
  { id: '2', position: { x: 100, y: 150 }, data: { label: 'Device: Mac M3 (New)' }, style: { background: 'var(--color-card)', color: 'white', border: '1px solid var(--color-border)', borderRadius: '8px', padding: '10px 20px' } },
  { id: '3', position: { x: 400, y: 150 }, data: { label: 'Location: VPN IP (RU)' }, style: { background: 'var(--color-destructive)', color: 'white', border: '1px solid var(--color-destructive)', borderRadius: '8px', padding: '10px 20px', boxShadow: '0 0 15px rgba(255,0,0,0.3)' } },
  { id: '4', position: { x: 250, y: 250 }, data: { label: 'Tx: $1,250.00' }, style: { background: 'var(--color-accent)', color: 'white', borderRadius: '8px', padding: '10px 20px' } },
];
const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#888', strokeWidth: 2 } },
  { id: 'e1-3', source: '1', target: '3', animated: true, style: { stroke: 'var(--color-destructive)', strokeWidth: 3 } },
  { id: 'e2-4', source: '2', target: '4', animated: true, style: { stroke: '#888', strokeWidth: 2 } },
  { id: 'e3-4', source: '3', target: '4', animated: true, style: { stroke: 'var(--color-destructive)', strokeWidth: 3 } },
];

export default function CaseDetailsPage() {
  const params = useParams();
  const caseId = params.id as string;
  const [status, setStatus] = useState("OPEN");

  const narrative = "Flagged due to high contribution from VPNUsed (0.28 influence) and significant deviation from 30-day historical baseline. The model assigns a 92.4% fraud probability. Recommend hold + verify device and customer identity.";

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex items-center gap-4">
        <Link href="/cases">
          <Button variant="ghost" size="icon" className="rounded-full hover:bg-primary/20">
            <ArrowLeft className="w-5 h-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-3">
            Case: {caseId}
            <Badge variant="outline" className={status === "OPEN" ? "bg-red-500/10 text-red-500 border-red-500/20" : "bg-green-500/10 text-green-500 border-green-500/20"}>
              {status}
            </Badge>
          </h1>
          <p className="text-muted-foreground">Customer: CUST_0481 | Composite Score: 92.4 (Fraud)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Panel: Graph */}
        <Card className="glass shadow-lg lg:col-span-2 overflow-hidden flex flex-col border-primary/20">
          <CardHeader className="bg-black/10 border-b border-border/50 pb-4">
            <CardTitle className="text-lg">Entity Graph</CardTitle>
          </CardHeader>
          <CardContent className="p-0 flex-1 min-h-[400px] relative bg-black/20">
            <ReactFlow nodes={initialNodes} edges={initialEdges} fitView>
              <Background color="#333" gap={16} />
              <Controls className="bg-card border-border fill-primary" />
            </ReactFlow>
          </CardContent>
        </Card>

        {/* Right Panel: Narrative & Actions */}
        <div className="space-y-6">
          <Card className="glass shadow-lg border-primary/20">
            <CardHeader className="bg-black/10 border-b border-border/50">
              <CardTitle className="text-lg flex items-center gap-2">
                <ShieldAlert className="w-5 h-5 text-primary" />
                AI Narrative
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <p className="text-muted-foreground leading-relaxed italic border-l-4 border-primary pl-4">
                "{narrative}"
              </p>
              
              <div className="mt-6 space-y-3">
                <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">Analyst Actions</h4>
                <Button 
                  className="w-full justify-start gap-2 bg-destructive/20 text-destructive hover:bg-destructive hover:text-destructive-foreground border border-destructive/50"
                  onClick={() => setStatus("FREEZE_APPLIED")}
                >
                  <AlertTriangle className="w-4 h-4" /> Freeze Account
                </Button>
                <Button 
                  className="w-full justify-start gap-2 bg-primary/20 text-primary hover:bg-primary hover:text-primary-foreground border border-primary/50"
                  onClick={() => setStatus("ESCALATED")}
                >
                  <ExternalLink className="w-4 h-4" /> Escalate to L2
                </Button>
                <Button 
                  className="w-full justify-start gap-2 bg-green-500/20 text-green-500 hover:bg-green-500 hover:text-white border border-green-500/50"
                  onClick={() => setStatus("FALSE_POSITIVE")}
                >
                  <CheckCircle2 className="w-4 h-4" /> Mark False Positive
                </Button>
              </div>
            </CardContent>
          </Card>
          
          <Card className="glass shadow-lg border-primary/20">
            <CardHeader className="bg-black/10 border-b border-border/50">
              <CardTitle className="text-lg">SHAP Contributions</CardTitle>
            </CardHeader>
            <CardContent className="pt-4 space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>VPNUsed</span>
                  <span className="text-destructive font-mono">+0.28</span>
                </div>
                <div className="h-2 w-full bg-card rounded-full overflow-hidden">
                  <div className="h-full bg-destructive w-[80%] rounded-full"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>NewDevice</span>
                  <span className="text-destructive font-mono">+0.15</span>
                </div>
                <div className="h-2 w-full bg-card rounded-full overflow-hidden">
                  <div className="h-full bg-destructive w-[45%] rounded-full"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Velocity</span>
                  <span className="text-green-500 font-mono">-0.05</span>
                </div>
                <div className="h-2 w-full bg-card rounded-full overflow-hidden flex justify-end">
                  <div className="h-full bg-green-500 w-[15%] rounded-full"></div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
