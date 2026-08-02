import { useState, useEffect } from 'react'
import './App.css'

const KONAMI = [
  'ArrowUp','ArrowUp','ArrowDown','ArrowDown',
  'ArrowLeft','ArrowRight','ArrowLeft','ArrowRight',
  'b','a',
]

function useKonami(onSuccess: () => void) {
  useEffect(() => {
    let pos = 0
    const handler = (e: KeyboardEvent) => {
      if (e.key === KONAMI[pos]) {
        pos++
        if (pos === KONAMI.length) { pos = 0; onSuccess() }
      } else {
        pos = e.key === KONAMI[0] ? 1 : 0
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onSuccess])
}

const features = [
  {
    icon: '☁️',
    colorClass: 'icon-blue',
    title: 'Hands-on Labs',
    desc: 'Practice in real AWS, Azure and GCP environments — no local setup required.',
  },
  {
    icon: '🏆',
    colorClass: 'icon-yellow',
    title: 'Industry Certifications',
    desc: 'Structured learning paths aligned with AWS, Azure, GCP and Terraform exams.',
  },
  {
    icon: '🤖',
    colorClass: 'icon-purple',
    title: 'AI-Powered Guidance',
    desc: 'Personalised recommendations and instant answers as you learn.',
  },
  {
    icon: '📈',
    colorClass: 'icon-green',
    title: 'Skill Assessments',
    desc: 'Benchmark your knowledge and track progress with detailed analytics.',
  },
  {
    icon: '👥',
    colorClass: 'icon-red',
    title: 'Team Learning',
    desc: 'Manage training for your whole team with dashboards and role assignments.',
  },
  {
    icon: '🔄',
    colorClass: 'icon-blue',
    title: 'Always Up-to-Date',
    desc: 'Content updated continuously to reflect the latest cloud services and best practices.',
  },
]

const courses = [
  {
    emoji: '🚀',
    level: 'Beginner',
    title: 'AWS Solutions Architect',
    desc: 'Master core AWS services and design resilient, scalable cloud architectures.',
    hours: '40h',
    labs: '28 labs',
  },
  {
    emoji: '⚙️',
    level: 'Intermediate',
    title: 'Terraform & IaC',
    desc: 'Provision and manage cloud infrastructure as code across multiple providers.',
    hours: '20h',
    labs: '15 labs',
  },
  {
    emoji: '🔁',
    level: 'Intermediate',
    title: 'CI/CD with GitHub Actions',
    desc: 'Build end-to-end pipelines: lint, test, build, and deploy automatically.',
    hours: '16h',
    labs: '12 labs',
  },
  {
    emoji: '🐳',
    level: 'Advanced',
    title: 'Kubernetes & EKS',
    desc: 'Deploy and operate production-grade Kubernetes clusters on Amazon EKS.',
    hours: '32h',
    labs: '22 labs',
  },
  {
    emoji: '🔒',
    level: 'Intermediate',
    title: 'AWS Security & IAM',
    desc: 'Implement least-privilege access, OIDC federation, and compliance controls.',
    hours: '18h',
    labs: '14 labs',
  },
  {
    emoji: '🌐',
    level: 'Beginner',
    title: 'Cloud Networking',
    desc: 'VPCs, subnets, routing, load balancers and global delivery with CloudFront.',
    hours: '24h',
    labs: '18 labs',
  },
]

const steps = [
  { n: '1', title: 'Create your account', desc: 'Sign up free and complete a quick skill assessment.' },
  { n: '2', title: 'Choose a learning path', desc: 'Pick a certification track or topic that matches your goals.' },
  { n: '3', title: 'Learn by doing', desc: 'Complete video lessons and spin up real cloud lab environments.' },
  { n: '4', title: 'Get certified', desc: 'Earn your certification and share your achievements.' },
]

const levelClass: Record<string, string> = {
  Beginner: 'level-beginner',
  Intermediate: 'level-intermediate',
  Advanced: 'level-advanced',
}

export default function App() {
  const [easterEgg, setEasterEgg] = useState(false)
  useKonami(() => setEasterEgg(true))

  return (
    <>
      {/* ── Easter egg modal ── */}
      {easterEgg && (
        <div className="egg-overlay" onClick={() => setEasterEgg(false)}>
          <div className="egg-modal" onClick={(e) => e.stopPropagation()}>
            <button type="button" className="egg-close" onClick={() => setEasterEgg(false)}>✕</button>
            <div className="egg-icon">🕵️</div>
            <h2 className="egg-title">Classified Intelligence Report</h2>
            <p className="egg-sub">⚠️ LEVEL 5 — EYES ONLY ⚠️</p>
            <div className="egg-body">
              <p>Our analysts have identified a <strong>critical infrastructure gap</strong>.</p>
              <p>
                <strong>🐟 Boston</strong> and <strong>🧑‍💻 Amir Shacham</strong> have yet to
                provision their S3 bucket, configure CloudFront, write a single line of
                Terraform, or set up a GitHub Actions workflow.
              </p>
              <p>
                The pipeline is <em>not</em> going to build itself, gentlemen.
              </p>
              <div className="egg-todo">
                <p>Pending action items:</p>
                <ul>
                  <li>☐ Write <code>main.tf</code></li>
                  <li>☐ Run <code>terraform apply</code></li>
                  <li>☐ Push to <code>main</code></li>
                  <li>☐ Explain what OIDC actually is</li>
                  <li>☐ Buy Lirone a coffee ☕</li>
                </ul>
              </div>
              <p className="egg-footer">This message will self-destruct when they submit their repo.</p>
            </div>
            <button type="button" className="egg-dismiss" onClick={() => setEasterEgg(false)}>
              🫡 Understood. I'll get to work.
            </button>
          </div>
        </div>
      )}

      {/* ── Navbar ── */}
      <nav className="navbar">
        <div className="navbar-inner">
          <a href="#" className="nav-logo">
            <span className="nav-logo-icon">☁</span>
            Cloud Academy
          </a>

          <ul className="nav-links">
            <li><a href="#courses">Courses</a></li>
            <li><a href="#features">Features</a></li>
            <li><a href="#how">How it works</a></li>
            <li><a href="#courses" className="nav-cta">Start learning</a></li>
          </ul>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="hero">
        <div className="hero-badge">🎓 Trusted by 200,000+ cloud professionals</div>
        <h1>
          Master the Cloud.<br />
          <span>Ship with Confidence.</span>
        </h1>
        <p className="hero-subtitle">
          Hands-on courses, real cloud labs, and certification prep — all in one place.
          Learn AWS, Terraform, Kubernetes, CI/CD and more.
        </p>
        <div className="hero-actions">
          <button type="button" className="btn-primary">Start for free →</button>
          <button type="button" className="btn-secondary">View all courses</button>
        </div>

        <div className="hero-stats">
          <div className="stat">
            <span className="stat-value">200k+</span>
            <span className="stat-label">Active learners</span>
          </div>
          <div className="stat">
            <span className="stat-value">500+</span>
            <span className="stat-label">Hands-on labs</span>
          </div>
          <div className="stat">
            <span className="stat-value">98%</span>
            <span className="stat-label">Pass rate</span>
          </div>
          <div className="stat">
            <span className="stat-value">4.9★</span>
            <span className="stat-label">Average rating</span>
          </div>
        </div>
      </section>

      {/* ── Logos ── */}
      <div className="logos-bar">
        <p>Trusted by teams at</p>
        <div className="logos-list">
          <span>Amazon</span>
          <span>Atlassian</span>
          <span>Spotify</span>
          <span>Shopify</span>
          <span>Stripe</span>
          <span>Airbnb</span>
        </div>
      </div>

      {/* ── Features ── */}
      <section className="section" id="features">
        <div className="section-inner">
          <div className="section-header">
            <span className="section-tag">Why Cloud Academy</span>
            <h2>Everything you need to grow in the cloud</h2>
            <p>Built for engineers, DevOps teams and cloud architects who learn by doing.</p>
          </div>

          <div className="features-grid">
            {features.map((f) => (
              <div className="feature-card" key={f.title}>
                <div className={`feature-icon ${f.colorClass}`}>
                  {f.icon}
                </div>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Courses ── */}
      <section className="section section-alt" id="courses">
        <div className="section-inner">
          <div className="section-header">
            <span className="section-tag">Learning Paths</span>
            <h2>Popular courses</h2>
            <p>From beginner to advanced — structured paths to cloud mastery.</p>
          </div>

          <div className="courses-grid">
            {courses.map((c) => (
              <div className="course-card" key={c.title}>
                <div className="course-header">
                  <span className="course-emoji">{c.emoji}</span>
                  <div className="course-meta">
                    <span className={`course-level ${levelClass[c.level]}`}>{c.level}</span>
                    <span className="course-title">{c.title}</span>
                  </div>
                </div>
                <div className="course-body">
                  <p className="course-desc">{c.desc}</p>
                  <div className="course-footer">
                    <div className="course-info">
                      <span>⏱ {c.hours}</span>
                      <span>🧪 {c.labs}</span>
                    </div>
                    <button type="button" className="course-enroll">Enrol →</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How it works ── */}
      <section className="section" id="how">
        <div className="section-inner">
          <div className="section-header">
            <span className="section-tag">How it works</span>
            <h2>Your path from zero to certified</h2>
            <p>A simple four-step journey to cloud expertise.</p>
          </div>

          <div className="steps">
            {steps.map((s) => (
              <div className="step" key={s.n}>
                <div className="step-number">{s.n}</div>
                <h3>{s.title}</h3>
                <p>{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <div className="cta-banner">
        <h2>Ready to level up your cloud skills?</h2>
        <p>Join 200,000+ engineers already learning on Cloud Academy.</p>
        <button type="button" className="btn-white">Get started for free</button>
      </div>

      {/* ── Footer ── */}
      <footer className="footer">
        <div className="footer-inner">
          <div className="footer-top">
            <div className="footer-brand">
              <span className="nav-logo">
                <span className="nav-logo-icon">☁</span>
                Cloud Academy
              </span>
              <p>The leading platform for hands-on cloud training and certification preparation.</p>
            </div>

            <div className="footer-cols">
              <div className="footer-col">
                <h4>Learn</h4>
                <ul>
                  <li><a href="#">AWS Courses</a></li>
                  <li><a href="#">Azure Courses</a></li>
                  <li><a href="#">GCP Courses</a></li>
                  <li><a href="#">Terraform</a></li>
                  <li><a href="#">Kubernetes</a></li>
                </ul>
              </div>
              <div className="footer-col">
                <h4>Company</h4>
                <ul>
                  <li><a href="#">About us</a></li>
                  <li><a href="#">Blog</a></li>
                  <li><a href="#">Careers</a></li>
                  <li><a href="#">Press</a></li>
                </ul>
              </div>
              <div className="footer-col">
                <h4>Support</h4>
                <ul>
                  <li><a href="#">Help centre</a></li>
                  <li><a href="#">Contact</a></li>
                  <li><a href="#">Status</a></li>
                  <li><a href="#">Community</a></li>
                </ul>
              </div>
            </div>
          </div>

          <div className="footer-bottom">
            <p>© {new Date().getFullYear()} Cloud Academy Inc. All rights reserved.</p>
            <div className="footer-bottom-links">
              <a href="#">Privacy</a>
              <a href="#">Terms</a>
              <a href="#">Cookies</a>
            </div>
          </div>
        </div>
      </footer>
    </>
  )
}
