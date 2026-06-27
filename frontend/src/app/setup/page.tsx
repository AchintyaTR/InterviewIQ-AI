"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import styles from "./setup.module.css";

export default function SetupPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [targetRole, setTargetRole] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("fresher");
  const [interviewMode, setInterviewMode] = useState<"voice" | "text">("voice");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [statusText, setStatusText] = useState("Start Interview");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please upload your resume.");
      return;
    }
    
    setIsLoading(true);
    setError("");
    
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth/login");
      return;
    }
    
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

    try {
      // Step 1: Upload Resume
      setStatusText("Parsing Resume...");
      const formData = new FormData();
      formData.append("file", file);

      const resumeRes = await fetch(`${API_URL}/resumes/upload`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: formData,
      });

      if (resumeRes.status === 401) {
        router.push("/auth/login");
        return;
      }

      if (!resumeRes.ok) {
        const errData = await resumeRes.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to upload and parse resume.");
      }
      const resumeData = await resumeRes.json();
      const resumeId = resumeData.resume_id;

      // Step 2: Start Interview
      setStatusText("Generating Interview...");
      const startRes = await fetch(`${API_URL}/interviews/start`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          resume_id: resumeId,
          target_role: targetRole,
          interview_mode: interviewMode,
          experience_level: experienceLevel
        })
      });

      if (startRes.status === 401) {
        router.push("/auth/login");
        return;
      }

      if (!startRes.ok) {
        const errData = await startRes.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to start interview.");
      }
      
      const startData = await startRes.json();
      
      // Navigate to the interview session
      router.push(`/interview/${startData.interview_id}`);

    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
      setStatusText("Start Interview");
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card className={`animate-fade-in ${styles.setupCard}`}>
        <div className={styles.header}>
          <h1 className={styles.title}>Interview Setup</h1>
          <p className={styles.subtitle}>Upload your resume and tell us what you're applying for.</p>
        </div>

        {error && <div className={styles.errorAlert}>{error}</div>}

        <form className={styles.form} onSubmit={handleSubmit}>
          
          <div className={styles.fileUploadWrapper}>
            <input 
              type="file" 
              accept=".pdf,.docx" 
              className={styles.fileInput} 
              onChange={handleFileChange}
              required
            />
            <div className={styles.uploadIcon}>📄</div>
            <div className={styles.uploadText}>
              Drag & drop or click to upload resume
            </div>
            <div className={styles.uploadSubtext}>
              Supports PDF and DOCX
            </div>
            {file && (
              <div className={styles.selectedFile}>
                ✓ Selected: {file.name}
              </div>
            )}
          </div>

          <Input
            label="Target Role"
            type="text"
            placeholder="e.g. Senior Frontend Engineer"
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
            required
          />

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              Experience Level
            </label>
            <select
              value={experienceLevel}
              onChange={(e) => setExperienceLevel(e.target.value)}
              style={{
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid var(--border-glass)',
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                fontSize: '1rem',
                outline: 'none',
                width: '100%',
                cursor: 'pointer'
              }}
            >
              <option value="fresher">Fresher</option>
              <option value="2+ years">2+ years</option>
              <option value="5+ years">5+ years</option>
              <option value="10+ years">10+ years</option>
              <option value="15+ years">15+ years</option>
            </select>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              Interview Mode
            </label>
            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                type="button"
                onClick={() => setInterviewMode("voice")}
                style={{
                  flex: 1,
                  padding: '12px',
                  borderRadius: '8px',
                  border: `2px solid ${interviewMode === 'voice' ? 'var(--accent-primary)' : 'var(--border-glass)'}`,
                  background: interviewMode === 'voice' ? 'rgba(56, 189, 248, 0.1)' : 'var(--bg-secondary)',
                  color: 'var(--text-primary)',
                  cursor: 'pointer',
                  fontWeight: 600,
                  transition: 'all 0.2s'
                }}
              >
                🎙️ Voice
              </button>
              <button
                type="button"
                onClick={() => setInterviewMode("text")}
                style={{
                  flex: 1,
                  padding: '12px',
                  borderRadius: '8px',
                  border: `2px solid ${interviewMode === 'text' ? 'var(--accent-primary)' : 'var(--border-glass)'}`,
                  background: interviewMode === 'text' ? 'rgba(56, 189, 248, 0.1)' : 'var(--bg-secondary)',
                  color: 'var(--text-primary)',
                  cursor: 'pointer',
                  fontWeight: 600,
                  transition: 'all 0.2s'
                }}
              >
                ⌨️ Text
              </button>
            </div>
          </div>

          <Button type="submit" size="lg" className={styles.submitBtn} isLoading={isLoading}>
            {isLoading ? statusText : "Start Interview"}
          </Button>
        </form>
      </Card>
    </div>
  );
}
