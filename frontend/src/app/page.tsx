'use client';

import React, { useState } from 'react';

export default function Home() {
  const [activeStep, setActiveStep] = useState(0);

  const mockSteps = [
    {
      title: "1. Upload Resume",
      desc: "Our AI parser extracts skills, projects, and work history to understand your professional background."
    },
    {
      title: "2. Generate adaptive mock questions",
      desc: "LLMs create targeted questions that test your specific credentials and role preferences."
    },
    {
      title: "3. Voice & coding session",
      desc: "Conduct simulated live rounds with speech input and real-time sandbox code assessment."
    },
    {
      title: "4. Receive custom performance evaluation",
      desc: "Get an interactive score report covering technical depth, communication, and learning roadmaps."
    }
  ];

  return (
    <div style={{ position: 'relative', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Background glow graphics */}
      <div className="glow-bg glow-left" />
      <div className="glow-bg glow-right" />

      {/* Header section */}
      <header style={{ borderBottom: '1px solid var(--border-color)', backdropFilter: 'blur(12px)', sticky: 'top', zIndex: 10 }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1.5rem 2rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ width: '40px', height: '40px', borderRadius: '10px', background: 'linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%)', display: 'flex', justifyContent: 'center', alignItems: 'center', fontWeight: 'bold' }}>
              IQ
            </div>
            <span style={{ fontSize: '1.25rem', fontWeight: 'bold', fontFamily: 'var(--font-heading)' }}>InterviewIQ <span style={{ color: 'var(--accent-teal)' }}>AI</span></span>
          </div>
          
          <nav style={{ display: 'flex', gap: '2rem' }}>
            <a href="#features" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'color 0.2s' }}>Features</a>
            <a href="#workflow" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'color 0.2s' }}>How it Works</a>
            <a href="#docs" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'color 0.2s' }}>Docs</a>
          </nav>

          <button className="btn-secondary" style={{ padding: '0.6rem 1.2rem', borderRadius: '8px' }}>
            Sign In
          </button>
        </div>
      </header>

      {/* Hero section */}
      <main style={{ flex: 1, maxWidth: '1200px', margin: '0 auto', padding: '6rem 2rem', display: 'flex', flexDirection: 'column', gap: '8rem' }}>
        <section style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', gap: '2rem' }}>
          <div style={{ border: '1px solid rgba(99, 102, 241, 0.2)', backgroundColor: 'rgba(99, 102, 241, 0.05)', padding: '0.5rem 1rem', borderRadius: '50px', display: 'inline-flex', gap: '0.5rem', alignItems: 'center', fontSize: '0.875rem' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--accent-teal)' }} />
            Next-gen Interview Preparation Platform
          </div>

          <h1 style={{ fontSize: '4.5rem', lineHeight: '1.1', maxWidth: '900px' }} className="gradient-text">
            Simulate Realistic Mock Interviews Powered by AI
          </h1>
          
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.25rem', maxWidth: '650px' }}>
            Upload your resume, customize target roles, and practice with real-time adaptive voice prompts, coding rounds, and comprehensive reports.
          </p>

          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <button className="btn-primary" style={{ padding: '1.2rem 2.5rem', fontSize: '1.1rem' }}>
              Get Started for Free
            </button>
            <button className="btn-secondary" style={{ padding: '1.2rem 2.5rem', fontSize: '1.1rem' }}>
              Explore Documentation
            </button>
          </div>
        </section>

        {/* Feature section */}
        <section id="features" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
          <div style={{ textAlign: 'center' }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Robust AI Interviewing Modules</h2>
            <p style={{ color: 'var(--text-secondary)' }}>Standardized core subsystems built for realistic evaluations.</p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem' }}>
            <div className="glass-card">
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>📄</div>
              <h3 style={{ fontSize: '1.5rem', marginBottom: '0.75rem' }}>Semantic Resume Parser</h3>
              <p style={{ color: 'var(--text-secondary)' }}>Extracts technical competencies, project scopes, and languages to generate matching technical profiles.</p>
            </div>

            <div className="glass-card">
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🎙️</div>
              <h3 style={{ fontSize: '1.5rem', marginBottom: '0.75rem' }}>Adaptive Audio Sessions</h3>
              <p style={{ color: 'var(--text-secondary)' }}>Conducted via Whisper Speech-to-Text and TTS pipelines for natural verbal communication assessments.</p>
            </div>

            <div className="glass-card">
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>📊</div>
              <h3 style={{ fontSize: '1.5rem', marginBottom: '0.75rem' }}>RAG Evaluation Engine</h3>
              <p style={{ color: 'var(--text-secondary)' }}>Generates custom company-specific questions matching real historical hiring patterns and metrics.</p>
            </div>
          </div>
        </section>

        {/* Interactive workflow stepper */}
        <section id="workflow" style={{ display: 'flex', flexDirection: 'column', gap: '4rem' }}>
          <div style={{ textAlign: 'center' }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Interactive Interview Pipeline</h2>
            <p style={{ color: 'var(--text-secondary)' }}>See how InterviewIQ guides candidates from uploads to custom roadmap recommendations.</p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4rem', alignItems: 'center' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              {mockSteps.map((step, idx) => (
                <div 
                  key={idx}
                  onClick={() => setActiveStep(idx)}
                  style={{
                    padding: '1.5rem',
                    borderRadius: '16px',
                    border: '1px solid',
                    borderColor: activeStep === idx ? 'rgba(99, 102, 241, 0.3)' : 'var(--glass-border)',
                    backgroundColor: activeStep === idx ? 'rgba(99, 102, 241, 0.05)' : 'transparent',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease'
                  }}
                >
                  <h4 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: activeStep === idx ? 'var(--text-primary)' : 'var(--text-secondary)' }}>
                    {step.title}
                  </h4>
                  {activeStep === idx && (
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                      {step.desc}
                    </p>
                  )}
                </div>
              ))}
            </div>

            {/* Display container reflecting active step state */}
            <div className="glass-card" style={{ height: '350px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center', gap: '1.5rem', background: 'radial-gradient(circle at top left, rgba(99, 102, 241, 0.05) 0%, transparent 100%), var(--bg-secondary)' }}>
              <div style={{ fontSize: '4rem' }}>
                {activeStep === 0 && '📤'}
                {activeStep === 1 && '🤖'}
                {activeStep === 2 && '💻'}
                {activeStep === 3 && '📈'}
              </div>
              <h3 style={{ fontSize: '1.75rem' }}>{mockSteps[activeStep].title}</h3>
              <p style={{ color: 'var(--text-secondary)', maxWidth: '400px' }}>{mockSteps[activeStep].desc}</p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer section */}
      <footer style={{ borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-secondary)', padding: '3rem 2rem', marginTop: '6rem' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ color: 'var(--text-tertiary)', fontSize: '0.9rem' }}>© 2026 InterviewIQ AI. All rights reserved.</span>
          <div style={{ display: 'flex', gap: '2rem' }}>
            <a href="#" style={{ color: 'var(--text-tertiary)', textDecoration: 'none' }}>Privacy Policy</a>
            <a href="#" style={{ color: 'var(--text-tertiary)', textDecoration: 'none' }}>Terms of Service</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
