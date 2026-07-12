import React, { useState, useEffect } from 'react';
import styles from './PremiumApp.module.css';

/**
 * PremiumApp: A reference implementation for the react-premium-design skill.
 * Demonstrates clean architecture, light theme default, atomic component structure,
 * and a mandatory theme toggle mechanism based on CSS variables (tokens).
 */
export default function PremiumApp() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Apply theme to a wrapper or the document body in a real app.
  // Here we apply it to the main container as a data attribute.
  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  return (
    <div className={styles.appContainer} data-theme={isDarkMode ? 'dark' : 'light'}>
      
      {/* Navigation Layer */}
      <nav className={styles.navbar}>
        <div className={styles.logo}>Astryx Design</div>
        <div className={styles.navActions}>
          <button className={styles.navLink}>Products</button>
          <button className={styles.navLink}>Pricing</button>
          
          {/* Mandatory Theme Toggle */}
          <button 
            className={styles.themeToggle} 
            onClick={toggleTheme}
            aria-label="Toggle Theme"
          >
            {isDarkMode ? '☀️ Light' : '🌙 Dark'}
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <header className={styles.hero}>
        <h1 className={styles.title}>
          Build interfaces that <span className={styles.accentText}>breathe.</span>
        </h1>
        <p className={styles.subtitle}>
          A premium design system architecture for modern React applications. 
          Focus on typography, micro-interactions, and immaculate spacing.
        </p>
        <div className={styles.heroActions}>
          <button className={styles.primaryButton}>Get Started</button>
          <button className={styles.secondaryButton}>View Components</button>
        </div>
      </header>

      {/* Feature Section (Demonstrating Depth & Cards) */}
      <section className={styles.featureSection}>
        <div className={styles.card}>
          <div className={styles.cardIcon}>✨</div>
          <h3 className={styles.cardTitle}>Token-Based CSS</h3>
          <p className={styles.cardText}>
            Every color, shadow, and spacing unit is controlled by a strictly 
            defined semantic token hierarchy.
          </p>
        </div>
        
        <div className={styles.card}>
          <div className={styles.cardIcon}>⚡️</div>
          <h3 className={styles.cardTitle}>Micro-Animations</h3>
          <p className={styles.cardText}>
            Interfaces that feel alive. Active states scale down slightly, 
            hover states lift up with diffused shadows.
          </p>
        </div>
      </section>
      
    </div>
  );
}
