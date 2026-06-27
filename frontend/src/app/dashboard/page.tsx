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
  
  const [modalConfig, setModalConfig] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    type: 'alert' | 'confirm';
    onConfirm?: () => void;
  }>({ isOpen: false, title: '', message: '', type: 'alert' });

  const showAlert = (title: string, message: string) => {
    setModalConfig({ isOpen: true, title, message, type: 'alert' });
  };

  const showConfirm = (title: string, message: string, onConfirm: () => void) => {
    setModalConfig({ isOpen: true, title, message, type: 'confirm', onConfirm });
  };

  const closeModal = () => {
    setModalConfig(prev => ({ ...prev, isOpen: false }));
  };

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

  const handleDelete = (interview_id: string) => {
    showConfirm(
      "Delete Interview",
      "Are you sure you want to delete this interview?",
      async () => {
        const token = localStorage.getItem("token");
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
        
        try {
          const res = await fetch(`${API_URL}/interviews/${interview_id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
          });
          
          if (res.ok) {
            setInterviews(prev => prev.filter(i => i.interview_id !== interview_id));
          } else {
            showAlert("Error", "Failed to delete interview.");
          }
        } catch (err) {
          console.error(err);
          showAlert("Error", "An error occurred while deleting.");
        }
      }
    );
  };

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

              <div className={styles.actions} style={{ display: 'flex', gap: '8px' }}>
                {interview.status === "completed" ? (
                  <Link href={`/report/${interview.interview_id}`} style={{ flex: 1 }}>
                    <Button variant="secondary" style={{ width: '100%' }}>
                      View Report
                    </Button>
                  </Link>
                ) : (
                  <Link href={`/interview/${interview.interview_id}`} style={{ flex: 1 }}>
                    <Button style={{ width: '100%' }}>
                      Continue
                    </Button>
                  </Link>
                )}
                <Button 
                  variant="secondary" 
                  onClick={() => handleDelete(interview.interview_id)}
                  style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', border: 'none', padding: '0 12px' }}
                  title="Delete Interview"
                >
                  🗑️
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
      
      {modalConfig.isOpen && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.6)', backdropFilter: 'blur(4px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999
        }}>
          <div className="animate-fade-in" style={{
            background: 'var(--bg-secondary)', padding: '24px', borderRadius: '12px',
            border: '1px solid var(--border-glass)', width: '90%', maxWidth: '400px',
            boxShadow: '0 20px 40px rgba(0,0,0,0.4)', textAlign: 'center'
          }}>
            <h3 style={{ marginTop: 0, color: 'var(--text-primary)', fontSize: '1.25rem', marginBottom: '12px' }}>{modalConfig.title}</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '24px', lineHeight: 1.5 }}>{modalConfig.message}</p>
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
              {modalConfig.type === 'confirm' && (
                <Button variant="ghost" onClick={closeModal}>Cancel</Button>
              )}
              <Button onClick={() => {
                closeModal();
                if (modalConfig.onConfirm) modalConfig.onConfirm();
              }}>
                {modalConfig.type === 'confirm' ? 'Confirm' : 'OK'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
