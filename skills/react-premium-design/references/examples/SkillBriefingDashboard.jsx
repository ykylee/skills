import React, { useState } from 'react';
import styles from './SkillBriefingDashboard.module.css';

/**
 * SkillBriefingDashboard: A briefing dashboard for the Skills repository.
 * Built using the SaaS/Admin Dashboard archetype from react-premium-design.
 */
export default function SkillBriefingDashboard() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  const skills = [
    { id: 'html-slides-builder', category: 'Generative UI', version: '1.2.0', status: 'Active', description: 'Generates HTML/CSS presentation decks.' },
    { id: 'react-premium-design', category: 'Generative UI', version: '2.0.0', status: 'Active', description: 'Provides 4 React design archetypes.' },
    { id: 'skill-discover', category: 'Meta', version: '0.1.0', status: 'Stable', description: 'Search and recommendation engine for skills.' },
    { id: 'skill-lint', category: 'Meta', version: '0.2.0', status: 'Stable', description: 'Validates SKILL.md frontmatter and structure.' }
  ];

  return (
    <div className={styles.appContainer} data-theme={isDarkMode ? 'dark' : 'light'}>
      
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.sidebarBrand}>Skills Repo Admin</div>
        <nav className={styles.sidebarNav}>
          <button className={`${styles.navItem} ${styles.active}`}>Overview</button>
          <button className={styles.navItem}>Catalog</button>
          <button className={styles.navItem}>Analytics</button>
          <button className={styles.navItem}>Settings</button>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className={styles.mainContent}>
        
        {/* Topbar */}
        <header className={styles.topbar}>
          <h1 className={styles.pageTitle}>Skill Development Briefing</h1>
          <div className={styles.topbarActions}>
            <button className={styles.themeToggle} onClick={toggleTheme}>
              {isDarkMode ? '☀️ Light' : '🌙 Dark'}
            </button>
            <div className={styles.avatar}>A</div>
          </div>
        </header>

        {/* Content Body */}
        <div className={styles.contentBody}>
          
          {/* Stats Grid */}
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <div className={styles.statLabel}>Total Skills Built</div>
              <div className={styles.statValue}>4</div>
              <div className={styles.statTrendPositive}>100% Ready for production</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statLabel}>Generative UI Skills</div>
              <div className={styles.statValue}>2</div>
              <div className={styles.statTrendPositive}>React & HTML based</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statLabel}>Meta Skills</div>
              <div className={styles.statValue}>2</div>
              <div className={styles.statTrendNeutral}>CI/CD & Discovery</div>
            </div>
          </div>

          {/* Data Table Area */}
          <div className={styles.dataTableCard}>
            <div className={styles.cardHeader}>
              <h2 className={styles.cardTitle}>Skill Catalog Directory</h2>
              <button className={styles.secondaryButton}>Export Manifest</button>
            </div>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Skill Name</th>
                  <th>Category</th>
                  <th>Version</th>
                  <th>Status</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {skills.map(skill => (
                  <tr key={skill.id}>
                    <td className={styles.fontWeightBold}>{skill.id}</td>
                    <td>{skill.category}</td>
                    <td>{skill.version}</td>
                    <td>
                      <span className={skill.status === 'Active' ? styles.badgeSuccess : styles.badgeStable}>
                        {skill.status}
                      </span>
                    </td>
                    <td className={styles.colorMuted}>{skill.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
      </main>
    </div>
  );
}
