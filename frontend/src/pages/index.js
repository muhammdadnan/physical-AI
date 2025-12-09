import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Read the Book - 5min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="A comprehensive textbook on Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section className="container">
          <div className="text--center padding-horiz--md">
            <h2>Welcome to the Physical AI & Humanoid Robotics Textbook</h2>
            <p>
              This comprehensive textbook covers everything from ROS 2 fundamentals to
              Vision-Language-Action (VLA) systems for humanoid robots.
            </p>
            <p>
              Explore the modules to learn about Digital Twin technologies, NVIDIA Isaac,
              VSLAM, Nav2, and advanced robotics AI systems.
            </p>
          </div>
        </section>
      </main>
    </Layout>
  );
}