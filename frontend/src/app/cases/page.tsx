"use client";

import { useState } from "react";
import Link from "next/link";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const mockCases = [
  { id: "CASE-001", customerId: "CUST_0481", amount: 1250.0, status: "OPEN", riskBand: "Fraud", score: 92.4, time: "2 mins ago" },
  { id: "CASE-002", customerId: "CUST_0112", amount: 840.5, status: "ASSIGNED", riskBand: "Fraud", score: 85.1, time: "15 mins ago" },
  { id: "CASE-003", customerId: "CUST_0991", amount: 45.0, status: "OPEN", riskBand: "Suspicious", score: 71.0, time: "1 hour ago" },
  { id: "CASE-004", customerId: "CUST_0344", amount: 3200.0, status: "UNDER_INVESTIGATION", riskBand: "Fraud", score: 98.9, time: "3 hours ago" },
  { id: "CASE-005", customerId: "CUST_0112", amount: 15.0, status: "FALSE_POSITIVE", riskBand: "Suspicious", score: 62.0, time: "1 day ago" },
];

export default function CasesPage() {
  const [cases] = useState(mockCases);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "OPEN": return "bg-red-500/10 text-red-500 border-red-500/20";
      case "ASSIGNED": return "bg-blue-500/10 text-blue-500 border-blue-500/20";
      case "UNDER_INVESTIGATION": return "bg-purple-500/10 text-purple-500 border-purple-500/20";
      case "FALSE_POSITIVE": return "bg-gray-500/10 text-gray-500 border-gray-500/20";
      case "RESOLVED": return "bg-green-500/10 text-green-500 border-green-500/20";
      default: return "bg-gray-500/10 text-gray-500 border-gray-500/20";
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Case Management</h1>
        <Button variant="outline" className="border-primary/50 hover:bg-primary/20">Assign Next Case</Button>
      </div>

      <div className="glass rounded-xl overflow-hidden border border-border/50">
        <Table>
          <TableHeader className="bg-black/20">
            <TableRow className="border-border/50 hover:bg-transparent">
              <TableHead>Case ID</TableHead>
              <TableHead>Customer</TableHead>
              <TableHead>Amount</TableHead>
              <TableHead>Risk Score</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Time</TableHead>
              <TableHead className="text-right">Action</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {cases.map((c) => (
              <TableRow key={c.id} className="border-border/50 hover:bg-primary/5 transition-colors">
                <TableCell className="font-medium text-primary">{c.id}</TableCell>
                <TableCell className="font-mono">{c.customerId}</TableCell>
                <TableCell>${c.amount.toFixed(2)}</TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span className={c.score > 80 ? "text-destructive font-bold" : "text-orange-400 font-bold"}>
                      {c.score.toFixed(1)}
                    </span>
                    <span className="text-xs text-muted-foreground">({c.riskBand})</span>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant="outline" className={getStatusColor(c.status)}>
                    {c.status.replace("_", " ")}
                  </Badge>
                </TableCell>
                <TableCell className="text-muted-foreground text-sm">{c.time}</TableCell>
                <TableCell className="text-right">
                  <Link href={`/cases/${c.id}`}>
                    <Button size="sm" className="bg-primary/20 text-primary hover:bg-primary hover:text-primary-foreground transition-all">
                      Investigate
                    </Button>
                  </Link>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
