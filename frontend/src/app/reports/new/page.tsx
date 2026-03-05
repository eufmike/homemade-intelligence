"use client";

import { useState, useRef } from "react";
import StreamingOutput from "@/components/report/StreamingOutput";
import ReportViewer from "@/components/report/ReportViewer";

const DOMAINS = ["general", "geopolitics", "markets", "taiwan", "energy"];

export default function NewReportPage() {
  const [topic, setTopic] = useState("");
  const [domain, setDomain] = useState("general");
  const [manualTitle, setManualTitle] = useState("");
  const [manualText, setManualText] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamEvents, setStreamEvents] = useState<{ type: string; data: Record<string, unknown> }[]>([]);
  const [completedReport, setCompletedReport] = useState<null | { id: number }>(null);
  const [error, setError] = useState("");
  const eventSourceRef = useRef<EventSource | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsStreaming(true);
    setStreamEvents([]);
    setCompletedReport(null);
    setError("");

    const body = JSON.stringify({ topic, domain, manual_text: manualText, manual_title: manualTitle });

    try {
      const response = await fetch("http://localhost:8000/api/reports/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() ?? "";

        for (const chunk of lines) {
          if (!chunk.trim()) continue;
          const eventLine = chunk.split("\n").find((l) => l.startsWith("event:"));
          const dataLine = chunk.split("\n").find((l) => l.startsWith("data:"));
          if (!eventLine || !dataLine) continue;
          const eventType = eventLine.replace("event:", "").trim();
          const data = JSON.parse(dataLine.replace("data:", "").trim());

          setStreamEvents((prev) => [...prev, { type: eventType, data }]);

          if (eventType === "complete") {
            setCompletedReport({ id: data.report_id });
          }
          if (eventType === "error") {
            setError(data.message || "Unknown error");
          }
        }
      }
    } catch (err) {
      setError(String(err));
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Generate Intelligence Report</h1>

      <form onSubmit={handleSubmit} className="space-y-4 bg-gray-900 rounded-xl p-6 border border-gray-800">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">Topic</label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. Iran Strait of Hormuz closure risk, Taiwan Strait military activity"
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">Domain</label>
          <select
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            className="px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            {DOMAINS.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Article to Inject (optional)
          </label>
          <input
            type="text"
            value={manualTitle}
            onChange={(e) => setManualTitle(e.target.value)}
            placeholder="Article title"
            className="w-full px-3 py-2 mb-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
          <textarea
            value={manualText}
            onChange={(e) => setManualText(e.target.value)}
            placeholder="Paste article text here to include in the analysis..."
            rows={6}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
          />
        </div>

        <button
          type="submit"
          disabled={isStreaming || !topic.trim()}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg font-medium transition-colors"
        >
          {isStreaming ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {(isStreaming || streamEvents.length > 0) && (
        <StreamingOutput events={streamEvents} isStreaming={isStreaming} />
      )}

      {error && (
        <div className="p-4 bg-red-950 border border-red-800 rounded-xl text-red-300">
          Error: {error}
        </div>
      )}

      {completedReport && (
        <div className="p-4 bg-green-950 border border-green-800 rounded-xl text-green-300">
          Report complete.{" "}
          <a href={`/reports/${completedReport.id}`} className="underline hover:text-green-200">
            View full report
          </a>
        </div>
      )}
    </div>
  );
}
