import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Trash2, Eye, Calendar, CheckSquare, Square, FileText } from 'lucide-react';
import './History.css';

const History = ({ onViewResult }) => {
    const [history, setHistory] = useState([]);
    const [selectedIds, setSelectedIds] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await axios.get('http://localhost:8000/history');
            setHistory(response.data);
            setLoading(false);
        } catch (error) {
            console.error("Failed to fetch history:", error);
            setLoading(false);
        }
    };

    const toggleSelect = (id) => {
        if (selectedIds.includes(id)) {
            setSelectedIds(selectedIds.filter(item => item !== id));
        } else {
            setSelectedIds([...selectedIds, id]);
        }
    };

    const toggleSelectAll = () => {
        if (selectedIds.length === history.length) {
            setSelectedIds([]);
        } else {
            setSelectedIds(history.map(item => item.id));
        }
    };

    const handleDelete = async () => {
        if (selectedIds.length === 0) return;

        if (window.confirm(`Are you sure you want to delete ${selectedIds.length} records?`)) {
            try {
                await axios.delete('http://localhost:8000/history', { data: selectedIds });
                setHistory(history.filter(item => !selectedIds.includes(item.id)));
                setSelectedIds([]);
            } catch (error) {
                console.error("Failed to delete records:", error);
            }
        }
    };

    if (loading) return <div className="loading">Loading history...</div>;

    return (
        <div className="history-container">
            <div className="history-header">
                <h3>Detection History</h3>
                <div className="history-actions">
                    <button
                        className="download-btn"
                        disabled={selectedIds.length === 0}
                        onClick={() => {
                            selectedIds.forEach(id => {
                                window.open(`http://localhost:8000/report/${id}`, '_blank');
                            });
                        }}
                    >
                        <FileText size={18} />
                        <span>Download Selected ({selectedIds.length})</span>
                    </button>
                    <button
                        className="delete-btn"
                        disabled={selectedIds.length === 0}
                        onClick={handleDelete}
                    >
                        <Trash2 size={18} />
                        <span>Delete Selected ({selectedIds.length})</span>
                    </button>
                </div>
            </div>

            {history.length === 0 ? (
                <div className="history-empty">
                    <p>No detection history found.</p>
                </div>
            ) : (
                <div className="history-grid">
                    <div className="grid-header">
                        <div className="col-select" onClick={toggleSelectAll}>
                            {selectedIds.length === history.length && history.length > 0 ?
                                <CheckSquare size={20} color="var(--accent-primary)" /> :
                                <Square size={20} />
                            }
                        </div>
                        <div className="col-preview">Preview</div>
                        <div className="col-date">Date</div>
                        <div className="col-violations">Violations</div>
                        <div className="col-actions">Actions</div>
                    </div>

                    <div className="grid-body">
                        {history.map((record) => (
                            <div key={record.id} className={`grid-row ${selectedIds.includes(record.id) ? 'selected' : ''}`}>
                                <div className="col-select" onClick={() => toggleSelect(record.id)}>
                                    {selectedIds.includes(record.id) ?
                                        <CheckSquare size={20} color="var(--accent-primary)" /> :
                                        <Square size={20} />
                                    }
                                </div>
                                <div className="col-preview">
                                    <img src={record.annotated_image_url} alt="Preview" />
                                </div>
                                <div className="col-date">
                                    <Calendar size={14} />
                                    <span>{new Date(record.timestamp).toLocaleString()}</span>
                                </div>
                                <div className="col-violations">
                                    {record.detections.length > 0 ? (
                                        <div className="tags">
                                            {record.detections.map((d, i) => (
                                                <span key={i} className={`tag ${d.violation_type.toLowerCase()}`}>
                                                    {d.violation_type}
                                                </span>
                                            ))}
                                        </div>
                                    ) : (
                                        <span className="no-violation">No Violations</span>
                                    )}
                                </div>
                                <div className="col-actions">
                                    <button className="view-btn" onClick={() => onViewResult(record)}>
                                        <Eye size={18} />
                                        <span>View</span>
                                    </button>
                                    <button className="icon-btn" onClick={() => window.open(`http://localhost:8000/report/${record.id}`, '_blank')} title="Download PDF">
                                        <FileText size={18} />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default History;
