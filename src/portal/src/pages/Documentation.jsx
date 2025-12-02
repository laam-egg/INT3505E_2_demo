import React, { useState } from 'react';
import apiSpec from '../../openapi.json';
import './Documentation.css';

const Documentation = () => {
  const [selectedTag, setSelectedTag] = useState('all');
  const [expandedEndpoint, setExpandedEndpoint] = useState(null);

  const tags = ['all', ...apiSpec.tags.map(tag => tag.name)];

  const getMethodColor = (method) => {
    const colors = {
      get: '#61affe',
      post: '#49cc90',
      put: '#fca130',
      patch: '#50e3c2',
      delete: '#f93e3e'
    };
    return colors[method.toLowerCase()] || '#999';
  };

  const getEndpoints = () => {
    const endpoints = [];
    Object.entries(apiSpec.paths).forEach(([path, methods]) => {
      Object.entries(methods).forEach(([method, details]) => {
        if (method !== 'parameters' && typeof details === 'object') {
          endpoints.push({
            path,
            method: method.toUpperCase(),
            ...details
          });
        }
      });
    });
    return endpoints;
  };

  const filteredEndpoints = getEndpoints().filter(endpoint => 
    selectedTag === 'all' || endpoint.tags?.includes(selectedTag)
  );

  const toggleEndpoint = (path, method) => {
    const key = `${method}-${path}`;
    setExpandedEndpoint(expandedEndpoint === key ? null : key);
  };

  const renderParameters = (params) => {
    if (!params || params.length === 0) return null;

    return (
      <div className="params-section">
        <h4>Parameters</h4>
        <table className="params-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>In</th>
              <th>Type</th>
              <th>Required</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {params.map((param, idx) => (
              <tr key={idx}>
                <td><code>{param.name}</code></td>
                <td><span className="param-in">{param.in}</span></td>
                <td>{param.type || param.schema?.type || 'object'}</td>
                <td>{param.required ? '✓' : ''}</td>
                <td>{param.description || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderSchema = (schemaRef) => {
    if (!schemaRef || !schemaRef.$ref) return null;
    
    const schemaName = schemaRef.$ref.split('/').pop();
    const schema = apiSpec.definitions[schemaName];
    
    if (!schema || !schema.properties) return null;

    return (
      <div className="schema-section">
        <h4>Request Body Schema: {schemaName}</h4>
        <table className="schema-table">
          <thead>
            <tr>
              <th>Field</th>
              <th>Type</th>
              <th>Required</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(schema.properties).map(([key, prop]) => (
              <tr key={key}>
                <td><code>{key}</code></td>
                <td>{prop.type}</td>
                <td>{schema.required?.includes(key) ? '✓' : ''}</td>
                <td>{prop.description || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="documentation-page">
      <div className="doc-header">
        <h1>API Documentation</h1>
        <p>Complete reference for all available endpoints</p>
      </div>

      <div className="tag-filters">
        {tags.map(tag => (
          <button
            key={tag}
            className={`tag-filter ${selectedTag === tag ? 'active' : ''}`}
            onClick={() => setSelectedTag(tag)}
          >
            {tag}
          </button>
        ))}
      </div>

      <div className="endpoints-list">
        {filteredEndpoints.map((endpoint, idx) => {
          const key = `${endpoint.method}-${endpoint.path}`;
          const isExpanded = expandedEndpoint === key;
          const bodyParam = endpoint.parameters?.find(p => p.in === 'body');

          return (
            <div key={idx} className="endpoint-card">
              <div 
                className="endpoint-header"
                onClick={() => toggleEndpoint(endpoint.path, endpoint.method)}
              >
                <div className="endpoint-method-path">
                  <span 
                    className="method-badge"
                    style={{ backgroundColor: getMethodColor(endpoint.method) }}
                  >
                    {endpoint.method}
                  </span>
                  <span className="endpoint-path">{endpoint.path}</span>
                </div>
                <div className="endpoint-summary">
                  {endpoint.description || endpoint.summary}
                </div>
                <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
              </div>

              {isExpanded && (
                <div className="endpoint-details">
                  {endpoint.description && (
                    <div className="description">
                      <strong>Description:</strong> {endpoint.description}
                    </div>
                  )}

                  {endpoint.security && (
                    <div className="security-info">
                      <strong>🔐 Authentication Required:</strong> Bearer Token
                    </div>
                  )}

                  {renderParameters(endpoint.parameters)}
                  
                  {bodyParam && renderSchema(bodyParam.schema)}

                  {endpoint.responses && (
                    <div className="responses-section">
                      <h4>Responses</h4>
                      {Object.entries(endpoint.responses).map(([code, response]) => (
                        <div key={code} className="response-item">
                          <span className={`response-code code-${code}`}>{code}</span>
                          <span className="response-desc">{response.description}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Documentation;
