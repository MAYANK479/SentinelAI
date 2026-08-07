"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Save, Settings2 } from "lucide-react";

const initialRules = [
  { id: 1, name: "High Amount", condition: "tx.amount > 1000", weight: 30.0 },
  { id: 2, name: "Extreme Velocity", condition: "tx.velocity > 10", weight: 40.0 },
  { id: 3, name: "Geographic Jump", condition: "tx.geoJump == 1", weight: 50.0 },
  { id: 4, name: "New Device + High Value", condition: "tx.newDevice == 1 && tx.amount > 500", weight: 45.0 },
  { id: 5, name: "VPN Used", condition: "tx.vpnUsed == 1", weight: 20.0 },
  { id: 6, name: "High Spend Deviation", condition: "tx.spendDeviation > 4.0", weight: 35.0 },
];

export default function RulesPage() {
  const [rules, setRules] = useState(initialRules);
  const [wMl, setWMl] = useState([50]);
  const [wRule, setWRule] = useState([30]);
  const [wBehavior, setWBehavior] = useState([20]);

  const handleWeightChange = (id: number, val: number[]) => {
    setRules(rules.map(r => r.id === id ? { ...r, weight: val[0] } : r));
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Rule & Risk Engine Configuration</h1>
          <p className="text-muted-foreground mt-1">Configure heuristic rules and composite risk weights.</p>
        </div>
        <Button className="gap-2"><Save className="w-4 h-4" /> Save Configuration</Button>
      </div>

      <Card className="glass shadow-lg border-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings2 className="w-5 h-5 text-primary" />
            Composite Risk Formula Weights
          </CardTitle>
          <CardDescription>
            Risk = (ML × W_ml) + (Rules × W_rule) + (Behavior × W_behavior)
          </CardDescription>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-4">
          <div className="space-y-4">
            <div className="flex justify-between">
              <label className="text-sm font-medium">Machine Learning Weight</label>
              <span className="text-sm font-mono text-primary">{wMl[0]}%</span>
            </div>
            <Slider value={wMl} onValueChange={(val) => setWMl(val as number[])} max={100} step={1} />
          </div>
          <div className="space-y-4">
            <div className="flex justify-between">
              <label className="text-sm font-medium">Heuristic Rule Weight</label>
              <span className="text-sm font-mono text-primary">{wRule[0]}%</span>
            </div>
            <Slider value={wRule} onValueChange={(val) => setWRule(val as number[])} max={100} step={1} />
          </div>
          <div className="space-y-4">
            <div className="flex justify-between">
              <label className="text-sm font-medium">Behavioral Deviation Weight</label>
              <span className="text-sm font-mono text-primary">{wBehavior[0]}%</span>
            </div>
            <Slider value={wBehavior} onValueChange={(val) => setWBehavior(val as number[])} max={100} step={1} />
          </div>
        </CardContent>
      </Card>

      <div>
        <h2 className="text-xl font-semibold mb-4">Active Heuristic Rules</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {rules.map((rule) => (
            <Card key={rule.id} className="glass shadow-sm border-border/50">
              <CardContent className="p-5 flex flex-col gap-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-primary">{rule.name}</h3>
                    <code className="text-xs text-muted-foreground bg-black/20 px-2 py-1 rounded mt-1 inline-block">
                      {rule.condition}
                    </code>
                  </div>
                  <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">
                    Active
                  </Badge>
                </div>
                
                <div className="space-y-3 mt-2">
                  <div className="flex justify-between">
                    <label className="text-sm text-muted-foreground">Penalty Weight</label>
                    <span className="text-sm font-mono font-medium">+{rule.weight} points</span>
                  </div>
                  <Slider 
                    value={[rule.weight]} 
                    onValueChange={(val) => handleWeightChange(rule.id, val as number[])} 
                    max={100} 
                    step={5} 
                  />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
