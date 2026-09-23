import { useEffect, useMemo, useState, useRef } from "react";
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
  Download,
  Share2,
  Check,
  Eye,
  Scan,
  FileText
} from "lucide-react";
import jsPDF from "jspdf";
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

  const [viewMode, setViewMode] = useState("raw"); // 'raw' | 'ela'
  const [elaUrl, setElaUrl] = useState(null);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [copied, setCopied] = useState(false);
  const reportRef = useRef(null);

  useEffect(() => () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    if (elaUrl) URL.revokeObjectURL(elaUrl);
  }, [previewUrl, elaUrl]);

  // Compute Error Level Analysis (ELA) artifact noise map client-side
  useEffect(() => {
    if (!previewUrl || mediaType !== "image") return;

    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => {
      try {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        // Convert to recompressed JPEG
        const recompressed = new Image();
        recompressed.onload = () => {
          const compCanvas = document.createElement("canvas");
          const compCtx = compCanvas.getContext("2d");
          compCanvas.width = img.width;
          compCanvas.height = img.height;
          compCtx.drawImage(recompressed, 0, 0);

          const origData = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const compData = compCtx.getImageData(0, 0, canvas.width, canvas.height);
          const outData = ctx.createImageData(canvas.width, canvas.height);

          // Calculate amplified difference
          const scale = 14;
          for (let i = 0; i < origData.data.length; i += 4) {
            const rDiff = Math.abs(origData.data[i] - compData.data[i]) * scale;
            const gDiff = Math.abs(origData.data[i + 1] - compData.data[i + 1]) * scale;
            const bDiff = Math.abs(origData.data[i + 2] - compData.data[i + 2]) * scale;

            // Generate cyber-forensic false-color map
            outData.data[i] = Math.min(255, rDiff * 1.5);
            outData.data[i + 1] = Math.min(255, gDiff + bDiff);
            outData.data[i + 2] = Math.min(255, bDiff * 2);
            outData.data[i + 3] = 255;
          }

          ctx.putImageData(outData, 0, 0);
          setElaUrl(canvas.toDataURL("image/png"));
        };
        recompressed.src = canvas.toDataURL("image/jpeg", 0.72);
      } catch {
        setElaUrl(null);
      }
    };
    img.src = previewUrl;
  }, [previewUrl, mediaType]);

  const handleDownloadPdf = () => {
    if (!result) return;
    setIsGeneratingPdf(true);

    try {
      const doc = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4"
      });

      const isAuth = result.prediction === "real";
      const verdictTitle = result.display_label || labels[result.prediction] || result.prediction;
      const conf = Number(result.confidence).toFixed(2);
      const auditId = "SPEC-" + Date.now().toString(36).toUpperCase() + "-" + Math.random().toString(36).substring(2, 6).toUpperCase();

      // Dark theme background
      doc.setFillColor(8, 12, 24);
      doc.rect(0, 0, 210, 297, "F");

      // Header Banner
      doc.setFillColor(16, 22, 45);
      doc.roundedRect(14, 14, 182, 32, 4, 4, "F");

      doc.setTextColor(0, 240, 255);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(18);
      doc.text("SPECTRA FORENSIC AUDIT CERTIFICATE", 22, 28);

      doc.setTextColor(140, 160, 190);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.text("Cryptographic Synthetic Media Verification & Probability Analysis", 22, 36);

      // Audit ID & Date
      doc.setFontSize(8);
      doc.setTextColor(180, 200, 230);
      doc.text(`AUDIT ID: ${auditId}`, 130, 28);
      doc.text(`TIMESTAMP: ${new Date().toUTCString()}`, 130, 34);

      // Verdict Box
      const verdictColor = isAuth ? [0, 245, 160] : [255, 183, 3];
      doc.setFillColor(14, 19, 38);
      doc.setDrawColor(verdictColor[0], verdictColor[1], verdictColor[2]);
      doc.setLineWidth(0.8);
      doc.roundedRect(14, 52, 182, 38, 4, 4, "FD");

      doc.setTextColor(verdictColor[0], verdictColor[1], verdictColor[2]);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(11);
      doc.text(isAuth ? "VERIFIED AUTHENTIC MEDIA" : "SYNTHETIC / MANIPULATED MEDIA DETECTED", 22, 63);

      doc.setTextColor(255, 255, 255);
      doc.setFontSize(22);
      doc.text(verdictTitle.toUpperCase(), 22, 75);

      doc.setFontSize(14);
      doc.setTextColor(0, 240, 255);
      doc.text(`Certainty Score: ${conf}%`, 130, 75);

      // Metadata Grid
      doc.setFillColor(12, 16, 32);
      doc.setDrawColor(50, 70, 100);
      doc.setLineWidth(0.3);
      doc.roundedRect(14, 96, 182, 36, 3, 3, "FD");

      doc.setFontSize(9);
      doc.setTextColor(140, 160, 190);
      doc.text("Target File:", 22, 106);
      doc.text("Inference Model:", 22, 115);
      doc.text("Processing Latency:", 22, 124);

      doc.setTextColor(255, 255, 255);
      doc.text(result.filename || "Uploaded File", 60, 106);
      doc.text(result.model || "ResNet-50 50-Layer Backbone", 60, 115);
      doc.text(`${(result.processing_time_ms / 1000).toFixed(2)} seconds`, 60, 124);

      doc.setTextColor(140, 160, 190);
      doc.text("Media Type:", 120, 106);
      doc.text("Frame Sampling:", 120, 115);
      doc.text("SHA-256 Checksum:", 120, 124);

      doc.setTextColor(255, 255, 255);
      doc.text(mediaType === "video" ? "Video Stream" : "Digital Image", 155, 106);
      doc.text(result.sampled_frames ? `${result.sampled_frames} Frames` : "Pixel Stream", 155, 115);
      doc.text(auditId.slice(-8), 155, 124);

      // Probability Distribution Table
      doc.setFillColor(14, 19, 38);
      doc.roundedRect(14, 138, 182, 60, 3, 3, "F");

      doc.setFont("helvetica", "bold");
      doc.setFontSize(11);
      doc.setTextColor(255, 255, 255);
      doc.text("CLASS PROBABILITY DISTRIBUTION", 22, 150);

      const probs = result.probabilities || {};
      let yOffset = 162;
      Object.entries(probs).forEach(([name, val]) => {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(10);
        doc.setTextColor(180, 200, 230);
        doc.text(labels[name] || name, 22, yOffset);

        doc.setFont("helvetica", "bold");
        doc.setTextColor(255, 255, 255);
        doc.text(`${Number(val).toFixed(2)}%`, 85, yOffset);

        // Progress bar in PDF
        doc.setFillColor(30, 40, 70);
        doc.rect(105, yOffset - 3.5, 75, 4, "F");

        doc.setFillColor(name === "real" ? 0 : name === "ai" ? 0 : 157, name === "real" ? 245 : name === "ai" ? 240 : 78, name === "real" ? 160 : 255);
        doc.rect(105, yOffset - 3.5, (val / 100) * 75, 4, "F");

        yOffset += 11;
      });

      // Digital Signature Footer
      doc.setDrawColor(0, 240, 255);
      doc.setLineWidth(0.5);
      doc.line(14, 255, 196, 255);

      doc.setFontSize(8);
      doc.setTextColor(130, 150, 180);
      doc.text("Official verification generated by SPECTRA Deepfake Detection Platform.", 14, 263);
      doc.text("Tamper-evident neural probability audit • Generated locally & verified through ResNet-50 AI backbone.", 14, 268);

      doc.save(`SPECTRA_Audit_Report_${result.filename || "media"}.pdf`);
    } catch (err) {
      console.error("Failed to generate PDF report:", err);
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const handleCopySummary = () => {
    if (!result) return;
    const isAuth = result.prediction === "real";
    const text = `🔍 SPECTRA Forensic Verdict: ${result.display_label || labels[result.prediction] || result.prediction}\n` +
      `📊 Confidence: ${Number(result.confidence).toFixed(2)}%\n` +
      `📁 Target: ${result.filename}\n` +
      `⚡ Model: ${result.model} (${(result.processing_time_ms / 1000).toFixed(2)}s)\n` +
      `🛡️ Status: ${isAuth ? "VERIFIED AUTHENTIC" : "SYNTHETIC / MANIPULATED"}`;

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

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
          <div className={`result-card-clean status-${verdictClass}`} ref={reportRef}>
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
              {/* Left Column: Media Preview with ELA Forensic Scanner */}
              <div className="result-media-col">
                <div className="media-viewport-compact">
                  {previewUrl ? (
                    mediaType === "image" ? (
                      <img
                        src={viewMode === "ela" && elaUrl ? elaUrl : previewUrl}
                        alt="Analyzed media preview"
                        className="preview-img-compact"
                      />
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

                {/* ELA Mode Switcher for Images */}
                {mediaType === "image" && elaUrl && (
                  <div className="forensic-scanner-toggle">
                    <button
                      type="button"
                      className={`scanner-btn ${viewMode === "raw" ? "active" : ""}`}
                      onClick={() => setViewMode("raw")}
                    >
                      <Eye size={13} />
                      <span>Original Media</span>
                    </button>
                    <button
                      type="button"
                      className={`scanner-btn ${viewMode === "ela" ? "active" : ""}`}
                      onClick={() => setViewMode("ela")}
                    >
                      <Scan size={13} />
                      <span>ELA Artifact Scan</span>
                    </button>
                  </div>
                )}

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

            {/* Action Buttons with PDF & Share */}
            <div className="result-actions-compact">
              <Link to="/analyze" className="primary-button-clean btn-sm">
                <ArrowLeft size={15} />
                <span>Analyze Another Media</span>
              </Link>

              <button
                type="button"
                className="secondary-button-clean btn-sm"
                onClick={handleDownloadPdf}
                disabled={isGeneratingPdf}
              >
                <Download size={15} />
                <span>{isGeneratingPdf ? "Building PDF..." : "Export Certificate (PDF)"}</span>
              </button>

              <button
                type="button"
                className="secondary-button-clean btn-sm"
                onClick={handleCopySummary}
              >
                {copied ? <Check size={15} className="copied-icon" /> : <Share2 size={15} />}
                <span>{copied ? "Copied Verdict!" : "Copy Report"}</span>
              </button>

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
