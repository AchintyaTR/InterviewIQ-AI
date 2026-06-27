"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import styles from "../report.module.css";

interface QuestionEvaluation {
  question: string;
  candidate_answer: string;
  score: number;
  feedback: string;
  expected_answer: string;
  keywords: string[];
}

interface ReportData {
  overall_score: number;
  accuracy_score: number;
  communication_score: number;
  problem_solving_score: number;
  confidence_score: number;
  detailed_feedback: string;
  actionable_items: string[];
  question_evaluations: QuestionEvaluation[];
}

export default function ReportPage() {
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

        if (res.status === 401) {
          router.push("/auth/login");
          return;
        }

        if (res.status === 404) {
          setError("Report not found or not generated yet.");
          return;
        }
        
        if (!res.ok) {
          const errData = await res.json().catch(() => ({}));
          throw new Error(errData.detail || "Failed to fetch report from server");
        }

        const data = await res.json();
        
        // Map backend schema to frontend expectations
        const mappedData: ReportData = {
          overall_score: Math.round(data.score_overall || 0),
          accuracy_score: Math.round(data.score_metrics?.technical_accuracy || 0),
          communication_score: Math.round(data.score_metrics?.communication_skills || 0),
          problem_solving_score: Math.round(data.score_metrics?.problem_solving || 0),
          confidence_score: Math.round(data.score_metrics?.confidence || 0),
          detailed_feedback: data.feedback || "No feedback available.",
          actionable_items: data.learning_roadmap 
            ? data.learning_roadmap.map((item: any) => `${item.topic}: ${item.suggestion}`)
            : [],
          question_evaluations: data.question_evaluations || []
        };
        
        setReport(mappedData);
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
          <Link href="/dashboard"><Button>Back to Dashboard</Button></Link>
        </Card>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={`${styles.header} animate-fade-in`}>
        <h1 className={styles.title}>Interview Performance Report</h1>
        <p className={styles.subtitle}>Here is your detailed AI evaluation</p>
      </div>

      <div className={styles.scoreGrid}>
        <Card className={`animate-fade-in ${styles.scoreCard}`} style={{ animationDelay: '0.1s' }}>
          <div className={styles.scoreLabel}>Overall Score</div>
          <div className={`${styles.scoreValue} ${getScoreColor(report.overall_score)}`}>
            {report.overall_score}%
          </div>
        </Card>
        
        <Card className={`animate-fade-in ${styles.scoreCard}`} style={{ animationDelay: '0.2s' }}>
          <div className={styles.scoreLabel}>Technical Accuracy</div>
          <div className={`${styles.scoreValue} ${getScoreColor(report.accuracy_score)}`}>
            {report.accuracy_score}%
          </div>
        </Card>

        <Card className={`animate-fade-in ${styles.scoreCard}`} style={{ animationDelay: '0.3s' }}>
          <div className={styles.scoreLabel}>Communication</div>
          <div className={`${styles.scoreValue} ${getScoreColor(report.communication_score)}`}>
            {report.communication_score}%
          </div>
        </Card>
      </div>

      <div className={`${styles.section} animate-fade-in`} style={{ animationDelay: '0.4s' }}>
        <h2 className={styles.sectionTitle}>💬 Detailed Feedback</h2>
        <Card className={styles.feedbackCard}>
          <p>{report.detailed_feedback}</p>
        </Card>
      </div>

      <div className={`${styles.section} animate-fade-in`} style={{ animationDelay: '0.5s' }}>
        <h2 className={styles.sectionTitle}>🎯 Actionable Improvements</h2>
        <Card className={styles.feedbackCard}>
          <ul className={styles.actionList}>
            {report.actionable_items.map((item, idx) => (
              <li key={idx} className={styles.actionItem}>
                <span className={styles.actionIcon}>→</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap', marginTop: '40px', paddingBottom: '40px' }}>
        <Link href={`/report/${id}/breakdown`}>
          <Button size="lg" className="animate-pulse-glow">
            View Detailed Question-by-Question Feedback
          </Button>
        </Link>
        <Link href="/dashboard">
          <Button size="lg" variant="secondary">Return to Dashboard</Button>
        </Link>
      </div>
    </div>
  );
}
