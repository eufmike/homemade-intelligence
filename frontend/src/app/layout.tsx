import type { Metadata } from "next";
import { Noto_Sans_TC } from "next/font/google";
import "./globals.css";

const notoSansTC = Noto_Sans_TC({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-noto-sans-tc",
});

export const metadata: Metadata = {
  title: "Homemade Intelligence",
  description: "Personal bias-aware geopolitical intelligence platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-TW">
      <body className={`${notoSansTC.variable} font-sans antialiased bg-gray-950 text-gray-100 min-h-screen`}>
        <nav className="border-b border-gray-800 bg-gray-900 px-6 py-3 flex items-center gap-6">
          <a href="/" className="text-lg font-bold text-white tracking-tight">
            Homemade Intelligence
          </a>
          <div className="flex gap-4 text-sm text-gray-400">
            <a href="/reports" className="hover:text-white transition-colors">Reports</a>
            <a href="/reports/new" className="hover:text-white transition-colors">+ New</a>
            <a href="/predictions" className="hover:text-white transition-colors">Predictions</a>
            <a href="/performance" className="hover:text-white transition-colors">Performance</a>
            <a href="/sources" className="hover:text-white transition-colors">Sources</a>
          </div>
        </nav>
        <main className="max-w-6xl mx-auto px-6 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
