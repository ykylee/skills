import React, { useState } from 'react';
import styles from './DashboardApp.module.css';

/**
 * DashboardApp: SaaS / Admin Panel Reference Implementation
 * Style: High density, sidebar navigation, tabular data, strict grid.
 */
export default function DashboardApp() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  return (
    <div className={styles.appContainer} data-theme={isDarkMode ? 'dark' : 'light'}>
      
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.sidebarBrand}>Acme Admin</div>
        <nav className={styles.sidebarNav}>
          <button className={`${styles.navItem} ${styles.active}`}>Overview</button>
          <button className={styles.navItem}>Customers</button>
          <button className={styles.navItem}>Analytics</button>
          <button className={styles.navItem}>Settings</button>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className={styles.mainContent}>
        
        {/* Topbar */}
        <header className={styles.topbar}>
          <h1 className={styles.pageTitle}>Dashboard Overview</h1>
          <div className={styles.topbarActions}>
            <button className={styles.themeToggle} onClick={toggleTheme}>
              {isDarkMode ? '☀️' : '🌙'}
            </button>
            <div className={styles.avatar}>A</div>
          </div>
        </header>

        {/* Content Body */}
        <div className={styles.contentBody}>
          
          {/* Stats Grid */}
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <div className={styles.statLabel}>Total Revenue</div>
              <div className={styles.statValue}>$45,231.89</div>
              <div className={styles.statTrendPositive}>+20.1% from last month</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statLabel}>Active Users</div>
              <div className={styles.statValue}>2,350</div>
              <div className={styles.statTrendPositive}>+180 new today</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statLabel}>Churn Rate</div>
              <div className={styles.statValue}>1.2%</div>
              <div className={styles.statTrendNegative}>-0.4% from last month</div>
            </div>
          </div>

          {/* Data Table Area */}
          <div className={styles.dataTableCard}>
            <div className={styles.cardHeader}>
              <h2 className={styles.cardTitle}>Recent Transactions</h2>
              <button className={styles.secondaryButton}>Export CSV</button>
            </div>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Transaction ID</th>
                  <th>Date</th>
                  <th>Amount</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>#TX-10023</td>
                  <td>2026-07-12</td>
                  <td>$1,250.00</td>
                  <td><span className={styles.badgeSuccess}>Completed</span></td>
                </tr>
                <tr>
                  <td>#TX-10024</td>
                  <td>2026-07-12</td>
                  <td>$45.50</td>
                  <td><span className={styles.badgeSuccess}>Completed</span></td>
                </tr>
                <tr>
                  <td>#TX-10025</td>
                  <td>2026-07-11</td>
                  <td>$3,200.00</td>
                  <td><span className={styles.badgePending}>Pending</span></td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </main>
    </div>
  );
}
