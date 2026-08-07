"use client";

import { useEffect, useState } from "react";
import { Client } from "@stomp/stompjs";
import SockJS from "sockjs-client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Activity } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function LiveMonitoringPage() {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [transactions, setTransactions] = useState<any[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [chartData, setChartData] = useState<any[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "http://localhost:8080/ws";
    
    const stompClient = new Client({
      webSocketFactory: () => new SockJS(wsUrl),
      debug: () => {
        // console.log(str);
      },
      onConnect: () => {
        setIsConnected(true);
        stompClient.subscribe("/topic/live-transactions", (message) => {
          const data = JSON.parse(message.body);
          
          setTransactions((prev) => {
            const newTx = [data, ...prev];
            return newTx.slice(0, 50); // Keep last 50
          });

          setChartData((prev) => {
            const timeStr = new Date().toLocaleTimeString();
            const newPoint = { time: timeStr, score: data.compositeScore };
            const newData = [...prev, newPoint];
            return newData.slice(-20); // Keep last 20 for the chart
          });
        });
      },
    });

    stompClient.activate();
    return () => {
      stompClient.deactivate();
    };
  }, []);

  if (!isMounted) return null;

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Live Monitoring</h1>
        <div className="flex items-center gap-2">
          {isConnected ? (
            <>
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
              </span>
              <span className="text-sm text-muted-foreground">Connected to stream</span>
            </>
          ) : (
            <>
              <span className="relative flex h-3 w-3">
                <span className="relative inline-flex rounded-full h-3 w-3 bg-yellow-500"></span>
              </span>
              <span className="text-sm text-muted-foreground">Connecting...</span>
            </>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="glass md:col-span-2 shadow-lg border-primary/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" />
              Risk Score Trend
            </CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="time" stroke="#666" fontSize={12} tickMargin={10} />
                <YAxis domain={[0, 100]} stroke="#666" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#111', borderColor: '#333' }} />
                <Line type="monotone" dataKey="score" stroke="var(--color-primary)" strokeWidth={3} dot={false} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        
        <Card className="glass shadow-lg border-primary/20">
          <CardHeader>
            <CardTitle>System Health</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center p-3 rounded-lg bg-card/50">
              <span className="text-sm">Model PSI (Drift)</span>
              <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">0.04 - Healthy</Badge>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg bg-card/50">
              <span className="text-sm">Latency</span>
              <span className="text-sm font-mono text-primary">42ms</span>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg bg-card/50">
              <span className="text-sm">Events/sec</span>
              <span className="text-sm font-mono text-primary">0.2</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <h2 className="text-xl font-semibold mt-8 mb-4">Recent Transactions</h2>
      <div className="space-y-4">
        {transactions.length === 0 ? (
          <div className="text-center p-12 text-muted-foreground border border-dashed rounded-lg">
            Waiting for live transactions...
          </div>
        ) : (
          transactions.map((tx, idx) => (
            <Card key={idx} className="glass shadow-sm transition-all hover:shadow-md border-l-4" style={{ borderLeftColor: tx.compositeScore > 80 ? 'var(--color-destructive)' : tx.compositeScore > 60 ? 'orange' : 'green' }}>
              <CardContent className="p-4 flex flex-col md:flex-row gap-4 justify-between md:items-center">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono font-medium text-lg text-primary">{tx.transaction.customerId}</span>
                    <Badge variant="outline" className={tx.compositeScore > 80 ? "border-destructive text-destructive" : ""}>
                      {tx.riskBand} ({tx.compositeScore.toFixed(1)})
                    </Badge>
                  </div>
                  <div className="text-sm text-muted-foreground flex gap-4">
                    <span>${tx.transaction.amount.toFixed(2)}</span>
                    <span>Velocity: {tx.transaction.velocity}</span>
                    <span>{tx.rulesTriggered.length} rules triggered</span>
                  </div>
                </div>
                
                <div className="text-sm md:max-w-md bg-black/20 p-3 rounded-md text-muted-foreground italic border border-white/5">
                  &quot;{tx.narrative}&quot;
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
