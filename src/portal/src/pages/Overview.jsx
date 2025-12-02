import React from 'react';
import './Overview.css';

const Overview = () => {
  return (
    <div className="overview-page">
      <div className="hero-section">
        <h1>Library Management API</h1>
        <p className="subtitle">Version 4 - Complete API for managing library operations</p>
      </div>

      <div className="info-section">
        <h2>About This API</h2>
        <p>
          The Library Management API provides a comprehensive set of endpoints for managing 
          library operations including patrons, books, borrowing, payments, and webhooks.
        </p>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <h3>📚 Book Management</h3>
          <p>Manage book titles and copies with full CRUD operations</p>
        </div>
        <div className="feature-card">
          <h3>👥 Patron Management</h3>
          <p>Handle library patrons and their premium memberships</p>
        </div>
        <div className="feature-card">
          <h3>📖 Borrowing System</h3>
          <p>Track book borrowing, returns, and lost items</p>
        </div>
        <div className="feature-card">
          <h3>💳 Payment Processing</h3>
          <p>Manage payments with verification and status tracking</p>
        </div>
        <div className="feature-card">
          <h3>🔐 Authentication</h3>
          <p>Secure JWT-based authentication for all operations</p>
        </div>
        <div className="feature-card">
          <h3>🔔 Webhooks</h3>
          <p>Subscribe to events with webhook notifications</p>
        </div>
      </div>

      <div className="quick-start">
        <h2>Quick Start</h2>
        <div className="code-block">
          <pre>
{`# Base URL
https://api.example.com/api/v4

# Authentication
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-password"
}

# Use the returned JWT token
Authorization: Bearer <your_JWT_token>`}
          </pre>
        </div>
      </div>

      <div className="resources-section">
        <h2>Resources</h2>
        <div className="resource-list">
          <div className="resource-item">
            <h4>Patrons</h4>
            <p>Library service users who can borrow books</p>
          </div>
          <div className="resource-item">
            <h4>Titles</h4>
            <p>Book titles with edition, author, and tag information</p>
          </div>
          <div className="resource-item">
            <h4>Copies</h4>
            <p>Physical copies of book titles</p>
          </div>
          <div className="resource-item">
            <h4>Borrows</h4>
            <p>Borrowing transactions with status tracking</p>
          </div>
          <div className="resource-item">
            <h4>Payments</h4>
            <p>Payment transactions for library services</p>
          </div>
          <div className="resource-item">
            <h4>Users</h4>
            <p>System user accounts (admins, librarians)</p>
          </div>
          <div className="resource-item">
            <h4>Webhooks</h4>
            <p>Event subscriptions for real-time notifications</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
