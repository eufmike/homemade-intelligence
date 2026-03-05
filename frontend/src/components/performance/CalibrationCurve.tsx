"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
  Legend,
} from "recharts";

interface BinData {
  bin_center: number;
  mean_forecast: number;
  actual_frequency: number;
  count: number;
}

interface Props {
  data: BinData[];
}

export default function CalibrationCurve({ data }: Props) {
  // Add perfect calibration line reference points
  const plotData = data.map((d) => ({
    ...d,
    perfect: d.bin_center,
    label: `${(d.bin_center * 100).toFixed(0)}%`,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={plotData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis
          dataKey="bin_center"
          stroke="#9CA3AF"
          tick={{ fontSize: 12 }}
          tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
          domain={[0, 1]}
        />
        <YAxis
          stroke="#9CA3AF"
          tick={{ fontSize: 12 }}
          tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
          domain={[0, 1]}
        />
        <Tooltip
          contentStyle={{ backgroundColor: "#111827", border: "1px solid #374151", borderRadius: 8 }}
          formatter={(val: number, name: string) => [`${(val * 100).toFixed(1)}%`, name]}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="perfect"
          stroke="#6B7280"
          strokeDasharray="4 4"
          name="Perfect Calibration"
          dot={false}
        />
        <Line
          type="monotone"
          dataKey="actual_frequency"
          stroke="#3B82F6"
          strokeWidth={2}
          name="Actual Frequency"
          dot={{ fill: "#3B82F6", r: 4 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
