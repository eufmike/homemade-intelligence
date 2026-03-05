"use client";

import { useState } from "react";

interface Props {
  onInjected: () => void;
}

export default function ManualInjectPanel({ onInjected }: Props) {
  const [mode, setMode] = useState<"text" | "url">("text");
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [url, setUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setResult(null);
    try {
      let res;
      if (mode === "text") {
        res = await fetch("http://localhost:8000/api/inject/text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title, body }),
        });
      } else {
        res = await fetch("http://localhost:8000/api/inject/url", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url }),
        });
      }
      const data = await res.json();
      setResult(data);
      if (data.success) {
        setTitle(""); setBody(""); setUrl("");
        onInjected();
      }
    } catch (err) {
      setResult({ success: false, message: String(err) });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
      <h2 className="text-lg font-semibold">Manual Article Injection</h2>

      <div className="flex gap-2">
        {(["text", "url"] as const).map((m) => (
          <button
            key={m}
            onClick={() => setMode(m)}
            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              mode === m ? "bg-blue-600 text-white" : "bg-gray-800 text-gray-400 hover:text-white"
            }`}
          >
            {m === "text" ? "Paste Text" : "Inject URL"}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        {mode === "text" ? (
          <>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              placeholder="Article title"
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              required
              rows={5}
              placeholder="Paste article text..."
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
            />
          </>
        ) : (
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            type="url"
            placeholder="https://..."
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
        )}

        <button
          type="submit"
          disabled={submitting}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-lg text-sm font-medium transition-colors"
        >
          {submitting ? "Injecting..." : "Inject"}
        </button>
      </form>

      {result && (
        <p className={`text-sm ${result.success ? "text-green-400" : "text-red-400"}`}>
          {result.message}
        </p>
      )}
    </div>
  );
}
