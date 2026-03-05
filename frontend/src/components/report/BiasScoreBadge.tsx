interface BiasScoreBadgeProps {
  score: number | null;
}

export default function BiasScoreBadge({ score }: BiasScoreBadgeProps) {
  if (score == null) return null;

  const color =
    score >= 0.7 ? "bg-red-900 text-red-300 border-red-800" :
    score >= 0.4 ? "bg-yellow-900 text-yellow-300 border-yellow-800" :
    "bg-gray-800 text-gray-300 border-gray-700";

  const label =
    score >= 0.7 ? "High Divergence" :
    score >= 0.4 ? "Moderate Divergence" :
    "Low Divergence";

  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs border ${color}`}>
      Bias: {score.toFixed(2)} — {label}
    </span>
  );
}
