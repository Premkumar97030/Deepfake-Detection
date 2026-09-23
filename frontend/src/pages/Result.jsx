import { useEffect, useMemo } from "react";
import { useLocation, Link } from "react-router-dom";
import {
  AlertTriangle,
  ArrowLeft,
  CheckCircle2,
  Clock,
  Cpu,
  Layers,
  ShieldCheck,
  ShieldAlert,
  Sparkles,
  FileVideo,
  Image as ImageIcon,
  Activity,
  History as HistoryIcon,
  RefreshCw
} from "lucide-react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const labels = {
  ai: "AI Generated",
  cgi: "CGI Render",
  real: "Authentic Real",
  fake: "Manipulated / Fake"
};

function Result() {
  const location = useLocation();
  const { file, mediaType = "image", result } = location.state || {};
  const previewUrl = useMemo(() => (file ? URL.createObjectURL(file) : null), [file]);

  useEffect(() => () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  if (!result) {
    return (
      <>
        <Navbar />
        <main className="result-page-clean">
          <section className="no-result-clean">
            <AlertTriangle size={44} className="warn-icon-clean" />
            <h2>No Active Analysis Found</h2>
            <p>Please upload an image or video file to run a detection analysis.</p>
            <Link to="/analyze" className="primary-button-clean">
              <Sparkles size={16} />
              <span>Analyze Media Now</span>
            </Link>
          </section>
        </main>
        <Footer />
      </>
    );
  }

  const isReal = result.prediction === "real";
  const isAi = result.prediction === "ai";
  const isCgi = result.prediction === "cgi";
  const probabilityEntries = Object.entries(result.probabilities || {});

  const verdictClass = isReal ? "real" : isAi ? "ai" : isCgi ? "cgi" : "fake";

  return (
    <>
      <Navbar />

      <main className="result-page-clean">
        <div className="result-header-clean">
          <div className="clean-badge">
            <span className="clean-pulse" />
            <span>SPECTRA FORENSIC REPORT</span>
          </div>
          <h1>Detection Verdict</h1>
          <p>
            Forensic classification and probability analysis for <strong>{result.filename}</strong>.
          </p>
        </div>

        <div className="result-container-clean">
          <div className={`result-card-clean status-${verdictClass}`}>
            {/* Top Verdict Banner */}
            <div className="verdict-banner-clean">
              <div className={`verdict-badge-icon ${verdictClass}`}>
                {isReal ? <ShieldCheck size={28} /> : <ShieldAlert size={28} />}
              </div>

              <div className="verdict-info-clean">
                <div className="verdict-meta-row">
                  <span className="verdict-tag">CLASSIFICATION VERDICT</span>
                  <div className={`status-tag-pill ${verdictClass}`}>
                    {isReal ? "VERIFIED AUTHENTIC" : "SYNTHETIC / MANIPULATED"}
                  </div>
                </div>
                <h2 className="verdict-name">
                  {result.display_label || labels[result.prediction] || result.prediction}
                </h2>
              </div>

              <div className="confidence-pill-clean">
                <span className="conf-label">Confidence</span>
                <strong className="conf-value">{Number(result.confidence).toFixed(1)}%</strong>
              </div>
            </div>

            {/* Compact 2-Column Grid */}
            <div className="result-grid-clean">
              {/* Left Column: Media Preview */}
              <div className="result-media-col">
                <div className="media-viewport-compact">
                  {previewUrl ? (
                    mediaType === "image" ? (
                      <img src={previewUrl} alt="Analyzed media preview" className="preview-img-compact" />
                    ) : (
                      <video src={previewUrl} controls className="preview-vid-compact" />
                    )
                  ) : (
                    <div className="no-preview-placeholder">
                      <ImageIcon size={32} />
                      <span>No Media Preview</span>
                    </div>
                  )}
                </div>

                {result.frame_summary && (
                  <div className="video-summary-compact">
                    <Activity size={14} />
                    <span>
                      <strong>{result.frame_summary.fake_frames}</strong> fake / <strong>{result.frame_summary.real_frames}</strong> real frames
                    </span>
                  </div>
                )}
              </div>

              {/* Right Column: Probabilities & Metrics */}
              <div className="result-data-col">
                {/* Probability Distribution */}
                <div className="probabilities-compact">
                  <div className="prob-section-title">
                    <Layers size={14} />
                    <span>Probability Distribution</span>
                  </div>

                  <div className="prob-rows-compact">
                    {probabilityEntries.map(([name, value]) => {
                      const barClass = name === "real" ? "real" : name === "ai" ? "ai" : name === "cgi" ? "cgi" : "fake";
                      return (
                        <div className="prob-row-compact" key={name}>
                          <div className="prob-header-compact">
                            <span className="class-title">{labels[name] || name}</span>
                            <strong className="class-score">{Number(value).toFixed(1)}%</strong>
                          </div>
                          <div className="prob-track-compact">
                            <div
                              className={`prob-fill-compact ${barClass}`}
                              style={{ width: `${value}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Metrics Info Row */}
                <div className="metrics-row-compact">
                  <div className="metric-chip">
                    <Cpu size={14} className="chip-icon" />
                    <div className="chip-text">
                      <span className="chip-label">Model</span>
                      <span className="chip-val">{result.model || "ResNet-50"}</span>
                    </div>
                  </div>

                  <div className="metric-chip">
                    <Clock size={14} className="chip-icon" />
                    <div className="chip-text">
                      <span className="chip-label">Speed</span>
                      <span className="chip-val">{(result.processing_time_ms / 1000).toFixed(2)}s</span>
                    </div>
                  </div>

                  <div className="metric-chip">
                    {mediaType === "video" ? <FileVideo size={14} className="chip-icon" /> : <ImageIcon size={14} className="chip-icon" />}
                    <div className="chip-text">
                      <span className="chip-label">Format</span>
                      <span className="chip-val">{mediaType === "video" ? `${result.sampled_frames} Frms` : "Image"}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="result-actions-compact">
              <Link to="/analyze" className="primary-button-clean btn-sm">
                <ArrowLeft size={15} />
                <span>Analyze Another Media</span>
              </Link>
              <Link to="/history" className="secondary-button-clean btn-sm">
                <HistoryIcon size={15} />
                <span>Audit History</span>
              </Link>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
}

export default Result;
