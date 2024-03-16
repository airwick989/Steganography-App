// index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* <AuthProvider>
      <App />
    </AuthProvider> */}
    <div
      style={{
          position: 'absolute', left: '50%', top: '50%',
          transform: 'translate(-50%, -50%)'
      }}
      >
      <App />
    </div>,
  </React.StrictMode>,
);