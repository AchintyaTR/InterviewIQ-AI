"use client";

import React, { useEffect, useState, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import TypewriterText from "@/components/TypewriterText";
import styles from "../interview.module.css";

interface ChatMessage {
  id: string;
  role: "interviewer" | "candidate";
  text: string;
}

interface InterviewState {
  interview_id: string;
  status: string;
  target_role: string;
  interview_mode: string;
  user_name?: string;
  history: Array<{
    id: string;
    role: "interviewer" | "candidate" | "system";
    text: string;
  }>;
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
  const scrollRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);
  const isRecordingRef = useRef(false);
  const finalTranscriptRef = useRef("");

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
    if (typeof window !== "undefined") {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        
        recognition.onstart = () => {
          console.log("Speech recognition started");
        };

        recognition.onresult = (event: any) => {
          console.log("Speech recognition result received:", event.results);
          let interimTranscript = "";
          for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
              finalTranscriptRef.current += event.results[i][0].transcript + " ";
            } else {
              interimTranscript += event.results[i][0].transcript;
            }
          }
          setTranscript((finalTranscriptRef.current + interimTranscript).trim());
        };
        
        recognition.onerror = (event: any) => {
          console.error("Speech recognition error:", event.error, event);
        };
        
        recognition.onend = () => {
          console.log("Speech recognition ended");
          if (isRecordingRef.current) {
            try {
              console.log("Attempting to restart recognition...");
              recognition.start();
            } catch(e) {
              console.error("Failed to restart:", e);
            }
          } else {
            setIsRecording(false);
          }
        };
        
        recognitionRef.current = recognition;
      }
    }
    
    return () => {
      if (recognitionRef.current) {
        isRecordingRef.current = false;
        recognitionRef.current.stop();
      }
    };
  }, []);

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

  // Auto-scroll to bottom of chat
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [interview?.history, isSubmitting]);

  const toggleRecording = () => {
    if (!recognitionRef.current) {
      showAlert("Unsupported Browser", "Speech recognition is not supported in your browser. Please try using Google Chrome.");
      return;
    }
    
    if (isRecordingRef.current) {
      isRecordingRef.current = false;
      setIsRecording(false);
      recognitionRef.current.stop();
    } else {
      // Preserve what was already in the textbox
      finalTranscriptRef.current = transcript ? transcript + " " : "";
      
      isRecordingRef.current = true;
      setIsRecording(true);
      try {
        recognitionRef.current.start();
      } catch (err) {
        console.error("Failed to start recording:", err);
      }
    }
  };

  const handleSubmitAnswer = async () => {
    if (!transcript.trim()) return;

    // Optimistically update chat
    const candidateMessage: ChatMessage = {
      id: `temp-${Date.now()}`,
      role: "candidate",
      text: transcript.trim()
    };
    
    setInterview(prev => prev ? {
      ...prev,
      history: [...prev.history, candidateMessage]
    } : null);

    const answerPayload = transcript.trim();
    setTranscript("");
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
        body: JSON.stringify({ answer_text: answerPayload })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to submit response");
      }

      const data = await res.json();

      if (data.status === "completed") {
        router.push(`/report/${id}`);
      } else {
        const nextMessage: ChatMessage = {
          id: data.next_question.id,
          role: "interviewer",
          text: data.next_question.text
        };
        
        setInterview(prev => {
          if (!prev) return null;
          // Filter out the temp candidate message since the API doesn't return candidate responses in this call,
          // but wait, we already added it. Actually, it's safer to just fetch the latest state from GET /interviews/{id} 
          // or just append the interviewer's new question!
          // We will append the interviewer's question to the existing optimistic history.
          return {
            ...prev,
            history: [...prev.history, nextMessage],
            latest_question: data.next_question,
            questions_count: prev.questions_count + 1
          };
        });
      }
    } catch (err: any) {
      console.error("Failed to submit response", err);
      showAlert("Submission Error", err.message || "An unexpected error occurred.");
      // Rollback optimistic update
      setInterview(prev => prev ? {
        ...prev,
        history: prev.history.filter(m => m.id !== candidateMessage.id)
      } : null);
      setTranscript(answerPayload);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEndInterview = () => {
    showConfirm(
      "End Interview Early?",
      "Are you sure you want to end the interview early? You will be evaluated on the questions answered so far.",
      async () => {
        setIsSubmitting(true);
        const token = localStorage.getItem("token");
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

        try {
          const res = await fetch(`${API_URL}/interviews/${id}/complete`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` }
          });

          if (!res.ok) throw new Error("Failed to end interview");
          
          router.push(`/report/${id}`);
        } catch (err) {
          console.error(err);
          showAlert("Error", "Failed to end interview early.");
          setIsSubmitting(false);
        }
      }
    );
  };

  if (isLoading) {
    return <div className={styles.loadingWrapper}><div className="animate-pulse-glow" style={{width: 40, height: 40, borderRadius: '50%', background: 'var(--accent-primary)'}} /></div>;
  }

  if (!interview) {
    return <div className={styles.container}><h2>Interview not found or already completed.</h2></div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <h1 className={styles.title}>{interview.target_role} Interview</h1>
          <div className={styles.status}>Question {interview.questions_count} / 5</div>
        </div>
        <Button 
          variant="secondary" 
          onClick={handleEndInterview} 
          disabled={isSubmitting}
        >
          End & Get Report
        </Button>
      </div>

      <div className={styles.chatScrollArea} ref={scrollRef}>
        {interview.history && interview.history.map((msg, index) => (
          <div key={msg.id || index} className={`${styles.messageWrapper} ${styles[msg.role]}`}>
            <div className={`${styles.messageBubble} ${styles[msg.role]}`}>
              <div className={styles.messageSender}>
                {msg.role === "interviewer" ? "AI Interviewer" : (interview.user_name || "You")}
              </div>
              {msg.role === "interviewer" ? (
                <TypewriterText 
                  text={msg.text} 
                  speed={interview.interview_mode === "voice" ? 45 : 15}
                  animate={index === interview.history.length - 1} 
                  playVoice={interview.interview_mode === "voice" && index === interview.history.length - 1}
                />
              ) : (
                msg.text
              )}
            </div>
          </div>
        ))}
        {isSubmitting && (
          <div className={`${styles.messageWrapper} ${styles.interviewer}`}>
            <div className={`${styles.messageBubble} ${styles.interviewer}`}>
              <div className={styles.messageSender}>AI Interviewer</div>
              <div className="animate-pulse">Thinking...</div>
            </div>
          </div>
        )}
      </div>

      <div className={styles.inputArea}>
        {interview.interview_mode === "voice" && (
          <div className={styles.controls}>
            <button 
              className={`${styles.recordBtn} ${isRecording ? styles.recording : ''}`}
              onClick={toggleRecording}
              title={isRecording ? "Stop Recording" : "Start Recording"}
            >
              {isRecording ? "■" : "🎙️"}
            </button>
          </div>
        )}
        
        <div className={styles.inputRow}>
          <textarea 
            className={styles.transcriptArea}
            placeholder="Type your answer here..."
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            disabled={isSubmitting}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmitAnswer();
              }
            }}
          />
          <Button 
            className={styles.submitBtn} 
            onClick={handleSubmitAnswer}
            isLoading={isSubmitting}
            disabled={!transcript.trim() || isRecording || isSubmitting}
          >
            Send
          </Button>
        </div>
      </div>
      
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
