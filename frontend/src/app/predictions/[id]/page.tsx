"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ResolutionModal from "@/components/predictions/ResolutionModal";
import ReferenceOddsBar from "@/components/predictions/ReferenceOddsBar";

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

export default function PredictionDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [showResolve, setShowResolve] = useState(false);

  const fetchPrediction = () => {
    fetch(`http://localhost:8000/api/predictions/${id}`)
      .then((r) => r.json())
      .then(setPrediction)
      .catch(console.error);
  };

  useEffect(() => { fetchPrediction(); }, [id]);

  if (!prediction) return <div className="text-gray-400">Loading...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 text-sm text-gray-400">
        <a href="/predictions" className="hover:text-white">Predictions</a>
        <span>/</span>
        <span className="text-white">{prediction.topic}</span>
      </div>

      <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
        <h1 className="text-2xl font-bold">{prediction.topic}</h1>
        <p className="text-gray-300">{prediction.prediction_text}</p>

        <div className="flex flex-wrap gap-4 text-sm">
          <div>
            <span className="text-gray-400">Confidence: </span>
            <span className="text-white font-bold text-lg">{prediction.confidence_pct}%</span>
          </div>
          <div>
            <span className="text-gray-400">Domain: </span>
            <span>{prediction.domain}</span>
          </div>
          {prediction.deadline_date && (
            <div>
              <span className="text-gray-400">Deadline: </span>
              <span>{prediction.deadline_date}</span>
            </div>
          )}
        </div>

        <ReferenceOddsBar
          myConfidence={prediction.confidence_pct ?? 50}
          metaculusPct={prediction.metaculus_community_pct}
          polymarketPct={prediction.polymarket_odds_pct}
        />

        {prediction.outcome ? (
          <div className="p-3 rounded-lg bg-gray-800">
            <span className="text-gray-400 text-sm">Outcome: </span>
            <span className={`font-medium ${prediction.outcome === "correct" ? "text-green-400" : prediction.outcome === "incorrect" ? "text-red-400" : "text-yellow-400"}`}>
              {prediction.outcome}
            </span>
            {prediction.resolved_at && (
              <span className="text-gray-400 text-sm ml-2">
                resolved {new Date(prediction.resolved_at).toLocaleDateString()}
              </span>
            )}
          </div>
        ) : (
          <button
            onClick={() => setShowResolve(true)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium transition-colors"
          >
            Resolve Prediction
          </button>
        )}
      </div>

      {showResolve && (
        <ResolutionModal
          predictionId={prediction.id}
          onClose={() => setShowResolve(false)}
          onResolved={() => { setShowResolve(false); fetchPrediction(); }}
        />
      )}
    </div>
  );
}
