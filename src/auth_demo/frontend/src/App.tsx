import React from "react";
import { BrowserRouter, Route, Routes } from "react-router";

const Home = React.lazy(() => import('./pages/home'));
const AuthHTTPOnlyCookie = React.lazy(() => import('./pages/auth_httponly_cookie'));
const AuthLocalStorage = React.lazy(() => import('./pages/auth_localStorage'));
const AuthSessionStorage = React.lazy(() => import('./pages/auth_sessionStorage'));

function App() {
  return <>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/local_storage" element={<AuthLocalStorage />} />
        <Route path="/session_storage" element={<AuthSessionStorage />} />
        <Route path="/httponly_cookie" element={<AuthHTTPOnlyCookie />} />
      </Routes>
    </BrowserRouter>
  </>
}

export default App
