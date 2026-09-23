import { useRef, useState } from "react";
import { Upload, Image as ImageIcon, Video as VideoIcon, X, CheckCircle2 } from "lucide-react";

function UploadBox({ mediaType, onFileSelect }) {
  const inputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState("");

  const handleFile = (selectedFile) => {
    setError("");

    if (!selectedFile) return;

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

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
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
          className={`upload-box-clean ${isDragging ? "dragging" : ""}`}
          onClick={() => inputRef.current?.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="upload-icon-clean">
            {mediaType === "image" ? (
              <ImageIcon size={38} />
            ) : (
              <VideoIcon size={38} />
            )}
          </div>

          <h3 className="upload-title">
            Upload {mediaType === "image" ? "Any Image Format" : "Any Video Format"}
          </h3>

          <p className="upload-subtext">
            Drag and drop your file here, or click to browse. All {mediaType === "image" ? "image" : "video"} formats are supported.
          </p>

          <button
            type="button"
            className="browse-button-clean"
            onClick={(e) => {
              e.stopPropagation();
              inputRef.current?.click();
            }}
          >
            <Upload size={16} />
            <span>Choose File</span>
          </button>

          <div className="format-pills">
            {mediaType === "image" ? (
              <>
                <span className="pill">JPG</span>
                <span className="pill">PNG</span>
                <span className="pill">WEBP</span>
                <span className="pill">BMP</span>
                <span className="pill">TIFF</span>
                <span className="pill">AVIF</span>
                <span className="pill">HEIC</span>
                <span className="pill">ALL</span>
              </>
            ) : (
              <>
                <span className="pill">MP4</span>
                <span className="pill">WEBM</span>
                <span className="pill">MOV</span>
                <span className="pill">AVI</span>
                <span className="pill">MKV</span>
                <span className="pill">WMV</span>
                <span className="pill">FLV</span>
                <span className="pill">ALL</span>
              </>
            )}
          </div>
        </div>
      ) : (
        <div className="preview-container-clean">
          <div className="preview-header-clean">
            <div className="preview-title-group">
              <span className="preview-badge-clean">
                <CheckCircle2 size={13} /> READY FOR ANALYSIS
              </span>
              <h3>{file.name}</h3>
            </div>

            <button
              type="button"
              className="remove-file-clean"
              onClick={removeFile}
              title="Remove file"
            >
              <X size={18} />
            </button>
          </div>

          <div className="media-preview-clean">
            {mediaType === "image" ? (
              <img src={previewUrl} alt="Selected media preview" />
            ) : (
              <video src={previewUrl} controls preload="metadata" />
            )}
          </div>

          <div className="file-details-clean">
            <div className="file-detail-item">
              <span>File Name</span>
              <strong>{file.name}</strong>
            </div>
            <div className="file-detail-item">
              <span>File Size</span>
              <strong>{(file.size / (1024 * 1024)).toFixed(2)} MB</strong>
            </div>
            <div className="file-detail-item">
              <span>MIME Type</span>
              <strong>{file.type || "Auto-detected"}</strong>
            </div>
          </div>
        </div>
      )}

      {error && <p className="upload-error">{error}</p>}

      <input
        ref={inputRef}
        type="file"
        hidden
        accept={mediaType === "image" ? "image/*, .jpg, .jpeg, .png, .webp, .bmp, .tiff, .tif, .gif, .svg, .heic, .heif, .avif, .ico" : "video/*, .mp4, .webm, .mov, .avi, .mkv, .flv, .wmv, .m4v, .3gp, .ts, .mts, .mpg, .mpeg"}
        onChange={handleInputChange}
      />
    </div>
  );
}

export default UploadBox;