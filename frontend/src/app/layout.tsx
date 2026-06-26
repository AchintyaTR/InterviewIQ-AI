import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "InterviewIQ AI",
  description: "Your AI-powered technical interview prep platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="navbar">
          <div className="navbar-content">
            <a href="/" className="logo text-gradient">InterviewIQ</a>
            <div className="nav-links">
              <a href="/dashboard" className="nav-link">Dashboard</a>
              <a href="/auth/login" className="nav-link login-btn">Login</a>
            </div>
          </div>
        </nav>
        <main className="main-content">
          {children}
        </main>
      </body>
    </html>
  );
}
