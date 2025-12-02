import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-logo">
          <h1>Library Management API</h1>
          <span className="version-badge">v4</span>
        </div>
        <div className="header-actions">
          <a 
            href="https://github.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="header-link"
          >
            GitHub
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;
