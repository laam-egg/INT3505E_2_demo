import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Overview from './pages/Overview';
import Documentation from './pages/Documentation';
import ApiExplorer from './pages/ApiExplorer';
import Authentication from './pages/Authentication';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <div className="app-body">
          <Sidebar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Navigate to="/overview" replace />} />
              <Route path="/overview" element={<Overview />} />
              <Route path="/documentation" element={<Documentation />} />
              <Route path="/api-explorer" element={<ApiExplorer />} />
              <Route path="/authentication" element={<Authentication />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
