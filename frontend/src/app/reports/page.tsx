"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Report {
  id: number;
  topic: string;
  domain: string | null;
  status: string;
  bias_score: number | null;
  confidence_overall: string | null;
  tokens_used: number | null;
  cost_usd: number | null;
  created_at: string | null;
}

const DOMAIN_COLORS: Record<string, string> = {
  geopolitics: "bg-red-900 text-red-300",
  markets: "bg-green-900 text-green-300",
  taiwan: "bg-blue-900 text-blue-300",
  energy: "bg-yellow-900 text-yellow-300",
  general: "bg-gray-800 text-gray-300",
};

const STATUS_COLORS: Record<string, string> = {
  complete: "text-green-400",
  generating: "text-yellow-400",
  failed: "text-red-400",
  pending: "text-gray-400",
};

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/reports?limit=50")
      .then((r) => r.json())
      .then(setReports)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Intelligence Reports</h1>
        <Link href="/reports/new"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium transition-colors">
          + New Report
        </Link>
      </div>

      {loading ? (
        <div className="text-gray-400">Loading reports...</div>
      ) : reports.length === 0 ? (
        <div className="text-center py-16 text-gray-500">
          <p className="text-lg">No reports yet.</p>
          <Link href="/reports/new" className="mt-4 inline-block text-blue-400 hover:text-blue-300">
            Generate your first report
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {reports.map((r) => (
            <Link key={r.id} href={`/reports/${r.id}`}
              className="block p-4 bg-gray-900 rounded-xl border border-gray-800 hover:border-gray-600 transition-colors">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{r.topic}</p>
                  <div className="flex items-center gap-2 mt-1 text-xs text-gray-400">
                    <span className={`px-2 py-0.5 rounded-full text-xs ${DOMAIN_COLORS[r.domain || "general"] ?? DOMAIN_COLORS.general}`}>
                      {r.domain || "general"}
                    </span>
                    <span className={STATUS_COLORS[r.status] ?? "text-gray-400"}>{r.status}</span>
                    {r.bias_score != null && (
                      <span>divergence: {r.bias_score.toFixed(2)}</span>
                    )}
                    {r.cost_usd != null && (
                      <span>${r.cost_usd.toFixed(4)}</span>
                    )}
                  </div>
                </div>
                <span className="text-xs text-gray-500 whitespace-nowrap">
                  {r.created_at ? new Date(r.created_at).toLocaleDateString() : ""}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
