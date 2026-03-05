"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import AudienceToggle from "./AudienceToggle";

type Audience = "en" | "zh_tw" | "zh_tw_elder";

interface ReportViewerProps {
  contentEn: string | null;
  contentZhTw: string | null;
  contentZhTwElder: string | null;
  topic: string;
}

export default function ReportViewer({ contentEn, contentZhTw, contentZhTwElder, topic }: ReportViewerProps) {
  const [audience, setAudience] = useState<Audience>("en");

  const content = audience === "en" ? contentEn : audience === "zh_tw" ? contentZhTw : contentZhTwElder;

  return (
    <div className="space-y-4">
      <AudienceToggle value={audience} onChange={setAudience} />

      {content ? (
        <div className={`prose prose-invert max-w-none bg-gray-900 rounded-xl p-6 border border-gray-800 ${audience !== "en" ? "font-[var(--font-noto-sans-tc)]" : ""}`}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </div>
      ) : (
        <div className="text-gray-500 text-center py-8">
          {audience === "en" ? "No English content available." : audience === "zh_tw" ? "尚無繁體中文版本。" : "尚無長輩版本。"}
        </div>
      )}
    </div>
  );
}
