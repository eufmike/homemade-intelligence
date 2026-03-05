import ReportViewer from "@/components/report/ReportViewer";

interface ReportDetail {
  id: number;
  topic: string;
  domain: string | null;
  status: string;
  bias_score: number | null;
  confidence_overall: string | null;
  tokens_used: number | null;
  tokens_cached: number | null;
  cost_usd: number | null;
  created_at: string | null;
  completed_at: string | null;
  content_en: string | null;
  content_zh_tw: string | null;
  content_zh_tw_elder: string | null;
}

async function getReport(id: string): Promise<ReportDetail | null> {
  try {
    const res = await fetch(`http://localhost:8000/api/reports/${id}`, { cache: "no-store" });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export default async function ReportPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const report = await getReport(id);

  if (!report) {
    return (
      <div className="text-center py-16 text-gray-500">
        <p>Report not found.</p>
        <a href="/reports" className="mt-4 inline-block text-blue-400 hover:text-blue-300">
          Back to Reports
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 text-sm text-gray-400">
        <a href="/reports" className="hover:text-white">Reports</a>
        <span>/</span>
        <span className="text-white">{report.topic}</span>
      </div>

      <div className="bg-gray-900 rounded-xl p-4 border border-gray-800 flex flex-wrap gap-4 text-sm">
        <span><span className="text-gray-400">Domain:</span> {report.domain || "general"}</span>
        <span><span className="text-gray-400">Status:</span> {report.status}</span>
        {report.bias_score != null && (
          <span><span className="text-gray-400">Bias Divergence:</span> {report.bias_score.toFixed(2)}</span>
        )}
        {report.tokens_used != null && (
          <span><span className="text-gray-400">Tokens:</span> {report.tokens_used.toLocaleString()} ({report.tokens_cached?.toLocaleString() ?? 0} cached)</span>
        )}
        {report.cost_usd != null && (
          <span><span className="text-gray-400">Cost:</span> ${report.cost_usd.toFixed(4)}</span>
        )}
        {report.created_at && (
          <span><span className="text-gray-400">Date:</span> {new Date(report.created_at).toLocaleString()}</span>
        )}
      </div>

      <ReportViewer
        contentEn={report.content_en}
        contentZhTw={report.content_zh_tw}
        contentZhTwElder={report.content_zh_tw_elder}
        topic={report.topic}
      />
    </div>
  );
}
