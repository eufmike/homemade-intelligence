import Link from "next/link";

interface StatCard {
  label: string;
  value: string;
  href: string;
}

async function getDashboardStats() {
  try {
    const [reportsRes, predictionsRes] = await Promise.all([
      fetch("http://localhost:8000/api/reports?limit=1", { cache: "no-store" }),
      fetch("http://localhost:8000/api/predictions?limit=1", { cache: "no-store" }),
    ]);
    const reports = reportsRes.ok ? await reportsRes.json() : [];
    const predictions = predictionsRes.ok ? await predictionsRes.json() : [];
    return { reports, predictions };
  } catch {
    return { reports: [], predictions: [] };
  }
}

export default async function Dashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white">Intelligence Dashboard</h1>
        <p className="text-gray-400 mt-1">
          Bias-aware geopolitical analysis | {new Date().toLocaleDateString("en-US", { dateStyle: "full" })}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link href="/reports/new"
          className="block p-6 rounded-xl bg-blue-600 hover:bg-blue-500 transition-colors">
          <div className="text-2xl mb-2">+ Generate Report</div>
          <p className="text-blue-100 text-sm">Analyze a topic across diverse sources</p>
        </Link>

        <Link href="/reports"
          className="block p-6 rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors">
          <div className="text-2xl mb-2">Reports</div>
          <p className="text-gray-400 text-sm">View past intelligence assessments</p>
        </Link>

        <Link href="/predictions"
          className="block p-6 rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors">
          <div className="text-2xl mb-2">Predictions</div>
          <p className="text-gray-400 text-sm">Track and score your forecasts</p>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link href="/performance"
          className="block p-6 rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors">
          <div className="text-lg font-semibold mb-1">Calibration Performance</div>
          <p className="text-gray-400 text-sm">Brier scores and accuracy timelines</p>
        </Link>

        <Link href="/sources"
          className="block p-6 rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors">
          <div className="text-lg font-semibold mb-1">Source Status</div>
          <p className="text-gray-400 text-sm">Feed health and manual injection</p>
        </Link>
      </div>

      <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
        <h2 className="text-lg font-semibold mb-3">Analytical Principles</h2>
        <ul className="space-y-2 text-sm text-gray-400">
          <li>Triangulation over trust — never treat a single source as authoritative</li>
          <li>Bias as a variable — every source has a perspective, tracked explicitly</li>
          <li>Leading over lagging — VIX, CDS, tanker flows before GDP and official statements</li>
          <li>Non-Western perspectives required — every analysis includes non-Anglophone sources</li>
          <li>Manipulation awareness — CIB checklist applied to all time-sensitive analysis</li>
        </ul>
      </div>
    </div>
  );
}
