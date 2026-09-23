import { Link, NavLink } from "react-router-dom";
import { Sparkles, Activity, Layers, Shield } from "lucide-react";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-container">
        <Link to="/" className="logo">
          <div className="logo-mark">
            <span className="spectra-prism-icon">◆</span>
            <div className="logo-glow" />
          </div>
          <span className="logo-text">
            SPEC<span className="logo-accent">TRA</span>
          </span>
          <span className="badge-ai-version">NEURAL FORENSICS</span>
        </Link>

        <nav className="nav-links" aria-label="Main navigation">
          <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : "")}>
            <span>Home</span>
          </NavLink>
          <NavLink to="/analyze" className={({ isActive }) => (isActive ? "active" : "")}>
            <span>Analyzer</span>
          </NavLink>
          <NavLink to="/history" className={({ isActive }) => (isActive ? "active" : "")}>
            <span>History</span>
          </NavLink>
          <NavLink to="/about" className={({ isActive }) => (isActive ? "active" : "")}>
            <span>Technology</span>
          </NavLink>
        </nav>

        <div className="nav-actions">
          <Link to="/analyze" className="nav-button">
            <Sparkles size={14} />
            <span>Launch Scanner</span>
          </Link>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
