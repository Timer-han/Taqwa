import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/index.css';
import App from './App';
import { StrictMode } from "react";
import { BrowserRouter } from "react-router-dom";

console.log("this is env: "+ process.env.REACT_APP_API_URL)
console.log("envs:" + process.env.PATH)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
