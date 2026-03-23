import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Stock Investment Research AI",
  description: "Advanced GenAI Research Assistant",
};

import Sidebar from "@/components/Sidebar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-zinc-950 text-zinc-50 antialiased`}>
        <div className="flex h-screen w-full bg-[#0a0a0a] text-zinc-100 font-sans overflow-hidden">
          <Sidebar />
          <main className="flex-1 flex flex-col h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-zinc-900/20 via-[#0a0a0a] to-[#0a0a0a]">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
