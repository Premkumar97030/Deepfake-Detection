import { useRef, useState } from "react";
import { Upload, Image, Video, X } from "lucide-react";

function UploadBox({ mediaType, onFileSelect }) {
  const inputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState("");

  const acceptedTypes =
    mediaType === "image"
      ? ["image/jpeg", "image/png", "image/webp"]
      : ["video/mp4", "video/webm", "video/quicktime"];

  const handleFile = (selectedFile) => {
    setError("");

    if (!selectedFile) {
      return;
    }

    if (!acceptedTypes.includes(selectedFile.type)) {
      setError(
        mediaType === "image"
          ? "Please select a JPG, PNG, or WEBP image."
          : "Please select an MP4, WEBM, or MOV video."
      );
      return;
    }

    // Remove previous preview URL
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    const url = URL.createObjectURL(selectedFile);

    setFile(selectedFile);
    setPreviewUrl(url);

    onFileSelect(selectedFile);
  };

  const handleInputChange = (event) => {
    handleFile(event.target.files[0]);
  };

  const removeFile = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setFile(null);
    setPreviewUrl(null);
    setError("");

    onFileSelect(null);

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <div className="upload-section">

      {!file ? (
        <div
          className="upload-box"
          onClick={() => inputRef.current?.click()}
        >
          <div className="upload-icon">
            {mediaType === "image" ? (
              <Image size={38} />
            ) : (
              <Video size={38} />
            )}
          </div>

          <h3>
            Upload {mediaType === "image" ? "Image" : "Video"}
          </h3>

          <p>
            Drag and drop your file here or click to browse
          </p>

          <button
            type="button"
            className="browse-button"
            onClick={(event) => {
              event.stopPropagation();
              inputRef.current?.click();
            }}
          >
            <Upload size={18} />
            Browse File
          </button>

          <span className="file-info">
            {mediaType === "image"
              ? "JPG, PNG, WEBP"
              : "MP4, WEBM, MOV"}
          </span>
        </div>
      ) : (
        <div className="preview-container">

          <div className="preview-header">
            <div>
              <h3>Selected {mediaType}</h3>
              <p>{file.name}</p>
            </div>

            <button
              type="button"
              className="remove-file"
              onClick={removeFile}
              title="Remove file"
            >
              <X size={22} />
            </button>
          </div>

          <div className="media-preview">

            {mediaType === "image" ? (
              <img
                src={previewUrl}
                alt="Selected media"
              />
            ) : (
              <video
                src={previewUrl}
                controls
                preload="metadata"
              />
            )}

          </div>

          <div className="file-details">
            <span>{file.name}</span>

            <span>
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>

        </div>
      )}

      {error && (
        <p className="upload-error">
          {error}
        </p>
      )}

      <input
        ref={inputRef}
        type="file"
        hidden
        accept={
          mediaType === "image"
            ? "image/jpeg,image/png,image/webp"
            : "video/mp4,video/webm,video/quicktime"
        }
        onChange={handleInputChange}
      />

    </div>
  );
}

export default UploadBox;