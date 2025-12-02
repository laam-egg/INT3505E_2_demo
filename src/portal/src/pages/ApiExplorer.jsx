import React, { useState } from 'react';
import axios from 'axios';
import apiSpec from '../../openapi.json';
import './ApiExplorer.css';

const ApiExplorer = () => {
  const [baseUrl, setBaseUrl] = useState('http://localhost:5000/api/v4');
  const [authToken, setAuthToken] = useState('');
  const [selectedEndpoint, setSelectedEndpoint] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState(null);
  const [requestBody, setRequestBody] = useState('{}');
  const [pathParams, setPathParams] = useState({});
  const [queryParams, setQueryParams] = useState({});
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

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

  const selectEndpoint = (endpoint) => {
    setSelectedEndpoint(endpoint.path);
    setSelectedMethod(endpoint.method);
    setResponse(null);
    
    // Initialize parameters
    const pathP = {};
    const queryP = {};
    
    endpoint.parameters?.forEach(param => {
      if (param.in === 'path') {
        pathP[param.name] = '';
      } else if (param.in === 'query') {
        queryP[param.name] = param.default || '';
      }
    });
    
    setPathParams(pathP);
    setQueryParams(queryP);
    
    // Initialize request body if needed
    const bodyParam = endpoint.parameters?.find(p => p.in === 'body');
    if (bodyParam && bodyParam.schema?.$ref) {
      const schemaName = bodyParam.schema.$ref.split('/').pop();
      const schema = apiSpec.definitions[schemaName];
      
      if (schema?.properties) {
        const example = {};
        Object.entries(schema.properties).forEach(([key, prop]) => {
          if (prop.example !== undefined) {
            example[key] = prop.example;
          } else if (prop.type === 'string') {
            example[key] = '';
          } else if (prop.type === 'number' || prop.type === 'integer') {
            example[key] = 0;
          } else if (prop.type === 'boolean') {
            example[key] = false;
          }
        });
        setRequestBody(JSON.stringify(example, null, 2));
      }
    } else {
      setRequestBody('{}');
    }
  };

  const buildUrl = () => {
    let url = baseUrl + selectedEndpoint;
    
    // Replace path parameters
    Object.entries(pathParams).forEach(([key, value]) => {
      url = url.replace(`{${key}}`, value);
    });
    
    // Add query parameters
    const validQueryParams = Object.entries(queryParams)
      .filter(([_, value]) => value !== '')
      .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
      .join('&');
    
    if (validQueryParams) {
      url += '?' + validQueryParams;
    }
    
    return url;
  };

  const executeRequest = async () => {
    setLoading(true);
    setResponse(null);
    
    try {
      const url = buildUrl();
      const headers = {
        'Content-Type': 'application/json',
      };
      
      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
      }
      
      const config = {
        method: selectedMethod.toLowerCase(),
        url,
        headers,
      };
      
      if (['POST', 'PUT', 'PATCH'].includes(selectedMethod) && requestBody) {
        config.data = JSON.parse(requestBody);
      }
      
      const result = await axios(config);
      
      setResponse({
        status: result.status,
        statusText: result.statusText,
        headers: result.headers,
        data: result.data,
        success: true
      });
    } catch (error) {
      setResponse({
        status: error.response?.status || 500,
        statusText: error.response?.statusText || 'Error',
        headers: error.response?.headers || {},
        data: error.response?.data || { message: error.message },
        success: false
      });
    } finally {
      setLoading(false);
    }
  };

  const currentEndpoint = getEndpoints().find(
    e => e.path === selectedEndpoint && e.method === selectedMethod
  );

  return (
    <div className="api-explorer-page">
      <div className="explorer-header">
        <h1>API Explorer</h1>
        <p>Test API endpoints interactively</p>
      </div>

      <div className="explorer-config">
        <div className="config-item">
          <label>Base URL:</label>
          <input
            type="text"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
            className="config-input"
          />
        </div>
        <div className="config-item">
          <label>Authorization Token:</label>
          <input
            type="text"
            value={authToken}
            onChange={(e) => setAuthToken(e.target.value)}
            placeholder="Bearer token (optional)"
            className="config-input"
          />
        </div>
      </div>

      <div className="explorer-body">
        <div className="endpoints-selector">
          <h3>Select Endpoint</h3>
          <div className="endpoints-list-explorer">
            {getEndpoints().map((endpoint, idx) => (
              <div
                key={idx}
                className={`endpoint-item ${
                  selectedEndpoint === endpoint.path && selectedMethod === endpoint.method
                    ? 'selected'
                    : ''
                }`}
                onClick={() => selectEndpoint(endpoint)}
              >
                <span className={`method-badge ${endpoint.method.toLowerCase()}`}>
                  {endpoint.method}
                </span>
                <span className="endpoint-path-small">{endpoint.path}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="request-panel">
          {currentEndpoint ? (
            <>
              <div className="request-header">
                <h3>Request</h3>
                <span className={`method-badge ${selectedMethod.toLowerCase()}`}>
                  {selectedMethod}
                </span>
                <span className="request-path">{selectedEndpoint}</span>
              </div>

              {currentEndpoint.description && (
                <div className="endpoint-description">
                  {currentEndpoint.description}
                </div>
              )}

              {Object.keys(pathParams).length > 0 && (
                <div className="params-section">
                  <h4>Path Parameters</h4>
                  {Object.keys(pathParams).map(param => (
                    <div key={param} className="param-input">
                      <label>{param}:</label>
                      <input
                        type="text"
                        value={pathParams[param]}
                        onChange={(e) => setPathParams({
                          ...pathParams,
                          [param]: e.target.value
                        })}
                      />
                    </div>
                  ))}
                </div>
              )}

              {Object.keys(queryParams).length > 0 && (
                <div className="params-section">
                  <h4>Query Parameters</h4>
                  {Object.keys(queryParams).map(param => {
                    const paramDef = currentEndpoint.parameters?.find(p => p.name === param);
                    return (
                      <div key={param} className="param-input">
                        <label>
                          {param}:
                          {paramDef?.description && (
                            <span className="param-hint"> ({paramDef.description})</span>
                          )}
                        </label>
                        <input
                          type="text"
                          value={queryParams[param]}
                          onChange={(e) => setQueryParams({
                            ...queryParams,
                            [param]: e.target.value
                          })}
                        />
                      </div>
                    );
                  })}
                </div>
              )}

              {['POST', 'PUT', 'PATCH'].includes(selectedMethod) && (
                <div className="body-section">
                  <h4>Request Body</h4>
                  <textarea
                    value={requestBody}
                    onChange={(e) => setRequestBody(e.target.value)}
                    className="body-editor"
                    rows={15}
                  />
                </div>
              )}

              <div className="execute-section">
                <button
                  onClick={executeRequest}
                  disabled={loading}
                  className="execute-button"
                >
                  {loading ? 'Executing...' : 'Execute Request'}
                </button>
              </div>

              {response && (
                <div className="response-section">
                  <h3>Response</h3>
                  <div className="response-status">
                    <span className={`status-badge ${response.success ? 'success' : 'error'}`}>
                      {response.status} {response.statusText}
                    </span>
                  </div>
                  <div className="response-body">
                    <h4>Body:</h4>
                    <pre>{JSON.stringify(response.data, null, 2)}</pre>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="no-selection">
              <p>Select an endpoint from the list to get started</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ApiExplorer;
