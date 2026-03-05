"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

interface DomainData {
  domain: string;
  count: number;
  mean_brier: number;
  skill_score: number | null;
}

interface Props {
  data: DomainData[];
}

export default function BrierScoreChart({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="domain" stroke="#9CA3AF" tick={{ fontSize: 12 }} />
        <YAxis stroke="#9CA3AF" tick={{ fontSize: 12 }} domain={[0, 1]} />
        <Tooltip
          contentStyle={{ backgroundColor: "#111827", border: "1px solid #374151", borderRadius: 8 }}
          labelStyle={{ color: "#F9FAFB" }}
          formatter={(val: number, name: string) => [val.toFixed(4), name]}
        />
        <Bar dataKey="mean_brier" name="Mean Brier Score" radius={[4, 4, 0, 0]}>
          {data.map((entry, idx) => (
            <Cell
              key={idx}
              fill={entry.mean_brier < 0.1 ? "#10B981" : entry.mean_brier < 0.2 ? "#F59E0B" : "#EF4444"}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
