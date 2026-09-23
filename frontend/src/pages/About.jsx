import { useState } from "react";
import { Link } from "react-router-dom";
import {
  BrainCircuit,
  ShieldCheck,
  Cpu,
  Layers,
  Sparkles,
  Lock,
  ArrowRight,
  ChevronDown,
  FileVideo,
  Activity,
  Zap,
  Terminal,
  Server,
  ShieldAlert,
  GitBranch
} from "lucide-react";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import TiltCard from "../components/TiltCard";

const pillars = [
  {
    icon: BrainCircuit,
    title: "50-Layer Deep Residual Vision",
    description:
      "Customized ResNet-50 convolutional neural backbone trained on high-frequency frequency spectra, capturing micro-level diffusion checkerboard distortions and GAN blending boundaries.",
    accent: "cyan"
  },
  {
    icon: FileVideo,
    title: "16-Frame Uniform Temporal Windowing",
    description:
      "Video deepfakes are uniformly sampled across 16 temporal positions. Frame-level anomalies, inter-frame jitter, and facial warping are aggregated via a 70/30 probability-majority vote.",
    accent: "purple"
  },
  {
    icon: Layers,
    title: "Tri-Class Forensic Categorization",
    description:
      "Eliminates ambiguity by isolating authentic camera sensor captures ('Real'), generative diffusion/adversarial syntheses ('AI Generated'), and 3D ray-traced assets ('CGI').",
    accent: "emerald"
  },
  {
    icon: Lock,
    title: "Stateless Zero-Retention Architecture",
    description:
      "All image and video inference occurs in volatile server memory with immediate ephemeral stream purging. No user uploads are ever persisted or retained on cloud storage.",
    accent: "amber"
  }
];

const pipelineSteps = [
  {
    step: "01",
    title: "Spatial & Temporal Ingestion",
    desc: "Media payload is ingested, validated against binary magic bytes, and rescaled to standard 224x224 RGB tensors normalized with ImageNet parameters."
  },
  {
    step: "02",
    title: "Deep Feature Propagation",
    desc: "Tensor flows through 50 convolutional residual blocks, extracting 2,048-dimensional high-level feature vectors across spatial and frequency domains."
  },
  {
    step: "03",
    title: "Multi-Class Probability Mapping",
    desc: "Softmax activation layers calculate exact probabilistic distributions across Real, AI-Generated, and CGI-rendered classes."
  },
  {
    step: "04",
    title: "Weighted Consensus Synthesis",
    desc: "For videos, a weighted consensus model fuses average frame confidence (70%) with majority-vote thresholding (30%) to generate the final verdict."
  }
];

const techSpecs = [
  { label: "Core Model Architecture", value: "Fine-Tuned ResNet-50 Deep CNN" },
  { label: "Temporal Sampling Rate", value: "16 Uniform Keyframes / Stream" },
  { label: "Deep Learning Engine", value: "PyTorch 2.3+ & TorchVision" },
  { label: "Backend API Engine", value: "FastAPI with Asynchronous ASGI Pipeline" },
  { label: "Input Tensor Geometry", value: "224 × 224 px (ImageNet Normalized)" },
  { label: "Inference Latency", value: "< 450ms (Image) / < 2.5s (Video)" },
  { label: "Supported Image Formats", value: "JPG, PNG, WEBP, BMP" },
  { label: "Supported Video Formats", value: "MP4, WEBM, MOV, AVI, MKV" }
];

const faqs = [
  {
    question: "How does the deep learning model detect AI-generated images?",
    answer:
      "Generative models (like Stable Diffusion, Midjourney, and Flux) construct images by denoising latent noise maps. This generative synthesis process leaves subtle, microscopic artifacts in high-frequency pixel transitions, unnatural skin texture smoothing, and lighting inconsistencies. Our fine-tuned ResNet-50 network is specialized to isolate these mathematical anomalies."
  },
  {
    question: "How does video deepfake detection work across frames?",
    answer:
      "Video uploads are sampled across 16 uniform temporal windows. Each keyframe is passed through the neural network to produce a frame probability distribution. The final score is synthesized using a 70% weighted probability score combined with a 30% majority-vote frame consensus, effectively preventing transient compression noise from causing false alarms."
  },
  {
    question: "What is the distinction between AI Generation and CGI Rendering?",
    answer:
      "CGI (Computer-Generated Imagery) refers to 3D geometry rendered using ray tracing, polygon meshes, and programmable shaders (e.g. game engines and 3D modeling software). AI generation creates pixels directly through neural diffusion or adversarial networks. Distinguishing between them provides crucial forensic context when verifying media authenticity."
  },
  {
    question: "Is my uploaded media stored or retained on any servers?",
    answer:
      "No. All media verification operates statelessly in local RAM. Once the neural forward pass completes and probabilities are calculated, temporary memory streams and disk buffers are purged immediately. Your content remains completely private."
  }
];

function About() {
  const [openFaq, setOpenFaq] = useState(0);

  return (
    <>
      <Navbar />

      <main className="about-page-3d">
        {/* Hero */}
        <section className="about-hero-3d">
          <div className="hero-pill-badge">
            <span className="live-pulse" />
            <span>NEURAL FORENSICS DOCUMENTATION</span>
            <Sparkles size={13} className="pill-sparkle" />
          </div>

          <h1>
            Architected for Digital Truth in the Era of <span className="gradient-text-3d">Generative AI.</span>
          </h1>

          <p className="about-hero-sub-3d">
            SPECTRA is an advanced deep learning media forensics framework designed to inspect, deconstruct, and classify synthetic media with high-speed neural precision.
          </p>

          <div className="about-hero-btns">
            <Link to="/analyze" className="primary-button-3d">
              <Sparkles size={16} />
              <span>Launch SPECTRA Scanner</span>
              <ArrowRight size={16} />
            </Link>
            <a href="#pipeline" className="secondary-button-3d">
              View Inspection Pipeline
            </a>
          </div>
        </section>

        {/* 3D Pillars Grid with Tilt Cards */}
        <section className="about-section-3d">
          <div className="section-header-3d">
            <p className="eyebrow-3d">
              <Cpu size={14} /> CORE PILLARS
            </p>
            <h2>Engineered with Deep Neural Foundations</h2>
            <p>
              Combining spatial convolution, temporal aggregation, and tri-class categorization to combat digital misinformation.
            </p>
          </div>

          <div className="pillars-grid-3d">
            {pillars.map(({ icon: Icon, title, description, accent }) => (
              <TiltCard key={title} maxTilt={8} scale={1.02}>
                <div className={`pillar-card-3d accent-${accent}`}>
                  <div className={`pillar-icon-3d ${accent}`}>
                    <Icon size={26} />
                  </div>
                  <h3>{title}</h3>
                  <p>{description}</p>
                </div>
              </TiltCard>
            ))}
          </div>
        </section>

        {/* Pipeline Workflow */}
        <section className="about-section-3d" id="pipeline">
          <div className="section-header-3d">
            <p className="eyebrow-3d">
              <GitBranch size={14} /> INFERENCE PIPELINE
            </p>
            <h2>How Media Flows Through the Neural Engine</h2>
            <p>From binary payload ingestion to calibrated classification verdict in four synchronized stages.</p>
          </div>

          <div className="pipeline-grid-3d">
            {pipelineSteps.map(({ step, title, desc }) => (
              <div className="pipeline-card-3d" key={step}>
                <span className="pipeline-badge-3d">{step}</span>
                <h3>{title}</h3>
                <p>{desc}</p>
                <div className="pipeline-glow-edge" />
              </div>
            ))}
          </div>
        </section>

        {/* Technical Specifications */}
        <section className="about-section-3d">
          <div className="section-header-3d">
            <p className="eyebrow-3d">
              <Server size={14} /> HARDWARE & MODEL SPECS
            </p>
            <h2>System Architecture Specifications</h2>
            <p>Key technical parameters governing neural computation and model inference.</p>
          </div>

          <div className="tech-specs-card-3d">
            <div className="specs-table-3d">
              {techSpecs.map(({ label, value }) => (
                <div className="spec-row-3d" key={label}>
                  <span className="spec-lbl">{label}</span>
                  <strong className="spec-val">{value}</strong>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Interactive FAQ Accordion */}
        <section className="about-section-3d">
          <div className="section-header-3d">
            <p className="eyebrow-3d">
              <Terminal size={14} /> COMMON INQUIRIES
            </p>
            <h2>Frequently Asked Questions</h2>
            <p>Understand the science and mechanics behind synthetic media verification.</p>
          </div>

          <div className="faq-accordion-3d">
            {faqs.map((faq, index) => {
              const isOpen = openFaq === index;
              return (
                <div
                  key={faq.question}
                  className={`faq-item-3d ${isOpen ? "open" : ""}`}
                  onClick={() => setOpenFaq(isOpen ? -1 : index)}
                >
                  <button className="faq-question-3d" aria-expanded={isOpen}>
                    <span>{faq.question}</span>
                    <ChevronDown
                      size={18}
                      className={`faq-arrow-3d ${isOpen ? "rotated" : ""}`}
                    />
                  </button>
                  {isOpen && (
                    <div className="faq-answer-3d">
                      <p>{faq.answer}</p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Bottom CTA Banner */}
        <section className="interactive-showcase-3d">
          <div className="showcase-card-3d">
            <div className="showcase-glow" />
            <div className="showcase-content">
              <span className="eyebrow-3d">
                <Activity size={14} /> READY TO DETECT
              </span>
              <h2>Start analyzing media files today.</h2>
              <p>
                Experience fast, reliable, multi-class verification with forensic probability reports.
              </p>
              <div className="showcase-actions">
                <Link to="/analyze" className="primary-button-3d">
                  <Sparkles size={16} />
                  <span>Launch DeepFake Analyzer</span>
                  <ArrowRight size={16} />
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

export default About;