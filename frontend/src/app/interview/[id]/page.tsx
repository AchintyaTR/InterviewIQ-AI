"use client";

import React, { useEffect, useState, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import styles from "../interview.module.css";

interface InterviewState {
  status: string;
  target_role: string;
  latest_question: {
    id: string;
    text: string;
  } | null;
  questions_count: number;
}

export default function InterviewPage() {
  const { id } = useParams();
  const router = useRouter();
  const [interview, setInterview] = useState<InterviewState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchInterviewState = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/auth/login");
        return;
      }

      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      try {
        const res = await fetch(`${API_URL}/interviews/${id}`, {
          headers: { "Authorization": `Bearer ${token}` }
        });

        if (res.status === 401) {
          router.push("/auth/login");
          return;
        }

        const data = await res.json();
        
        if (data.status === "completed") {
          router.push(`/report/${id}`);
          return;
        }

        setInterview(data);
      } catch (err) {
        console.error("Failed to fetch interview state", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchInterviewState();
  }, [id, router]);

  // Mock Voice Recording Toggle
  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      // Simulate speech recognition starting
      setTranscript("");
    } else {
      // Simulate speech recognition ending
      if (!transcript) {
        setTranscript("I believe my strong background in React and Python makes me an excellent fit for this role.");
      }
    }
  };

  const handleSubmitAnswer = async () => {
    if (!transcript.trim()) return;

    setIsSubmitting(true);
    const token = localStorage.getItem("token");
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

    try {
      const res = await fetch(`${API_URL}/interviews/${id}/respond`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ answer_text: transcript })
      });

      const data = await res.json();

      if (data.status === "completed") {
        router.push(`/report/${id}`);
      } else {
        // Clear transcript and update question
        setTranscript("");
        setInterview(prev => prev ? {
          ...prev,
          latest_question: data.next_question,
          questions_count: prev.questions_count + 1
        } : null);
      }
    } catch (err) {
      console.error("Failed to submit response", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <div className={styles.loadingWrapper}><div className="animate-pulse-glow" style={{width: 40, height: 40, borderRadius: '50%', background: 'var(--accent-primary)'}} /></div>;
  }

  if (!interview || !interview.latest_question) {
    return <div className={styles.container}><h2>Interview not found or already completed.</h2></div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>{interview.target_role} Interview</h1>
        <div className={styles.status}>Question {interview.questions_count}</div>
      </div>

      <Card className={`animate-fade-in ${styles.questionCard}`}>
        <div className={styles.questionLabel}>AI Interviewer</div>
        <div className={styles.questionText}>
          "{interview.latest_question.text}"
        </div>

        <div className={styles.controls}>
          <button 
            className={`${styles.recordBtn} ${isRecording ? styles.recording : ''}`}
            onClick={toggleRecording}
            title={isRecording ? "Stop Recording" : "Start Recording"}
          >
            {isRecording ? "■" : "🎙️"}
          </button>
        </div>

        <textarea 
          className={styles.transcriptArea}
          placeholder="Speak into your microphone or type your answer here..."
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
        />

        <Button 
          className={styles.submitBtn} 
          onClick={handleSubmitAnswer}
          isLoading={isSubmitting}
          disabled={!transcript.trim() || isRecording}
        >
          Submit Answer
        </Button>
      </Card>
    </div>
  );
}
