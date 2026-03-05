"use client";

import { useState } from "react";

interface Props {
  predictionId: number;
  onClose: () => void;
  onResolved: () => void;
}

export default function ResolutionModal({ predictionId, onClose, onResolved }: Props) {
  const [outcome, setOutcome] = useState<"correct" | "incorrect" | "partial">("correct");
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await fetch(`http://localhost:8000/api/predictions/${predictionId}/resolve`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ outcome, resolution_notes: notes }),
      });
      if (!res.ok) throw new Error(await res.text());
      onResolved();
    } catch (err) {
      setError(String(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-xl border border-gray-700 p-6 w-full max-w-md space-y-4">
        <h2 className="text-lg font-semibold">Resolve Prediction</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-300 mb-2">Outcome</label>
            <div className="flex gap-2">
              {(["correct", "incorrect", "partial"] as const).map((o) => (
                <button
                  key={o}
                  type="button"
                  onClick={() => setOutcome(o)}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                    outcome === o
                      ? o === "correct" ? "bg-green-700 text-white"
                        : o === "incorrect" ? "bg-red-700 text-white"
                        : "bg-yellow-700 text-white"
                      : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                  }`}
                >
                  {o}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-1">Resolution Notes</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              placeholder="Context for this resolution..."
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
            />
          </div>

          {error && <p className="text-red-400 text-sm">{error}</p>}

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-lg text-sm font-medium transition-colors"
            >
              {submitting ? "Saving..." : "Confirm"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
