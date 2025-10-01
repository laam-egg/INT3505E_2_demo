import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

import { OpenAPI } from './api/index.ts'

OpenAPI.BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api/v1'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
