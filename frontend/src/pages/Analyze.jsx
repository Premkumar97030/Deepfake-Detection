import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Image, Video, ShieldCheck } from "lucide-react";

import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";

function Analyze() {
  const navigate = useNavigate();

  const [mediaType, setMediaType] = useState("image");
  const [file, setFile] = useState(null);

  const handleAnalyze = () => {
    if (!file) return;

    navigate("/result", {
      state: {
        file,
        mediaType,
      },
    });
  };

  return (
    <>
      <Navbar />

      <main className="analyze-page">

        <section className="analyze-header">

          <p className="hero-label">
            DEEPFAKE DETECTION
          </p>

          <h1>Analyze Your Media</h1>

          <p>
            Upload an image or video to detect
            AI-generated and manipulated content.
          </p>

        </section>

        <section className="media-selector">

          <button
            className={
              mediaType === "image"
                ? "media-option active"
                : "media-option"
            }
            onClick={() => {
              setMediaType("image");
              setFile(null);
            }}
          >
            <Image size={24} />
            <span>Image</span>
          </button>

          <button
            className={
              mediaType === "video"
                ? "media-option active"
                : "media-option"
            }
            onClick={() => {
              setMediaType("video");
              setFile(null);
            }}
          >
            <Video size={24} />
            <span>Video</span>
          </button>

        </section>

        <section className="analyze-card">

          <UploadBox
            mediaType={mediaType}
            onFileSelect={setFile}
          />

          <div className="analyze-info">
            <ShieldCheck size={20} />

            <span>
              Your media will be analyzed using
              deep learning models.
            </span>
          </div>

          <button
            className="analyze-button"
            disabled={!file}
            onClick={handleAnalyze}
          >
            Analyze {mediaType === "image" ? "Image" : "Video"}
          </button>

        </section>

      </main>
    </>
  );
}

export default Analyze;