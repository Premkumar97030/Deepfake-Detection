import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Image as ImageIcon, Video as VideoIcon, ShieldCheck, Sparkles, Cpu, AlertCircle, Loader2 } from "lucide-react";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import UploadBox from "../components/UploadBox";
import { saveAnalysisRecord } from "../utils/historyStorage";

function Analyze() {
  const navigate = useNavigate();

  const [mediaType, setMediaType] = useState("image");
  const [file, setFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!file) return;

    setIsAnalyzing(true);
    setError("");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}/api/analyze`,
        { method: "POST", body: formData }
      );
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Analysis could not be completed.");

      // Save record to local history with thumbnail
      await saveAnalysisRecord({
        file,
        mediaType,
        result: data
      });

      navigate("/result", { state: { file, mediaType, result: data } });
    } catch (requestError) {
      setError(requestError.message || "Could not connect to the detection service.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <>
      <Navbar />

      <main className="analyze-page-3d">
        {/* Header */}
        <section className="analyze-header-3d">
          <div className="hero-pill-badge">
            <span className="live-pulse" />
            <span>NEURAL MEDIA VERIFIER</span>
            <Sparkles size={13} className="pill-sparkle" />
          </div>

          <h1>Analyze Media Authenticity</h1>

          <p>
            Upload any digital image or video stream to detect AI-generated artifacts, deepfake face-swaps, and CGI rendering patterns.
          </p>
        </section>

        {/* 3D Mode Selector Switcher */}
        <section className="media-selector-3d">
          <button
            className={`media-option-3d ${mediaType === "image" ? "active" : ""}`}
            onClick={() => {
              setMediaType("image");
              setFile(null);
              setError("");
            }}
          >
            <ImageIcon size={20} />
            <span>Image Analysis</span>
            {mediaType === "image" && <div className="active-glow-dot" />}
          </button>

          <button
            className={`media-option-3d ${mediaType === "video" ? "active" : ""}`}
            onClick={() => {
              setMediaType("video");
              setFile(null);
              setError("");
            }}
          >
            <VideoIcon size={20} />
            <span>Video Temporal Scan</span>
            {mediaType === "video" && <div className="active-glow-dot" />}
          </button>
        </section>

        {/* 3D Glassmorphic Analyzer Card */}
        <section className="analyze-card-3d">
          <UploadBox
            key={mediaType}
            mediaType={mediaType}
            onFileSelect={setFile}
          />

          <div className="analyze-features-row">
            <div className="analyze-feature-item">
              <ShieldCheck size={18} className="feat-icon emerald" />
              <span>ResNet-50 50-Layer Deep Convolution</span>
            </div>
            <div className="analyze-feature-item">
              <Cpu size={18} className="feat-icon cyan" />
              <span>{mediaType === "video" ? "16-Keyframe Uniform Sampling" : "Pixel Artifact Spectrum Extraction"}</span>
            </div>
          </div>

          {/* Action Button / Loading State */}
          <button
            className={`analyze-submit-button-3d ${isAnalyzing ? "loading" : ""}`}
            disabled={!file || isAnalyzing}
            onClick={handleAnalyze}
          >
            {isAnalyzing ? (
              <>
                <Loader2 size={20} className="spinning-loader" />
                <span>Running Deep Neural Inference...</span>
              </>
            ) : (
              <>
                <Sparkles size={18} />
                <span>Execute {mediaType === "image" ? "Image" : "Video"} Analysis</span>
              </>
            )}
          </button>

          {error && (
            <div className="analysis-error-card">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}
        </section>
      </main>

      <Footer />
    </>
  );
}

export default Analyze;
