import React from 'react';
import { CheckCircle, AlertTriangle, Car, FileText } from 'lucide-react';
import './Results.css';

const Results = ({ results }) => {
    if (!results) {
        return (
            <div className="results-empty">
                <div className="empty-state">
                    <FileText size={48} />
                    <h3>No Results Yet</h3>
                    <p>Upload an image or video to see detection results here.</p>
                </div>
            </div>
        );
    }

    const { original_file, annotated_image_url, detections, timestamp } = results;

    return (
        <div className="results-container">
            <div className="results-header">
                <h3>Detection Analysis</h3>
                <div className="header-actions">
                    <button className="download-btn" onClick={() => window.open(`http://localhost:8000/report/${results.id}`, '_blank')}>
                        <FileText size={16} />
                        Download Report
                    </button>
                    <span className="timestamp">{new Date(timestamp).toLocaleString()}</span>
                </div>
            </div>

            <div className="results-grid">
                <div className="image-section">
                    <h4>Annotated Output</h4>
                    <div className="annotated-image-wrapper">
                        {results.annotated_video_url ? (
                            <video controls src={results.annotated_video_url} className="result-video" width="100%" />
                        ) : (
                            <img src={annotated_image_url} alt="Annotated Detection" />
                        )}
                    </div>
                    <p className="file-ref">Source: {original_file}</p>
                </div>

                <div className="data-section">
                    <h4>Detected Violations & Objects</h4>

                    {detections.length === 0 ? (
                        <div className="no-detections">
                            <CheckCircle size={24} color="#22c55e" />
                            <p>No violations or objects detected.</p>
                        </div>
                    ) : (
                        <div className="detections-list">
                            {detections.map((det, index) => (
                                <div key={index} className={`detection-card ${det.violation_type.toLowerCase()}`}>
                                    <div className="card-header">
                                        <span className="violation-type">{det.violation_type}</span>
                                        <span className="confidence-badge">{det.confidence}% Conf.</span>
                                    </div>

                                    <div className="card-details">
                                        {det.license_plate !== "N/A" && (
                                            <div className="plate-info">
                                                <Car size={16} />
                                                <span className="plate-number">{det.license_plate}</span>
                                                <span className="ocr-conf">(OCR: {det.ocr_confidence}%)</span>
                                            </div>
                                        )}

                                        {(det.violation_type.toLowerCase() === 'littering' || det.violation_type.toLowerCase() === 'smoke') && (
                                            <div className="violation-alert">
                                                <AlertTriangle size={16} />
                                                <span>Violation Detected</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Results;
