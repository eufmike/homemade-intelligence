interface Props {
  myConfidence: number;
  metaculusPct: number | null;
  polymarketPct: number | null;
}

function Bar({ label, pct, color }: { label: string; pct: number; color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-gray-400">
        <span>{label}</span>
        <span className="text-white font-medium">{pct}%</span>
      </div>
      <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export default function ReferenceOddsBar({ myConfidence, metaculusPct, polymarketPct }: Props) {
  const hasRef = metaculusPct != null || polymarketPct != null;

  return (
    <div className="space-y-3">
      <Bar label="My Confidence" pct={myConfidence} color="bg-blue-500" />
      {metaculusPct != null && <Bar label="Metaculus Community" pct={metaculusPct} color="bg-purple-500" />}
      {polymarketPct != null && <Bar label="Polymarket" pct={polymarketPct} color="bg-green-500" />}
      {!hasRef && <p className="text-xs text-gray-500">No reference odds recorded.</p>}
    </div>
  );
}
