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
  const [targetCompany, setTargetCompany] = useState("");
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

      if (!resumeRes.ok) {
        throw new Error("Failed to upload and parse resume.");
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
          target_company: targetCompany || "General"
        })
      });

      if (!startRes.ok) {
        throw new Error("Failed to start interview.");
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

          <Input
            label="Target Company (Optional)"
            type="text"
            placeholder="e.g. Google, Stripe, Startup"
            value={targetCompany}
            onChange={(e) => setTargetCompany(e.target.value)}
          />

          <Button type="submit" size="lg" className={styles.submitBtn} isLoading={isLoading}>
            {isLoading ? statusText : "Start Interview"}
          </Button>
        </form>
      </Card>
    </div>
  );
}
