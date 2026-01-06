import React from 'react';
import { LayoutDashboard, Upload, FileText, Calendar, Users, Sun, Moon } from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ activeTab, setActiveTab, theme, toggleTheme }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { id: 'upload', label: 'Upload Media', icon: <Upload size={20} /> },
    { id: 'results', label: 'Detection Results', icon: <FileText size={20} /> },
    { id: 'history', label: 'History', icon: <Calendar size={20} /> },
    { id: 'about', label: 'About Us', icon: <Users size={20} /> },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <img
            src={theme === 'light' ? "/logo_light.png" : "/logo_dark.png"}
            alt="EcoScout"
            className="sidebar-logo-img"
          />
        </div>
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

      <div className="theme-toggle-container">
        <button className="theme-toggle-btn" onClick={toggleTheme} aria-label="Toggle Theme">
          {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
          <span>{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>
        </button>
      </div>

      <div className="sidebar-footer">
        <p>© 2025 EcoScout System</p>
      </div>
    </div>
  );
};

export default Sidebar;
