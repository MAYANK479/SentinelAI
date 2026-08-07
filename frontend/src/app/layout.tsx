import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { Activity, LayoutDashboard, ShieldAlert, Settings } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SentinelAI Fraud Intelligence",
  description: "Enterprise-grade real-time transaction monitoring",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} flex h-screen overflow-hidden`}>
        {/* Sidebar */}
        <aside className="w-64 glass border-r flex flex-col">
          <div className="p-6 border-b border-border/50">
            <h1 className="text-xl font-bold flex items-center gap-2 text-primary">
              <ShieldAlert className="w-6 h-6" />
              SentinelAI
            </h1>
          </div>
          <nav className="flex-1 p-4 space-y-2">
            <Link href="/" className="flex items-center gap-3 px-4 py-3 rounded-md hover:bg-primary/20 text-sm font-medium transition-colors">
              <LayoutDashboard className="w-5 h-5 text-muted-foreground" />
              Live Monitoring
            </Link>
            <Link href="/cases" className="flex items-center gap-3 px-4 py-3 rounded-md hover:bg-primary/20 text-sm font-medium transition-colors">
              <Activity className="w-5 h-5 text-muted-foreground" />
              Case Management
            </Link>
            <Link href="/business" className="flex items-center gap-3 px-4 py-3 rounded-md hover:bg-primary/20 text-sm font-medium transition-colors">
              <Activity className="w-5 h-5 text-muted-foreground" />
              Business Impact
            </Link>
            <Link href="/rules" className="flex items-center gap-3 px-4 py-3 rounded-md hover:bg-primary/20 text-sm font-medium transition-colors">
              <Settings className="w-5 h-5 text-muted-foreground" />
              Rule Engine
            </Link>
          </nav>
          <div className="p-4 border-t border-border/50 text-xs text-muted-foreground">
            admin@sentinel.ai (Analyst Role)
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-8 relative">
          {children}
        </main>
      </body>
    </html>
  );
}
