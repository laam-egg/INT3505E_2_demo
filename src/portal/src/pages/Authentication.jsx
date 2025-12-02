import React from 'react';
import './Authentication.css';

const Authentication = () => {
  return (
    <div className="auth-page">
      <h1>Authentication</h1>
      
      <div className="auth-section">
        <h2>Overview</h2>
        <p>
          The Library Management API uses JWT (JSON Web Tokens) for authentication. 
          Most endpoints require a valid Bearer token in the Authorization header.
        </p>
      </div>

      <div className="auth-section">
        <h2>How to Authenticate</h2>
        
        <h3>Step 1: Register a User Account</h3>
        <p>First, create a user account using the registration endpoint:</p>
        <div className="code-block">
          <pre>
{`POST /api/v4/users/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-secure-password",
  "fullName": "John Doe"
}`}
          </pre>
        </div>

        <h3>Step 2: Login to Get Access Token</h3>
        <p>Use your credentials to login and receive a JWT token:</p>
        <div className="code-block">
          <pre>
{`POST /api/v4/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-secure-password"
}`}
          </pre>
        </div>

        <p>Response:</p>
        <div className="code-block">
          <pre>
{`{
  "content": {
    "user": {
      "id": "user123",
      "email": "user@example.com",
      "fullName": "John Doe"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "_links": {
    "self": ["/api/v4/auth/login"]
  }
}`}
          </pre>
        </div>

        <h3>Step 3: Use the Token in Requests</h3>
        <p>Include the access token in the Authorization header for protected endpoints:</p>
        <div className="code-block">
          <pre>
{`GET /api/v4/patrons/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`}
          </pre>
        </div>
      </div>

      <div className="auth-section">
        <h2>Security Best Practices</h2>
        <ul className="best-practices">
          <li>🔒 Always use HTTPS in production</li>
          <li>🔑 Store tokens securely (never in local storage for sensitive apps)</li>
          <li>⏰ Implement token refresh mechanisms</li>
          <li>🚫 Never share your access tokens</li>
          <li>🔄 Rotate credentials regularly</li>
        </ul>
      </div>

      <div className="auth-section">
        <h2>Protected Endpoints</h2>
        <p>The following endpoints require authentication:</p>
        <ul className="protected-endpoints">
          <li><strong>Patrons:</strong> All endpoints except GET /patrons/ and GET /patrons/&#123;patronId&#125;</li>
          <li><strong>Titles:</strong> POST, PUT, PATCH, DELETE operations</li>
          <li><strong>Copies:</strong> POST, PUT, PATCH, DELETE operations</li>
          <li><strong>Borrows:</strong> All endpoints</li>
          <li><strong>Payments:</strong> All endpoints</li>
          <li><strong>Users:</strong> All endpoints except POST /users/ (registration)</li>
        </ul>
      </div>

      <div className="auth-section">
        <h2>Error Responses</h2>
        <p>Common authentication errors:</p>
        <div className="error-list">
          <div className="error-item">
            <code>401 Unauthorized</code>
            <p>Missing or invalid token</p>
          </div>
          <div className="error-item">
            <code>403 Forbidden</code>
            <p>Valid token but insufficient permissions</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Authentication;
