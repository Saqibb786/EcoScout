import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import UploadMedia from './components/UploadMedia';
import Results from './components/Results';
import History from './components/History';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [latestResults, setLatestResults] = useState(null);

  const handleUploadSuccess = (data) => {
    setLatestResults(data);
    setActiveTab('results');
  };

  const handleViewResult = (result) => {
    setLatestResults(result);
    setActiveTab('results');
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <div className="dashboard-view">
            <div className="welcome-card">
              <h2>Welcome to EcoScout</h2>
              <p>Smart Vehicle Littering & Smoke Emission Detection System</p>
              <button className="cta-btn" onClick={() => setActiveTab('upload')}>
                Start Detection
              </button>
            </div>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>System Status</h3>
                <p className="status-ok">Operational</p>
              </div>
              <div className="stat-card">
                <h3>Model</h3>
                <p>YOLOv8 + EasyOCR</p>
              </div>
              <div className="stat-card">
                <h3>Active Session</h3>
                <p>Localhost</p>
              </div>
            </div>
          </div>
        );
      case 'upload':
        return (
          <div className="upload-view">
            <h2>Upload Media</h2>
            <p className="subtitle">Upload images or videos for automated violation detection.</p>
            <UploadMedia onUploadSuccess={handleUploadSuccess} />
          </div>
        );
      case 'results':
        return (
          <div className="results-view">
            <h2>Detection Results</h2>
            <Results results={latestResults} />
          </div>
        );
      case 'history':
        return (
          <div className="history-view">
            <h2>Detection History</h2>
            <History onViewResult={handleViewResult} />
          </div>
        );

      default:
        return <div>Select a tab</div>;
    }
  };

  return (
    <div className="app-container">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="main-content">
        <div className="content-area">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

export default App;
