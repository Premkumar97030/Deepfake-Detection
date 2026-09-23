import { Link } from "react-router-dom";
import { Sparkles, Shield, Activity } from "lucide-react";

function Footer() {
  return (
    <footer className="footer-3d">
      <div className="footer-container-3d">
        <div className="footer-brand-group">
          <Link to="/" className="footer-logo">
            <div className="footer-logo-mark">
              <span className="spectra-prism-icon-sm">◆</span>
            </div>
            <span>SPEC<span className="accent-color">TRA</span></span>
          </Link>
          <p className="footer-tagline">
            Next-generation neural forensics platform engineered for synthetic media detection and spatial-temporal authenticity verification.
          </p>
          <div className="system-status-indicator">
            <span className="status-pulse-dot" />
            <span>SPECTRA Neural Inference Cluster // Operational</span>
          </div>
        </div>

        <div className="footer-links-column">
          <h4>Platform</h4>
          <Link to="/">Overview</Link>
          <Link to="/analyze">Media Scanner</Link>
          <Link to="/history">Audit Logs</Link>
          <Link to="/about">Architecture</Link>
        </div>

        <div className="footer-links-column">
          <h4>Models & Engine</h4>
          <span className="footer-info-text">ResNet-50 Fine-Tuned CNN</span>
          <span className="footer-info-text">16-Frame Temporal Sampler</span>
          <span className="footer-info-text">Tri-Class Softmax Engine</span>
        </div>
      </div>

      <div className="footer-bottom-bar">
        <p>© {new Date().getFullYear()} SPECTRA AI Media Forensics. All rights reserved.</p>
        <p className="footer-engine-tag">PyTorch • FastAPI • WebGL 3D • React 19</p>
      </div>
    </footer>
  );
}

export default Footer;
