import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiBook, FiCode, FiKey, FiHome } from 'react-icons/fi';
import './Sidebar.css';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/overview', label: 'Overview', icon: <FiHome /> },
    { path: '/documentation', label: 'Documentation', icon: <FiBook /> },
    { path: '/api-explorer', label: 'API Explorer', icon: <FiCode /> },
    { path: '/authentication', label: 'Authentication', icon: <FiKey /> },
  ];

  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-label">{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
