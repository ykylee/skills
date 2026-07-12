import React, { useState } from 'react';
import styles from './CommerceApp.module.css';

/**
 * CommerceApp: E-Commerce / Showcase Reference Implementation
 * Style: Highly experiential, large imagery, bold CTAs, glassmorphism.
 */
export default function CommerceApp() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  return (
    <div className={styles.appContainer} data-theme={isDarkMode ? 'dark' : 'light'}>
      
      {/* Sticky Glassmorphic Header */}
      <header className={styles.header}>
        <div className={styles.logo}>Aura</div>
        <nav className={styles.nav}>
          <a href="#" className={styles.navLink}>Shop</a>
          <a href="#" className={styles.navLink}>Collections</a>
          <a href="#" className={styles.navLink}>About</a>
        </nav>
        <div className={styles.headerActions}>
          <button className={styles.iconButton} onClick={toggleTheme}>
            {isDarkMode ? '☀️' : '🌙'}
          </button>
          <button className={styles.cartButton}>
            Cart (2)
          </button>
        </div>
      </header>

      {/* Experiential Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>The Summer Collection</h1>
          <p className={styles.heroSubtitle}>Breathe in the new season with lightweight, breathable fabrics designed for movement.</p>
          <button className={styles.heroCta}>Shop Now</button>
        </div>
        {/* Placeholder for a large stunning background image */}
        <div className={styles.heroImageOverlay}></div>
      </section>

      {/* Product Grid (Masonry-style Showcase) */}
      <section className={styles.productSection}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Featured Drops</h2>
          <a href="#" className={styles.viewAll}>View All →</a>
        </div>
        
        <div className={styles.productGrid}>
          {/* Product Card 1 */}
          <div className={styles.productCard}>
            <div className={styles.imagePlaceholder}></div>
            <div className={styles.productInfo}>
              <h3 className={styles.productName}>Linen Over-shirt</h3>
              <p className={styles.productPrice}>$120</p>
            </div>
            <button className={styles.addToCartOverlay}>+ Add to Cart</button>
          </div>

          {/* Product Card 2 */}
          <div className={styles.productCard}>
            <div className={styles.imagePlaceholder}></div>
            <div className={styles.productInfo}>
              <h3 className={styles.productName}>Pleated Trousers</h3>
              <p className={styles.productPrice}>$145</p>
            </div>
            <button className={styles.addToCartOverlay}>+ Add to Cart</button>
          </div>

          {/* Product Card 3 */}
          <div className={styles.productCard}>
            <div className={styles.imagePlaceholder}></div>
            <div className={styles.productInfo}>
              <h3 className={styles.productName}>Woven Tote</h3>
              <p className={styles.productPrice}>$85</p>
            </div>
            <button className={styles.addToCartOverlay}>+ Add to Cart</button>
          </div>
        </div>
      </section>

    </div>
  );
}
