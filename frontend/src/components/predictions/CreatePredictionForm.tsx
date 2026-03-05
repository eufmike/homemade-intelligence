"use client";

import { useState } from "react";

interface Props {
  onCreated: () => void;
}

const DOMAINS = ["geopolitics", "markets", "taiwan", "energy", "other"];

export default function CreatePredictionForm({ onCreated }: Props) {
  const [form, setForm] = useState({
    topic: "",
    prediction_text: "",
    confidence_pct: 60,
    domain: "geopolitics",
    deadline_date: "",
    metaculus_community_pct: "",
    polymarket_odds_pct: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const body = {
        ...form,
        confidence_pct: Number(form.confidence_pct),
        deadline_date: form.deadline_date || null,
        metaculus_community_pct: form.metaculus_community_pct ? Number(form.metaculus_community_pct) : null,
        polymarket_odds_pct: form.polymarket_odds_pct ? Number(form.polymarket_odds_pct) : null,
      };
      const res = await fetch("http://localhost:8000/api/predictions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(await res.text());
      onCreated();
    } catch (err) {
      setError(String(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
      <h2 className="text-lg font-semibold">New Prediction</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm text-gray-300 mb-1">Topic</label>
          <input
            value={form.topic}
            onChange={(e) => setForm({ ...form, topic: e.target.value })}
            required
            placeholder="Short label"
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-300 mb-1">Domain</label>
          <select
            value={form.domain}
            onChange={(e) => setForm({ ...form, domain: e.target.value })}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            {DOMAINS.map((d) => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm text-gray-300 mb-1">Prediction Statement</label>
        <textarea
          value={form.prediction_text}
          onChange={(e) => setForm({ ...form, prediction_text: e.target.value })}
          required
          rows={3}
          placeholder="Full prediction statement..."
          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm text-gray-300 mb-1">Confidence: {form.confidence_pct}%</label>
          <input
            type="range"
            min={1}
            max={99}
            value={form.confidence_pct}
            onChange={(e) => setForm({ ...form, confidence_pct: Number(e.target.value) })}
            className="w-full"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-300 mb-1">Deadline</label>
          <input
            type="date"
            value={form.deadline_date}
            onChange={(e) => setForm({ ...form, deadline_date: e.target.value })}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-300 mb-1">Metaculus Odds %</label>
          <input
            type="number"
            min={0}
            max={100}
            value={form.metaculus_community_pct}
            onChange={(e) => setForm({ ...form, metaculus_community_pct: e.target.value })}
            placeholder="e.g. 35"
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
        </div>
      </div>

      {error && <p className="text-red-400 text-sm">{error}</p>}

      <button
        type="submit"
        disabled={submitting}
        className="px-6 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-lg font-medium transition-colors"
      >
        {submitting ? "Saving..." : "Create Prediction"}
      </button>
    </form>
  );
}
