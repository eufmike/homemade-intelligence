"use client";

type Audience = "en" | "zh_tw" | "zh_tw_elder";

interface AudienceToggleProps {
  value: Audience;
  onChange: (audience: Audience) => void;
}

const TABS: { key: Audience; label: string }[] = [
  { key: "en", label: "EN" },
  { key: "zh_tw", label: "繁中" },
  { key: "zh_tw_elder", label: "長輩版" },
];

export default function AudienceToggle({ value, onChange }: AudienceToggleProps) {
  return (
    <div className="flex gap-1 p-1 bg-gray-900 rounded-lg border border-gray-800 w-fit">
      {TABS.map((tab) => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
            value === tab.key
              ? "bg-blue-600 text-white"
              : "text-gray-400 hover:text-white"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
