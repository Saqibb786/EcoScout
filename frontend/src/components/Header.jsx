import React from 'react';
import './Header.css';

const Header = ({ title }) => {
    return (
        <header className="header">
            <h1>{title}</h1>
            <div className="header-actions">
                <span className="status-badge">System Online</span>
            </div>
        </header>
    );
};

export default Header;
