"use client";

import { useEffect, useState } from "react";
import BrierScoreChart from "@/components/performance/BrierScoreChart";
import CalibrationCurve from "@/components/performance/CalibrationCurve";

interface BrierData {
  overall: { count: number; mean_brier: number | null; skill_score: number | null };
  by_domain: { domain: string; count: number; mean_brier: number; skill_score: number | null }[];
}

interface CalibrationData {
  bins: { bin_center: number; mean_forecast: number; actual_frequency: number; count: number }[];
}

export default function PerformancePage() {
  const [brierData, setBrierData] = useState<BrierData | null>(null);
  const [calibrationData, setCalibrationData] = useState<CalibrationData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:8000/api/metrics/brier").then((r) => r.json()),
      fetch("http://localhost:8000/api/metrics/calibration").then((r) => r.json()),
    ]).then(([brier, cal]) => {
      setBrierData(brier);
      setCalibrationData(cal);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-gray-400">Loading metrics...</div>;

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">Calibration Performance</h1>

      {brierData && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <p className="text-gray-400 text-sm">Predictions Scored</p>
            <p className="text-3xl font-bold mt-1">{brierData.overall.count}</p>
          </div>
          <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <p className="text-gray-400 text-sm">Mean Brier Score</p>
            <p className="text-3xl font-bold mt-1">
              {brierData.overall.mean_brier != null ? brierData.overall.mean_brier.toFixed(3) : "—"}
            </p>
            <p className="text-xs text-gray-500 mt-1">Lower = better (0 = perfect)</p>
          </div>
          <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <p className="text-gray-400 text-sm">Skill Score</p>
            <p className="text-3xl font-bold mt-1">
              {brierData.overall.skill_score != null ? brierData.overall.skill_score.toFixed(3) : "—"}
            </p>
            <p className="text-xs text-gray-500 mt-1">vs. 50% baseline (&gt;0 = better)</p>
          </div>
        </div>
      )}

      {brierData && brierData.by_domain.length > 0 && (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
          <h2 className="text-lg font-semibold mb-4">Brier Score by Domain</h2>
          <BrierScoreChart data={brierData.by_domain} />
        </div>
      )}

      {calibrationData && calibrationData.bins.length > 0 && (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
          <h2 className="text-lg font-semibold mb-4">Calibration Curve</h2>
          <p className="text-sm text-gray-400 mb-4">
            A well-calibrated forecaster&apos;s line lies close to the diagonal. Points above = underconfident; below = overconfident.
          </p>
          <CalibrationCurve data={calibrationData.bins} />
        </div>
      )}

      {(!brierData || brierData.overall.count === 0) && (
        <div className="text-center py-16 text-gray-500">
          <p>No scored predictions yet.</p>
          <a href="/predictions" className="mt-4 inline-block text-blue-400 hover:text-blue-300">
            Create and resolve predictions to see calibration data
          </a>
        </div>
      )}
    </div>
  );
}
