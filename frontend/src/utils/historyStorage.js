const STORAGE_KEY = "dfp_analysis_history";

/**
 * Creates a lightweight base64 thumbnail string (< 60 KB) for persistent storage.
 */
export async function createThumbnail(file, mediaType = "image") {
  if (!file) return null;

  return new Promise((resolve) => {
    try {
      if (mediaType === "image") {
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = new Image();
          img.onload = () => {
            const canvas = document.createElement("canvas");
            const maxDim = 320;
            let { width, height } = img;

            if (width > height) {
              if (width > maxDim) {
                height = Math.round((height * maxDim) / width);
                width = maxDim;
              }
            } else {
              if (height > maxDim) {
                width = Math.round((width * maxDim) / height);
                height = maxDim;
              }
            }

            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);
            resolve(canvas.toDataURL("image/jpeg", 0.78));
          };
          img.onerror = () => resolve(null);
          img.src = e.target.result;
        };
        reader.onerror = () => resolve(null);
        reader.readAsDataURL(file);
      } else {
        // For video, extract first frame via video element
        const video = document.createElement("video");
        video.preload = "metadata";
        video.muted = true;
        video.playsInline = true;
        const objectUrl = URL.createObjectURL(file);
        video.src = objectUrl;

        video.onloadeddata = () => {
          video.currentTime = 0.5;
        };

        video.onseeked = () => {
          const canvas = document.createElement("canvas");
          const maxDim = 320;
          let width = video.videoWidth || 320;
          let height = video.videoHeight || 240;

          if (width > height) {
            if (width > maxDim) {
              height = Math.round((height * maxDim) / width);
              width = maxDim;
            }
          } else {
            if (height > maxDim) {
              width = Math.round((width * maxDim) / height);
              height = maxDim;
            }
          }

          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext("2d");
          ctx.drawImage(video, 0, 0, width, height);
          URL.revokeObjectURL(objectUrl);
          resolve(canvas.toDataURL("image/jpeg", 0.75));
        };

        video.onerror = () => {
          URL.revokeObjectURL(objectUrl);
          resolve(null);
        };
      }
    } catch {
      resolve(null);
    }
  });
}

export function getAnalysisHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (err) {
    console.error("Failed to read analysis history:", err);
    return [];
  }
}

export async function saveAnalysisRecord({ file, mediaType, result, thumbnail }) {
  try {
    const history = getAnalysisHistory();
    
    // If thumbnail wasn't pre-generated, create it now
    let thumbData = thumbnail;
    if (!thumbData && file) {
      thumbData = await createThumbnail(file, mediaType);
    }

    const newRecord = {
      id: "analysis_" + Date.now() + "_" + Math.random().toString(36).substring(2, 7),
      filename: result.filename || file?.name || "Uploaded File",
      fileSize: file?.size || null,
      timestamp: new Date().toISOString(),
      mediaType: mediaType || result.media_type || "image",
      prediction: result.prediction,
      displayLabel: result.display_label || result.prediction,
      confidence: result.confidence,
      probabilities: result.probabilities || {},
      model: result.model || "Fine-tuned ResNet50",
      processingTimeMs: result.processing_time_ms || 0,
      sampledFrames: result.sampled_frames || null,
      videoDurationSeconds: result.video_duration_seconds || null,
      frameSummary: result.frame_summary || null,
      thumbnail: thumbData || null
    };

    // Keep up to 60 most recent records
    const updated = [newRecord, ...history.filter(item => item.id !== newRecord.id)].slice(0, 60);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    return newRecord;
  } catch (err) {
    console.error("Failed to save analysis record:", err);
    return null;
  }
}

export function deleteAnalysisRecord(id) {
  try {
    const history = getAnalysisHistory();
    const filtered = history.filter(item => item.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
    return filtered;
  } catch (err) {
    console.error("Failed to delete analysis record:", err);
    return [];
  }
}

export function clearAnalysisHistory() {
  try {
    localStorage.removeItem(STORAGE_KEY);
    return [];
  } catch (err) {
    console.error("Failed to clear analysis history:", err);
    return [];
  }
}

