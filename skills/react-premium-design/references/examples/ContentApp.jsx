import React, { useState } from 'react';
import styles from './ContentApp.module.css';

/**
 * ContentApp: Blog / Documentation Reference Implementation
 * Style: Hyper-focused on readability, perfect typography, narrow width.
 */
export default function ContentApp() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  return (
    <div className={styles.appContainer} data-theme={isDarkMode ? 'dark' : 'light'}>
      
      {/* Minimal Header */}
      <header className={styles.header}>
        <div className={styles.logo}>Journal</div>
        <button className={styles.themeToggle} onClick={toggleTheme}>
          {isDarkMode ? 'Light' : 'Dark'} Mode
        </button>
      </header>

      {/* Main Content Article */}
      <article className={styles.article}>
        <header className={styles.articleHeader}>
          <time className={styles.meta}>July 12, 2026 • 5 min read</time>
          <h1 className={styles.title}>The Return to Craft in Web Design</h1>
          <p className={styles.standfirst}>
            Why the industry is moving away from generic component libraries and embracing bespoke, hyper-polished interfaces.
          </p>
          <div className={styles.author}>
            <div className={styles.authorAvatar}>A</div>
            <div>
              <div className={styles.authorName}>Alex Designer</div>
              <div className={styles.authorRole}>Lead Designer @ Astryx</div>
            </div>
          </div>
        </header>

        <div className={styles.prose}>
          <p>
            For the past decade, web design has been dominated by utility classes and brutalist efficiency. While these tools have democratized development, they've also homogenized the web. Every dashboard looks the same. Every landing page follows the same three-column grid.
          </p>
          
          <h2>The Resurgence of Detail</h2>
          <p>
            We are now seeing a massive shift. Users are tired of software that feels like a spreadsheet. They want tools that feel like physical objects—tools with weight, depth, and immediate physical feedback.
          </p>

          <blockquote>
            "Design is not just what it looks like and feels like. Design is how it works."
          </blockquote>

          <p>
            This doesn't mean we abandon our design systems. It means our design systems need to evolve. We must build tokens for <em>micro-animations</em>, not just colors. We need strict typographic scales that respect the golden ratio, and we need to embrace the power of modern CSS.
          </p>

          <h3>Next Steps</h3>
          <ul>
            <li>Audit your current component library for missing active states.</li>
            <li>Implement a strict 4px baseline grid.</li>
            <li>Stop using pure black (`#000000`) and pure white (`#FFFFFF`) in dark modes.</li>
          </ul>
        </div>
      </article>

    </div>
  );
}
