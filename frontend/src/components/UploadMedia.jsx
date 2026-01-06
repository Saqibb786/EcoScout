import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Upload, X, FileVideo, Image as ImageIcon, CheckCircle, AlertCircle } from 'lucide-react';
import './UploadMedia.css';

const UploadMedia = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setError(null);

            // Create preview
            if (selectedFile.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onloadend = () => {
                    setPreview(reader.result);
                };
                reader.readAsDataURL(selectedFile);
            } else if (selectedFile.type.startsWith('video/')) {
                setPreview(null); // Video preview logic can be added if needed
            }
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const selectedFile = e.dataTransfer.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setError(null);
            if (selectedFile.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onloadend = () => {
                    setPreview(reader.result);
                };
                reader.readAsDataURL(selectedFile);
            }
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a file first.");
            return;
        }

        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post('http://localhost:8000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            if (response.data) {
                onUploadSuccess(response.data);
                setFile(null);
                setPreview(null);
                if (fileInputRef.current) fileInputRef.current.value = "";
            }
        } catch (err) {
            console.error("Upload failed:", err);
            setError(err.response?.data?.detail || "Upload failed. Please try again.");
        } finally {
            setUploading(false);
        }
    };

    const clearFile = () => {
        setFile(null);
        setPreview(null);
        setError(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
    };

    return (
        <div className="upload-container">
            <div
                className={`drop-zone ${file ? 'has-file' : ''}`}
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
            >
                {!file ? (
                    <div className="upload-prompt">
                        <Upload size={48} className="upload-icon" />
                        <h3>Drag & Drop or Click to Upload</h3>
                        <p>Supports JPG, PNG, MP4</p>
                        <input
                            type="file"
                            ref={fileInputRef}
                            onChange={handleFileChange}
                            accept="image/*,video/*"
                            className="file-input"
                            style={{ display: 'none' }}
                            onClick={(e) => e.stopPropagation()}
                        />
                    </div>
                ) : (
                    <div className="file-preview">
                        <div className="preview-content">
                            {preview ? (
                                <img src={preview} alt="Preview" className="image-preview" />
                            ) : (
                                <div className="video-placeholder">
                                    <FileVideo size={48} />
                                    <p>{file.name}</p>
                                </div>
                            )}
                        </div>
                        <div className="file-info">
                            <span className="file-name">{file.name}</span>
                            <button onClick={clearFile} className="remove-btn">
                                <X size={20} />
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {error && (
                <div className="error-message">
                    <AlertCircle size={20} />
                    <span>{error}</span>
                </div>
            )}

            <div className="upload-actions">
                <button
                    className="upload-btn"
                    onClick={handleUpload}
                    disabled={!file || uploading}
                >
                    {uploading ? "Processing..." : "Run Detection"}
                </button>
            </div>
        </div>
    );
};

export default UploadMedia;
