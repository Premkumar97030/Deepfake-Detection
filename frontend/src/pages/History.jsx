import { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  Clock,
  Trash2,
  Search,
  Filter,
  Image as ImageIcon,
  Video as VideoIcon,
  ShieldCheck,
  ShieldAlert,
  Sparkles,
  ArrowRight,
  BarChart3,
  CheckCircle2,
  AlertTriangle,
  Layers,
  X,
  ExternalLink,
  Cpu,
  Activity
} from "lucide-react";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import TiltCard from "../components/TiltCard";
import {
  getAnalysisHistory,
  deleteAnalysisRecord,
  clearAnalysisHistory
} from "../utils/historyStorage";

const labelMap = {
  ai: "AI Generated",
  cgi: "CGI Render",
  real: "Authentic Real",
  fake: "Manipulated / Fake"
};

function History() {
  const [records, setRecords] = useState([]);
  const [search, setSearch] = useState("");
  const [mediaFilter, setMediaFilter] = useState("all");
  const [resultFilter, setResultFilter] = useState("all");
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [showClearConfirm, setShowClearConfirm] = useState(false);

  useEffect(() => {
    setRecords(getAnalysisHistory());
  }, []);

  const handleDelete = (id, e) => {
    e.stopPropagation();
    const updated = deleteAnalysisRecord(id);
    setRecords(updated);
    if (selectedRecord?.id === id) {
      setSelectedRecord(null);
    }
  };

  const handleClearAll = () => {
    clearAnalysisHistory();
    setRecords([]);
    setSelectedRecord(null);
    setShowClearConfirm(false);
  };

  const stats = useMemo(() => {
    if (!records.length) return { total: 0, real: 0, fake: 0, avgConf: 0 };
    const total = records.length;
    const real = records.filter(r => r.prediction === "real").length;
    const fake = total - real;
    const avgConf = (records.reduce((sum, r) => sum + (Number(r.confidence) || 0), 0) / total).toFixed(1);
    return {
      total,
      real,
      fake,
      realPct: Math.round((real / total) * 100),
      fakePct: Math.round((fake / total) * 100),
      avgConf
    };
  }, [records]);

  const filteredRecords = useMemo(() => {
    return records.filter(record => {
      const matchesSearch =
        search.trim() === "" ||
        record.filename.toLowerCase().includes(search.toLowerCase()) ||
        (record.displayLabel || record.prediction || "").toLowerCase().includes(search.toLowerCase());

      const matchesMedia =
        mediaFilter === "all" || record.mediaType === mediaFilter;

      const matchesResult =
        resultFilter === "all" ||
        (resultFilter === "real" && record.prediction === "real") ||
        (resultFilter === "fake" && record.prediction !== "real") ||
        (resultFilter === "ai" && record.prediction === "ai") ||
        (resultFilter === "cgi" && record.prediction === "cgi");

      return matchesSearch && matchesMedia && matchesResult;
    });
  }, [records, search, mediaFilter, resultFilter]);

  const formatDate = (isoStr) => {
    try {
      const date = new Date(isoStr);
      return date.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      });
    } catch {
      return isoStr;
    }
  };

  return (
    <>
      <Navbar />

      <main className="history-page-3d">
        {/* Header */}
        <section className="history-header-3d">
          <div className="hero-pill-badge">
            <span className="live-pulse" />
            <span>SESSION AUDIT TRAIL</span>
          </div>
          <h1>Detection Log & History</h1>
          <p>
            Browse, filter, and inspect your past synthetic media verifications with probability breakdowns.
          </p>
        </section>

        {records.length > 0 && (
          <>
            {/* 3D Stats Dashboard */}
            <section className="history-stats-grid-3d">
              <TiltCard maxTilt={8} scale={1.02}>
                <div className="stat-card-3d border-cyan">
                  <div className="stat-icon-3d cyan">
                    <BarChart3 size={22} />
                  </div>
                  <div className="stat-info-3d">
                    <span className="stat-lbl">TOTAL SCANNED</span>
                    <strong className="stat-num">{stats.total}</strong>
                    <span className="stat-sub">Files Ingested</span>
                  </div>
                </div>
              </TiltCard>

              <TiltCard maxTilt={8} scale={1.02}>
                <div className="stat-card-3d border-emerald">
                  <div className="stat-icon-3d emerald">
                    <ShieldCheck size={22} />
                  </div>
                  <div className="stat-info-3d">
                    <span className="stat-lbl">AUTHENTIC REAL</span>
                    <strong className="stat-num">{stats.real} <small>({stats.realPct}%)</small></strong>
                    <span className="stat-sub">Natural Imagery</span>
                  </div>
                </div>
              </TiltCard>

              <TiltCard maxTilt={8} scale={1.02}>
                <div className="stat-card-3d border-amber">
                  <div className="stat-icon-3d amber">
                    <ShieldAlert size={22} />
                  </div>
                  <div className="stat-info-3d">
                    <span className="stat-lbl">SYNTHETIC / AI</span>
                    <strong className="stat-num">{stats.fake} <small>({stats.fakePct}%)</small></strong>
                    <span className="stat-sub">Manipulated / GenAI</span>
                  </div>
                </div>
              </TiltCard>

              <TiltCard maxTilt={8} scale={1.02}>
                <div className="stat-card-3d border-purple">
                  <div className="stat-icon-3d purple">
                    <Sparkles size={22} />
                  </div>
                  <div className="stat-info-3d">
                    <span className="stat-lbl">AVG CERTAINTY</span>
                    <strong className="stat-num">{stats.avgConf}<small>%</small></strong>
                    <span className="stat-sub">Model Score</span>
                  </div>
                </div>
              </TiltCard>
            </section>

            {/* 3D Filter & Search Toolbar */}
            <section className="history-toolbar-3d">
              <div className="search-box-3d">
                <Search size={16} />
                <input
                  type="text"
                  placeholder="Filter by filename or class..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
                {search && (
                  <button className="clear-search-btn" onClick={() => setSearch("")}>
                    <X size={14} />
                  </button>
                )}
              </div>

              <div className="filters-group-3d">
                <div className="filter-wrapper-3d">
                  <Filter size={14} />
                  <select
                    value={mediaFilter}
                    onChange={(e) => setMediaFilter(e.target.value)}
                  >
                    <option value="all">All Formats</option>
                    <option value="image">Images Only</option>
                    <option value="video">Videos Only</option>
                  </select>
                </div>

                <div className="filter-wrapper-3d">
                  <Layers size={14} />
                  <select
                    value={resultFilter}
                    onChange={(e) => setResultFilter(e.target.value)}
                  >
                    <option value="all">All Verdicts</option>
                    <option value="real">Authentic Real</option>
                    <option value="fake">Fake / AI Only</option>
                    <option value="ai">AI Generated</option>
                    <option value="cgi">CGI Render</option>
                  </select>
                </div>

                <button
                  className="clear-history-btn-3d"
                  onClick={() => setShowClearConfirm(true)}
                  title="Wipe historical records"
                >
                  <Trash2 size={15} />
                  <span>Clear All</span>
                </button>
              </div>
            </section>
          </>
        )}

        {/* List Section */}
        {records.length === 0 ? (
          <section className="history-empty-3d">
            <div className="empty-hologram-circle">
              <Clock size={40} />
            </div>
            <h2>No verification records yet</h2>
            <p>
              Your processed media analyses and probability logs will automatically appear here with full forensic details.
            </p>
            <Link to="/analyze" className="primary-button-3d">
              <Sparkles size={16} />
              <span>Perform First Analysis</span>
            </Link>
          </section>
        ) : filteredRecords.length === 0 ? (
          <section className="history-empty-3d">
            <div className="empty-hologram-circle">
              <Search size={36} />
            </div>
            <h2>No matching records found</h2>
            <p>Try resetting your search query or format filters.</p>
            <button
              className="secondary-button-3d"
              onClick={() => {
                setSearch("");
                setMediaFilter("all");
                setResultFilter("all");
              }}
            >
              Reset Filters
            </button>
          </section>
        ) : (
          <section className="history-cards-list-3d">
            {filteredRecords.map((item) => {
              const isReal = item.prediction === "real";
              const isAi = item.prediction === "ai";
              const isCgi = item.prediction === "cgi";
              const theme = isReal ? "emerald" : isAi ? "cyan" : isCgi ? "purple" : "amber";

              return (
                <div
                  key={item.id}
                  className={`history-row-card-3d theme-${theme}`}
                  onClick={() => setSelectedRecord(item)}
                >
                  <div className="row-card-left">
                    <div className="row-media-thumb-container">
                      {item.thumbnail ? (
                        <img src={item.thumbnail} alt={item.filename} className="row-media-thumb" />
                      ) : (
                        <div className={`row-media-icon ${item.mediaType}`}>
                          {item.mediaType === "video" ? (
                            <VideoIcon size={20} />
                          ) : (
                            <ImageIcon size={20} />
                          )}
                        </div>
                      )}
                      <span className="row-thumb-badge">
                        {item.mediaType === "video" ? "VID" : "IMG"}
                      </span>
                    </div>

                    <div className="row-text-info">
                      <h3 title={item.filename}>{item.filename}</h3>
                      <div className="row-meta">
                        <span className="row-time">
                          <Clock size={12} /> {formatDate(item.timestamp)}
                        </span>
                        <span className="row-dot">•</span>
                        <span className="row-model">{item.model}</span>
                        {item.processingTimeMs > 0 && (
                          <>
                            <span className="row-dot">•</span>
                            <span>{(item.processingTimeMs / 1000).toFixed(2)}s</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="row-card-right">
                    <div className={`status-pill-3d ${theme}`}>
                      {isReal ? <CheckCircle2 size={14} /> : <AlertTriangle size={14} />}
                      <span>{item.displayLabel || labelMap[item.prediction] || item.prediction}</span>
                    </div>

                    <div className="confidence-gauge-3d">
                      <div className="gauge-header">
                        <span>Confidence</span>
                        <strong>{Number(item.confidence).toFixed(1)}%</strong>
                      </div>
                      <div className="gauge-track">
                        <div
                          className={`gauge-fill ${theme}`}
                          style={{ width: `${Math.min(100, Math.max(8, item.confidence))}%` }}
                        />
                      </div>
                    </div>

                    <button
                      className="row-delete-btn-3d"
                      onClick={(e) => handleDelete(item.id, e)}
                      title="Delete record"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              );
            })}
          </section>
        )}

        {/* 3D Glass Detail Modal */}
        {selectedRecord && (
          <div className="modal-backdrop-3d" onClick={() => setSelectedRecord(null)}>
            <div className="modal-content-3d" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header-3d">
                <div>
                  <span className="modal-eyebrow-3d">DEEPFAKE FORENSIC AUDIT</span>
                  <h2>{selectedRecord.filename}</h2>
                </div>
                <button
                  className="modal-close-3d"
                  onClick={() => setSelectedRecord(null)}
                >
                  <X size={18} />
                </button>
              </div>

              <div className="modal-body-3d">
                {/* Analyzed Image Preview in Modal */}
                {selectedRecord.thumbnail && (
                  <div className="modal-media-preview-container">
                    <img
                      src={selectedRecord.thumbnail}
                      alt={selectedRecord.filename}
                      className="modal-media-preview-img"
                    />
                    <div className="modal-media-caption">
                      <span>Analyzed Media Snapshot</span>
                      <strong>{selectedRecord.filename}</strong>
                    </div>
                  </div>
                )}

                <div className="modal-top-boxes">
                  <div className={`modal-box ${selectedRecord.prediction === "real" ? "emerald" : "amber"}`}>
                    <span>Verdict</span>
                    <strong>{selectedRecord.displayLabel || labelMap[selectedRecord.prediction] || selectedRecord.prediction}</strong>
                  </div>
                  <div className="modal-box cyan">
                    <span>Certainty</span>
                    <strong>{Number(selectedRecord.confidence).toFixed(2)}%</strong>
                  </div>
                  <div className="modal-box purple">
                    <span>Media Type</span>
                    <strong>{selectedRecord.mediaType === "video" ? "Video Stream" : "Image Tensor"}</strong>
                  </div>
                </div>

                {selectedRecord.probabilities && Object.keys(selectedRecord.probabilities).length > 0 && (
                  <div className="modal-prob-section">
                    <h3>
                      <Layers size={16} />
                      <span>Class Probabilities</span>
                    </h3>
                    <div className="modal-prob-list">
                      {Object.entries(selectedRecord.probabilities).map(([className, score]) => {
                        const theme = className === "real" ? "emerald" : className === "ai" ? "cyan" : className === "cgi" ? "purple" : "amber";
                        return (
                          <div className="prob-item-row" key={className}>
                            <div className="prob-item-head">
                              <span>{labelMap[className] || className}</span>
                              <strong>{Number(score).toFixed(2)}%</strong>
                            </div>
                            <div className="prob-item-track">
                              <div
                                className={`prob-item-fill ${theme}`}
                                style={{ width: `${score}%` }}
                              />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                <div className="modal-specs-grid">
                  <div>
                    <span>Logged At</span>
                    <strong>{formatDate(selectedRecord.timestamp)}</strong>
                  </div>
                  <div>
                    <span>Backbone Model</span>
                    <strong>{selectedRecord.model}</strong>
                  </div>
                  <div>
                    <span>Processing Latency</span>
                    <strong>{(selectedRecord.processingTimeMs / 1000).toFixed(2)} seconds</strong>
                  </div>
                  {selectedRecord.sampledFrames && (
                    <div>
                      <span>Temporal Samples</span>
                      <strong>{selectedRecord.sampledFrames} frames</strong>
                    </div>
                  )}
                </div>

                {selectedRecord.frameSummary && (
                  <div className="modal-frame-notice">
                    <Activity size={16} />
                    <span>
                      Frame Consensus: {selectedRecord.frameSummary.fake_frames} manipulated frames vs. {selectedRecord.frameSummary.real_frames} authentic frames.
                    </span>
                  </div>
                )}
              </div>

              <div className="modal-footer-3d">
                <button
                  className="secondary-button-3d"
                  onClick={() => setSelectedRecord(null)}
                >
                  Close Audit
                </button>
                <Link to="/analyze" className="primary-button-3d">
                  <span>Analyze Another</span>
                  <ArrowRight size={15} />
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Clear History Confirmation Modal */}
        {showClearConfirm && (
          <div className="modal-backdrop-3d" onClick={() => setShowClearConfirm(false)}>
            <div className="confirm-modal-3d" onClick={(e) => e.stopPropagation()}>
              <div className="confirm-icon-3d">
                <AlertTriangle size={32} />
              </div>
              <h2>Clear All Logged History?</h2>
              <p>
                Are you sure you want to permanently delete all {records.length} verification records? This action cannot be reversed.
              </p>
              <div className="confirm-actions-3d">
                <button
                  className="secondary-button-3d"
                  onClick={() => setShowClearConfirm(false)}
                >
                  Cancel
                </button>
                <button
                  className="danger-button-3d"
                  onClick={handleClearAll}
                >
                  Yes, Wipe All Records
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </>
  );
}

export default History;