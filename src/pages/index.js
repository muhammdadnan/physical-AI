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
            Get Started - Read the Book
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
      title={`Welcome to ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics - A comprehensive textbook">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h2>Module 1: ROS 2</h2>
                <p>Learn the fundamentals of Robot Operating System 2 for humanoid robotics applications.</p>
              </div>
              <div className="col col--4">
                <h2>Module 2: Digital Twin</h2>
                <p>Explore Gazebo physics simulation and Unity rendering for digital twin environments.</p>
              </div>
              <div className="col col--4">
                <h2>Module 3: AI-Robot Brain</h2>
                <p>Master NVIDIA Isaac Sim, VSLAM, and Nav2 for advanced humanoid AI systems.</p>
              </div>
            </div>
            <div className="row" style={{marginTop: '2rem'}}>
              <div className="col col--4 col--offset-2">
                <h2>Module 4: Vision-Language-Action</h2>
                <p>Build complete VLA systems with Whisper, LLMs, and ROS 2 action execution.</p>
              </div>
              <div className="col col--4">
                <h2>Hands-On Projects</h2>
                <p>Complete mini-projects and capstone challenges to reinforce your learning.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}