import { useLocation, Link } from "react-router-dom";
import { CheckCircle, AlertTriangle, ArrowLeft } from "lucide-react";
import Navbar from "../components/Navbar";

function Result() {
  const location = useLocation();

  const file = location.state?.file;
  const mediaType = location.state?.mediaType || "image";

  // Temporary mock result
  const result = {
    label: "AI",
    confidence: 0.942,
    probabilities: {
      ai: 0.942,
      cgi: 0.038,
      real: 0.020,
    },
    model: "ResNet50",
    processingTime: 1.82,
  };

  const previewUrl = file
    ? URL.createObjectURL(file)
    : null;

  return (
    <>
      <Navbar />

      <main className="result-page">

        <div className="result-header">

          <p className="hero-label">
            ANALYSIS COMPLETE
          </p>

          <h1>Detection Result</h1>

          <p>
            Your media has been analyzed by the
            DeepFake detection system.
          </p>

        </div>

        <section className="result-card">

          {/* Result summary */}

          <div className="result-summary">

            <div className="result-icon">
              <AlertTriangle size={38} />
            </div>

            <div>
              <p className="result-label">
                DETECTION RESULT
              </p>

              <h2>
                {result.label === "AI"
                  ? "AI Generated"
                  : result.label}
              </h2>

              <p className="confidence">
                {(result.confidence * 100).toFixed(1)}%
                confidence
              </p>
            </div>

          </div>

          {/* Media preview */}

          {file && previewUrl && (
            <div className="result-media">

              {mediaType === "image" ? (
                <img
                  src={previewUrl}
                  alt="Analyzed media"
                />
              ) : (
                <video
                  src={previewUrl}
                  controls
                />
              )}

            </div>
          )}

          {!file && (
            <div className="no-media">
              <p>No media was provided.</p>

              <Link to="/analyze">
                Analyze a file
              </Link>
            </div>
          )}

          {/* Probability section */}

          <div className="probability-section">

            <h3>Class Probabilities</h3>

            <div className="probability-item">

              <div className="probability-header">
                <span>AI Generated</span>
                <strong>
                  {(result.probabilities.ai * 100).toFixed(1)}%
                </strong>
              </div>

              <div className="probability-bar">
                <div
                  className="probability-fill ai"
                  style={{
                    width: `${result.probabilities.ai * 100}%`,
                  }}
                />
              </div>

            </div>

            <div className="probability-item">

              <div className="probability-header">
                <span>CGI</span>
                <strong>
                  {(result.probabilities.cgi * 100).toFixed(1)}%
                </strong>
              </div>

              <div className="probability-bar">
                <div
                  className="probability-fill cgi"
                  style={{
                    width: `${result.probabilities.cgi * 100}%`,
                  }}
                />
              </div>

            </div>

            <div className="probability-item">

              <div className="probability-header">
                <span>Real</span>
                <strong>
                  {(result.probabilities.real * 100).toFixed(1)}%
                </strong>
              </div>

              <div className="probability-bar">
                <div
                  className="probability-fill real"
                  style={{
                    width: `${result.probabilities.real * 100}%`,
                  }}
                />
              </div>

            </div>

          </div>

          {/* Model information */}

          <div className="model-info">

            <div>
              <span>Detection Model</span>
              <strong>{result.model}</strong>
            </div>

            <div>
              <span>Processing Time</span>
              <strong>
                {result.processingTime}s
              </strong>
            </div>

            <div>
              <span>Media Type</span>
              <strong>
                {mediaType === "image"
                  ? "Image"
                  : "Video"}
              </strong>
            </div>

          </div>

          {/* Actions */}

          <div className="result-actions">

            <Link
              to="/analyze"
              className="secondary-button"
            >
              <ArrowLeft size={18} />
              Analyze Another
            </Link>

          </div>

        </section>

      </main>
    </>
  );
}

export default Result;