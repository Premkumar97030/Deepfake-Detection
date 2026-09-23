import { Link } from "react-router-dom";
import {
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  Sparkles,
  Layers,
  Cpu,
  ShieldCheck,
  Zap,
  Activity,
  ChevronRight,
  Lock,
  SearchCheck,
  Eye
} from "lucide-react";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import Hero3DScanner from "../components/Hero3DScanner";
import TiltCard from "../components/TiltCard";

const capabilities = [
  {
    icon: BrainCircuit,
    title: "Spatial Deep Residual Vision",
    desc: "Analyzes high-frequency pixel spectra using a fine-tuned ResNet-50 backbone to expose micro-synthesis GAN and diffusion checkerboard anomalies.",
    tag: "Spatial Domain",
    accent: "cyan"
  },
  {
    icon: Layers,
    title: "Temporal Frame Sequencing",
    desc: "Extracts 16 uniform keyframes across video streams, evaluating inter-frame facial consistency and boundary warping with majority-vote weighting.",
    tag: "Temporal Domain",
    accent: "purple"
  },
  {
    icon: ShieldCheck,
    title: "Tri-Class Forensic Verdict",
    desc: "Provides clear mathematical probability distributions across Authentic Real, AI Generated, and CGI Computer Graphics.",
    tag: "Confidence Engine",
    accent: "emerald"
  }
];

const workflowSteps = [
  {
    number: "01",
    title: "Payload Ingestion",
    desc: "Images and videos are validated and normalized to 224x224 RGB tensors in volatile memory."
  },
  {
    number: "02",
    title: "50-Layer Convolution",
    desc: "Propagates tensors through deep residual blocks extracting 2,048-dimensional forensic feature embeddings."
  },
  {
    number: "03",
    title: "Instant Confidence Report",
    desc: "Softmax activation layers synthesize calibrated probability scores and forensic classification in < 450ms."
  }
];

function Home() {
  return (
    <>
      <Navbar />

      <main className="landing-clean-container">
        {/* Clean Hero Section */}
        <section className="hero-clean">
          <div className="hero-clean-content">
            <div className="clean-badge">
              <span className="clean-pulse" />
              <span>SPECTRA // FORENSIC NEURAL VISION</span>
            </div>

            <h1 className="hero-clean-title">
              Decode Synthetic Media. <br />
              <span className="gradient-spectra">Verify Digital Reality.</span>
            </h1>

            <p className="hero-clean-subtitle">
              Inspect images and video streams for generative AI diffusion traces, GAN artifacts, and facial deepfakes in sub-second latency.
            </p>

            <div className="hero-clean-actions">
              <Link to="/analyze" className="primary-button-3d">
                <Sparkles size={16} />
                <span>Start Media Inspection</span>
                <ArrowRight size={16} />
              </Link>
              <Link to="/about" className="secondary-button-3d">
                <span>View Architecture</span>
              </Link>
            </div>

            <div className="clean-trust-strip">
              <div className="trust-item">
                <span className="trust-dot" />
                <span>Stateless Zero-Retention Privacy</span>
              </div>
              <div className="trust-item">
                <span className="trust-dot" />
                <span>&lt; 450ms Inference Latency</span>
              </div>
              <div className="trust-item">
                <span className="trust-dot" />
                <span>Multi-Class Forensic Accuracy</span>
              </div>
            </div>
          </div>

          <div className="hero-clean-hologram">
            <Hero3DScanner />
          </div>
        </section>

        {/* Clean Capabilities 3D Grid */}
        <section className="clean-section">
          <div className="clean-section-header">
            <span className="clean-eyebrow">
              <Cpu size={14} /> CAPABILITIES
            </span>
            <h2>Precision Engineered for Media Forensics</h2>
            <p>
              Combining deep residual vision with temporal sequence modeling to expose synthetic artifacts invisible to human observation.
            </p>
          </div>

          <div className="clean-cards-grid">
            {capabilities.map(({ icon: Icon, title, desc, tag, accent }, idx) => (
              <TiltCard key={title} maxTilt={7} scale={1.02}>
                <div className={`clean-card accent-${accent}`}>
                  <div className="card-topline">
                    <span className="card-num">0{idx + 1}</span>
                    <span className={`card-tag ${accent}`}>{tag}</span>
                  </div>

                  <div className={`card-icon-box ${accent}`}>
                    <Icon size={24} />
                  </div>

                  <h3>{title}</h3>
                  <p>{desc}</p>

                  <div className="card-footer-link">
                    <Link to="/about">
                      <span>Explore Technical Specs</span>
                      <ChevronRight size={14} />
                    </Link>
                  </div>
                </div>
              </TiltCard>
            ))}
          </div>
        </section>

        {/* Streamlined Workflow / How It Works */}
        <section className="clean-section">
          <div className="clean-section-header">
            <span className="clean-eyebrow">
              <Activity size={14} /> HOW SPECTRA WORKS
            </span>
            <h2>Three-Stage Neural Verification Pipeline</h2>
            <p>From binary payload ingestion to multi-class probabilistic scoring in milliseconds.</p>
          </div>

          <div className="clean-steps-grid">
            {workflowSteps.map((step) => (
              <div className="clean-step-card" key={step.number}>
                <div className="step-header">
                  <span className="step-badge">{step.number}</span>
                  <span className="step-line" />
                </div>
                <h3>{step.title}</h3>
                <p>{step.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Minimalist CTA Banner */}
        <section className="clean-cta-wrap">
          <div className="clean-cta-card">
            <div className="cta-glow-bg" />
            <div className="cta-inner">
              <span className="clean-eyebrow">
                <Sparkles size={14} /> INSTANT MEDIA VERIFICATION
              </span>
              <h2>Ready to inspect digital authenticity?</h2>
              <p>
                Upload any photograph or video stream to receive a complete probability breakdown and forensic confidence report.
              </p>
              <div className="cta-buttons">
                <Link to="/analyze" className="primary-button-3d">
                  <Sparkles size={16} />
                  <span>Launch SPECTRA Scanner</span>
                  <ArrowRight size={16} />
                </Link>
                <Link to="/history" className="secondary-button-3d">
                  <span>View Verification Logs</span>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
}

export default Home;
