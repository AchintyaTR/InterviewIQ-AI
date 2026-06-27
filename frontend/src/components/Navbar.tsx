"use client";

import React, { useEffect, useState, useRef } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import styles from "./Navbar.module.css";

export default function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const router = useRouter();
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const checkLogin = () => {
      setIsLoggedIn(!!localStorage.getItem("token"));
    };
    
    checkLogin();
    window.addEventListener("storage", checkLogin);
    window.addEventListener("auth-change", checkLogin);
    
    return () => {
      window.removeEventListener("storage", checkLogin);
      window.removeEventListener("auth-change", checkLogin);
    };
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    setDropdownOpen(false);
    window.dispatchEvent(new Event("auth-change"));
    router.push("/");
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link href="/" className="logo text-gradient" style={{ textDecoration: 'none' }}>InterviewIQ</Link>
        <div className="nav-links">
          {isLoggedIn ? (
            <div className={styles.profileMenu} ref={dropdownRef}>
              <button 
                className={styles.profileBtn}
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                Profile ▾
              </button>
              {dropdownOpen && (
                <div className={styles.dropdown}>
                  <Link href="/dashboard" className={styles.dropdownItem} onClick={() => setDropdownOpen(false)}>
                    Dashboard
                  </Link>
                  <button onClick={handleLogout} className={styles.dropdownItem}>
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <Link href="/auth/login" className="nav-link login-btn">Login</Link>
          )}
        </div>
      </div>
    </nav>
  );
}
