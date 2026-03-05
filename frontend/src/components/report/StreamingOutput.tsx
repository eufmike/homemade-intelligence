"use client";

import { useEffect, useRef } from "react";

interface StreamEvent {
  type: string;
  data: Record<string, unknown>;
}

interface StreamingOutputProps {
  events: StreamEvent[];
  isStreaming: boolean;
}

export default function StreamingOutput({ events, isStreaming }: StreamingOutputProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  const tokens = events.filter((e) => e.type === "token").map((e) => String(e.data.text ?? "")).join("");
  const stages = events.filter((e) => e.type === "status");
  const warnings = events.filter((e) => e.type === "warning");
  const complete = events.find((e) => e.type === "complete");

  const currentStage = stages.length > 0 ? String(stages[stages.length - 1].data.stage) : "";

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [tokens]);

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3 text-sm text-gray-400">
        {isStreaming && (
          <span className="inline-flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-green-400 animate-pulse" />
            {currentStage === "analyze" ? "Streaming analysis..." : `Stage: ${currentStage}`}
          </span>
        )}
        {warnings.map((w, i) => (
          <span key={i} className="text-yellow-400">Warning: {String(w.data.message)}</span>
        ))}
        {complete && (
          <span className="text-green-400">
            Done — {Number(complete.data.tokens_used).toLocaleString()} tokens,
            {" "}{Number(complete.data.tokens_cached).toLocaleString()} cached,
            {" "}${Number(complete.data.cost_usd).toFixed(4)}
          </span>
        )}
      </div>

      {tokens && (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 font-mono text-sm text-gray-200 whitespace-pre-wrap max-h-[60vh] overflow-y-auto">
          {tokens}
          {isStreaming && <span className="animate-pulse">|</span>}
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  );
}
