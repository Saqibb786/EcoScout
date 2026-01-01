import React from 'react';
import { LayoutDashboard, Upload, FileText, Calendar } from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { id: 'upload', label: 'Upload Media', icon: <Upload size={20} /> },
    { id: 'results', label: 'Detection Results', icon: <FileText size={20} /> },
    { id: 'history', label: 'History', icon: <Calendar size={20} /> },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>EcoScout</h2>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="sidebar-footer">
        <p>© 2025 EcoScout System</p>
      </div>
    </div>
  );
};

export default Sidebar;
