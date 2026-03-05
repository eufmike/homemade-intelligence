"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import CreatePredictionForm from "@/components/predictions/CreatePredictionForm";

interface Prediction {
  id: number;
  topic: string;
  prediction_text: string;
  confidence_pct: number | null;
  domain: string | null;
  deadline_date: string | null;
  created_at: string | null;
  resolved_at: string | null;
  outcome: string | null;
  metaculus_community_pct: number | null;
  polymarket_odds_pct: number | null;
}

const OUTCOME_STYLES: Record<string, string> = {
  correct: "text-green-400",
  incorrect: "text-red-400",
  partial: "text-yellow-400",
};

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  const fetchPredictions = () => {
    fetch("http://localhost:8000/api/predictions?limit=100")
      .then((r) => r.json())
      .then(setPredictions)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchPredictions(); }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Predictions</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium transition-colors"
        >
          {showForm ? "Cancel" : "+ New Prediction"}
        </button>
      </div>

      {showForm && (
        <CreatePredictionForm
          onCreated={() => { setShowForm(false); fetchPredictions(); }}
        />
      )}

      {loading ? (
        <div className="text-gray-400">Loading...</div>
      ) : predictions.length === 0 ? (
        <div className="text-center py-16 text-gray-500">No predictions yet.</div>
      ) : (
        <div className="space-y-3">
          {predictions.map((p) => (
            <Link key={p.id} href={`/predictions/${p.id}`}
              className="block p-4 bg-gray-900 rounded-xl border border-gray-800 hover:border-gray-600 transition-colors">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <p className="font-medium">{p.topic}</p>
                  <p className="text-sm text-gray-400 mt-0.5 truncate">{p.prediction_text}</p>
                  <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                    <span className="text-white font-medium">{p.confidence_pct}%</span>
                    {p.metaculus_community_pct != null && <span>Metaculus: {p.metaculus_community_pct}%</span>}
                    {p.polymarket_odds_pct != null && <span>Polymarket: {p.polymarket_odds_pct}%</span>}
                    <span>{p.domain}</span>
                    {p.deadline_date && <span>due {p.deadline_date}</span>}
                  </div>
                </div>
                <div className="text-right">
                  {p.outcome ? (
                    <span className={`text-sm font-medium ${OUTCOME_STYLES[p.outcome] ?? "text-gray-400"}`}>
                      {p.outcome}
                    </span>
                  ) : (
                    <span className="text-xs text-gray-500">pending</span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
