"use client";

import React, { useState, useEffect } from "react";

interface TypewriterTextProps {
  text: string;
  speed?: number; // milliseconds per character
  animate?: boolean;
  playVoice?: boolean;
  onComplete?: () => void;
}

export default function TypewriterText({ text, speed = 30, animate = true, playVoice = false, onComplete }: TypewriterTextProps) {
  const [displayedText, setDisplayedText] = useState(animate ? "" : text);
  const [currentIndex, setCurrentIndex] = useState(animate ? 0 : text.length);

  // Reset when text changes completely
  useEffect(() => {
    if (animate) {
      setDisplayedText("");
      setCurrentIndex(0);
      
      if (playVoice && typeof window !== "undefined" && window.speechSynthesis) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        // Optional: find a good voice
        const voices = window.speechSynthesis.getVoices();
        const englishVoice = voices.find(v => v.lang.startsWith('en-') && (v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Natural')));
        if (englishVoice) {
          utterance.voice = englishVoice;
        }
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
      }
      
    } else {
      setDisplayedText(text);
      setCurrentIndex(text.length);
    }
    
    return () => {
      if (playVoice && typeof window !== "undefined" && window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, [text, animate, playVoice]);

  useEffect(() => {
    if (!animate) return;
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText(prev => prev + text[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, speed);
      
      return () => clearTimeout(timeout);
    } else if (currentIndex === text.length && text.length > 0) {
      if (onComplete) {
        onComplete();
      }
    }
  }, [currentIndex, text, speed, onComplete]);

  return (
    <span>
      {displayedText}
      {currentIndex < text.length && (
        <span style={{ 
          display: 'inline-block', 
          width: '4px', 
          height: '1em', 
          background: 'var(--accent-primary)', 
          marginLeft: '2px',
          verticalAlign: 'middle',
          animation: 'pulse-glow 1s infinite'
        }} />
      )}
    </span>
  );
}
