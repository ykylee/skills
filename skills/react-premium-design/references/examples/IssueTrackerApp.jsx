import React, { useState } from 'react';
import styles from './IssueTrackerApp.module.css';

/**
 * IssueTrackerApp: Jira / Linear style reference implementation
 * Style: Ultra-dense functional UI, multi-pane layouts, micro-tags, strict borders.
 */
export default function IssueTrackerApp() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  // Mock data for the issue list
  const issues = [
    { id: 'AST-104', title: 'Implement keyboard navigation in lists', status: 'In Progress', priority: 'High', assignee: 'Y' },
    { id: 'AST-103', title: 'Fix focus state on glassmorphism header', status: 'Todo', priority: 'Medium', assignee: 'Y' },
    { id: 'AST-102', title: 'Design system typography audit', status: 'Done', priority: 'Low', assignee: 'A' },
    { id: 'AST-101', title: 'Create initial React templates', status: 'Done', priority: 'High', assignee: 'A' },
  ];

  return (
    <div className={styles.appContainer} data-theme={isDarkMode ? 'dark' : 'light'}>
      
      {/* 1. Left Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.sidebarHeader}>
          <div className={styles.workspaceIcon}>A</div>
          <span className={styles.workspaceName}>Astryx Corp</span>
        </div>
        
        <div className={styles.navGroup}>
          <div className={styles.navGroupTitle}>Your Views</div>
          <button className={`${styles.navItem} ${styles.active}`}>My Issues</button>
          <button className={styles.navItem}>Active Cycle</button>
          <button className={styles.navItem}>Backlog</button>
        </div>

        <div className={styles.navGroup}>
          <div className={styles.navGroupTitle}>Projects</div>
          <button className={styles.navItem}>Frontend Replatform</button>
          <button className={styles.navItem}>Mobile App V2</button>
        </div>
        
        <div className={styles.sidebarFooter}>
          <button className={styles.themeToggle} onClick={toggleTheme}>
            {isDarkMode ? '☀️ Light' : '🌙 Dark'}
          </button>
        </div>
      </aside>

      {/* 2. Middle Pane: Issue List */}
      <div className={styles.listPane}>
        <header className={styles.listHeader}>
          <h1 className={styles.viewTitle}>My Issues</h1>
          <div className={styles.listActions}>
            <button className={styles.iconButton}>Filter</button>
            <button className={styles.iconButton}>Sort</button>
            <button className={styles.primaryButton}>New Issue</button>
          </div>
        </header>
        
        <div className={styles.issueList}>
          {issues.map(issue => (
            <div key={issue.id} className={`${styles.issueRow} ${issue.id === 'AST-104' ? styles.selected : ''}`}>
              <div className={styles.issueLeft}>
                <span className={styles.issueId}>{issue.id}</span>
                <span className={styles.issueStatusIcon} data-status={issue.status}></span>
                <span className={styles.issueTitle}>{issue.title}</span>
              </div>
              <div className={styles.issueRight}>
                <span className={styles.microTag} data-priority={issue.priority}>{issue.priority}</span>
                <div className={styles.assigneeAvatar}>{issue.assignee}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 3. Right Pane: Issue Details */}
      <div className={styles.detailPane}>
        <header className={styles.detailHeader}>
          <span className={styles.detailBreadcrumb}>Astryx Corp / AST-104</span>
          <div className={styles.detailActions}>
            <button className={styles.iconButton}>Copy Link</button>
            <button className={styles.iconButton}>Close</button>
          </div>
        </header>
        
        <div className={styles.detailContent}>
          <h2 className={styles.detailTitle}>Implement keyboard navigation in lists</h2>
          
          <div className={styles.detailProperties}>
            <div className={styles.propertyRow}>
              <span className={styles.propertyLabel}>Status</span>
              <span className={styles.propertyValue}>
                 <span className={styles.microTag}>In Progress</span>
              </span>
            </div>
            <div className={styles.propertyRow}>
              <span className={styles.propertyLabel}>Assignee</span>
              <span className={styles.propertyValue}>YongKyu Lee</span>
            </div>
            <div className={styles.propertyRow}>
              <span className={styles.propertyLabel}>Priority</span>
              <span className={styles.propertyValue}>High</span>
            </div>
          </div>
          
          <div className={styles.detailDescription}>
            <h3>Description</h3>
            <p>
              Users should be able to navigate the issue list using up/down arrows, 
              and press Enter to open the issue details in the right pane.
              Also, pressing 'Esc' should close the detail pane.
            </p>
            <p>
              Please ensure focus states are clearly visible for accessibility.
            </p>
          </div>
        </div>
      </div>

    </div>
  );
}
