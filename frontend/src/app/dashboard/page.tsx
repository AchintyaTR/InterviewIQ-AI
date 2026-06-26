"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import styles from "./dashboard.module.css";

interface Interview {
  interview_id: str;
  target_role: string;
  target_company: string;
  status: "completed" | "in_progress";
  started_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchInterviews = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/auth/login");
        return;
      }

      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
        const res = await fetch(`${API_URL}/interviews/`, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });

        if (res.status === 401) {
          localStorage.removeItem("token");
          router.push("/auth/login");
          return;
        }

        const data = await res.json();
        setInterviews(data);
      } catch (err) {
        console.error("Failed to fetch interviews:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchInterviews();
  }, [router]);

  if (isLoading) {
    return <div className={styles.loadingWrapper}><div className="animate-pulse-glow" style={{width: 40, height: 40, borderRadius: '50%', background: 'var(--accent-primary)'}} /></div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Your Dashboard</h1>
        <Link href="/setup">
          <Button size="lg" className="animate-pulse-glow">
            Start New Interview
          </Button>
        </Link>
      </div>

      {interviews.length === 0 ? (
        <Card className={styles.emptyState}>
          <h3>No Interviews Yet</h3>
          <p>Ready to test your skills? Start a new mock interview session now.</p>
          <Link href="/setup">
            <Button>Start Interview</Button>
          </Link>
        </Card>
      ) : (
        <div className={styles.grid}>
          {interviews.map((interview, index) => (
            <Card 
              key={interview.interview_id} 
              className="animate-fade-in" 
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className={styles.cardHeader}>
                <div>
                  <h3 className={styles.role}>{interview.target_role}</h3>
                  <div className={styles.company}>{interview.target_company}</div>
                </div>
                <span className={`${styles.statusBadge} ${styles[`status_${interview.status}`]}`}>
                  {interview.status.replace("_", " ")}
                </span>
              </div>
              
              <div className={styles.date}>
                Started: {new Date(interview.started_at).toLocaleDateString()}
              </div>

              <div className={styles.actions}>
                {interview.status === "completed" ? (
                  <Link href={`/report/${interview.interview_id}`} style={{ width: '100%' }}>
                    <Button variant="secondary" style={{ width: '100%' }}>
                      View Report
                    </Button>
                  </Link>
                ) : (
                  <Link href={`/interview/${interview.interview_id}`} style={{ width: '100%' }}>
                    <Button style={{ width: '100%' }}>
                      Continue Interview
                    </Button>
                  </Link>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
