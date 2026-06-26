import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.container}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className="animate-fade-in">
          <div className={styles.badge}>
            <span className={styles.badgeDot}></span>
            Now Powered by Llama 3.1
          </div>
          
          <h1 className={styles.title}>
            Master Your Next Interview with <br />
            <span className="text-gradient">AI-Powered Mock Sessions</span>
          </h1>
          
          <p className={styles.subtitle}>
            Upload your resume, select your target role, and experience a realistic 
            voice-based interview tailored to your unique background. Get instant, 
            actionable feedback to land your dream job.
          </p>
          
          <div className={styles.ctaGroup}>
            <Link href="/auth/register">
              <Button size="lg" className="animate-pulse-glow">
                Start Practicing Free
              </Button>
            </Link>
            <Link href="/auth/login">
              <Button variant="secondary" size="lg">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className={styles.features}>
        <div className={styles.featuresGrid}>
          <Card hoverable className="animate-fade-in" style={{ animationDelay: "0.2s" }}>
            <div className={styles.iconWrapper}>📄</div>
            <h3>Resume Parsing</h3>
            <p className="text-secondary">
              Our AI extracts your skills and projects to formulate highly personalized questions.
            </p>
          </Card>
          
          <Card hoverable className="animate-fade-in" style={{ animationDelay: "0.4s" }}>
            <div className={styles.iconWrapper}>🎙️</div>
            <h3>Voice Recognition</h3>
            <p className="text-secondary">
              Answer naturally using your microphone. Our Whisper integration perfectly transcribes your speech.
            </p>
          </Card>
          
          <Card hoverable className="animate-fade-in" style={{ animationDelay: "0.6s" }}>
            <div className={styles.iconWrapper}>📊</div>
            <h3>Deep Evaluation</h3>
            <p className="text-secondary">
              Receive a detailed scorecard grading your communication, problem-solving, and technical accuracy.
            </p>
          </Card>
        </div>
      </section>
    </div>
  );
}
