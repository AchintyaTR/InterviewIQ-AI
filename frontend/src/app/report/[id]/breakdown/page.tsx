"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import styles from "../../report.module.css";

interface QuestionEvaluation {
  question: string;
  candidate_answer: string;
  score: number;
  feedback: string;
  expected_answer: string;
  keywords: string[];
}

interface ReportData {
  question_evaluations: QuestionEvaluation[];
}

export default function BreakdownPage() {
  const { id } = useParams();
  const router = useRouter();
  const [report, setReport] = useState<ReportData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchReport = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/auth/login");
        return;
      }

      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      try {
        const res = await fetch(`${API_URL}/interviews/${id}/report`, {
          headers: { "Authorization": `Bearer ${token}` }
        });

        if (!res.ok) {
          throw new Error("Failed to fetch report from server");
        }

        const data = await res.json();
        
        setReport({
          question_evaluations: data.question_evaluations || []
        });
      } catch (err: any) {
        console.error("Failed to fetch report", err);
        setError(err.message || "Failed to load evaluation report.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchReport();
  }, [id, router]);

  const getScoreColor = (score: number) => {
    if (score >= 90) return styles.excellent;
    if (score >= 75) return styles.good;
    if (score >= 60) return styles.average;
    return styles.needs_work;
  };

  if (isLoading) {
    return <div className={styles.loadingWrapper}><div className="animate-pulse-glow" style={{width: 40, height: 40, borderRadius: '50%', background: 'var(--accent-primary)'}} /></div>;
  }

  if (error || !report) {
    return (
      <div className={styles.container}>
        <Card className={styles.errorState}>
          <h2>{error || "Report not available"}</h2>
          <br />
          <Link href={`/report/${id}`}><Button>Back to Summary</Button></Link>
        </Card>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={`${styles.header} animate-fade-in`}>
        <h1 className={styles.title}>Question-by-Question Breakdown</h1>
        <p className={styles.subtitle}>Detailed insights for each of your responses</p>
      </div>

      {report.question_evaluations.length > 0 ? (
        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          {report.question_evaluations.map((qEval, idx) => (
            <Card key={idx} className={`${styles.feedbackCard} animate-fade-in`} style={{ display: "flex", flexDirection: "column", gap: "12px", animationDelay: `${0.1 * idx}s` }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "12px" }}>
                <h3 style={{ fontSize: "1.1rem", margin: 0, color: "var(--text-primary)" }}>
                  Q{idx + 1}: {qEval.question}
                </h3>
                <div className={`${styles.scoreValue} ${getScoreColor(qEval.score)}`} style={{ fontSize: "1.2rem" }}>
                  {qEval.score}%
                </div>
              </div>
              
              <div>
                <strong style={{ color: "var(--accent-primary)" }}>Your Answer:</strong>
                <p style={{ margin: "4px 0 0", color: "var(--text-secondary)", fontSize: "0.95rem" }}>
                  {qEval.candidate_answer || "(No answer provided)"}
                </p>
              </div>
              
              <div style={{ padding: "12px", background: "var(--bg-secondary)", borderRadius: "8px", borderLeft: "4px solid var(--accent-primary)" }}>
                <strong style={{ color: "var(--text-primary)" }}>Feedback:</strong>
                <p style={{ margin: "4px 0 0", color: "var(--text-secondary)", fontSize: "0.95rem" }}>
                  {qEval.feedback}
                </p>
              </div>

              <div>
                <strong style={{ color: "var(--text-primary)" }}>Expected Answer:</strong>
                <p style={{ margin: "4px 0 8px", color: "var(--text-secondary)", fontSize: "0.95rem" }}>
                  {qEval.expected_answer}
                </p>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                  {qEval.keywords?.map((kw, i) => (
                    <span key={i} style={{ padding: "4px 8px", background: "rgba(56, 189, 248, 0.1)", color: "var(--accent-primary)", borderRadius: "12px", fontSize: "0.8rem", fontWeight: 500 }}>
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card className={styles.feedbackCard}>
          <p>No question breakdown available.</p>
        </Card>
      )}

      <div className={styles.controls} style={{ marginTop: '30px' }}>
        <Link href={`/report/${id}`}>
          <Button size="lg" variant="secondary">Back to Summary</Button>
        </Link>
      </div>
    </div>
  );
}
