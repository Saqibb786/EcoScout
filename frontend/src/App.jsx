import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import UploadMedia from './components/UploadMedia';
import Results from './components/Results';
import History from './components/History';
import AboutUs from './components/AboutUs';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [latestResults, setLatestResults] = useState(null);
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark');

  React.useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

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
            {/* Project Overview Section */}
            <div className="project-overview">
              <h3>Project Overview</h3>
              <p>
                <strong>EcoScout</strong> is an advanced AI-powered solution designed to monitor and detect vehicle littering and smoke emissions in real-time.
                Utilizing state-of-the-art YOLOv8 object detection and EasyOCR for license plate recognition, EcoScout aims to promote cleaner urban and hilly environments by automating the detection of environmental violations.
              </p>
            </div>

            {/* Key Features Grid */}
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">🚗</div>
                <h3>Litter Detection</h3>
                <p>Identifies trash being thrown from moving vehicles with high accuracy.</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">💨</div>
                <h3>Smoke Emission</h3>
                <p>Detects visible smoke emissions from vehicles to curb air pollution.</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🔢</div>
                <h3>License Plate OCR</h3>
                <p>Automatically extracts license plate numbers for offender identification.</p>
              </div>
            </div>

            {/* Team Info Section removed as per user request (moved to About Us) */}
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
      case 'about':
        return <AboutUs />;

      default:
        return <div>Select a tab</div>;
    }
  };

  return (
    <div className="app-container">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        theme={theme}
        toggleTheme={toggleTheme}
      />
      <div className="main-content">
        <div className="content-area">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

export default App;
