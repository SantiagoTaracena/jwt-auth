/**
 * Universidad del Valle de Guatemala
 * Cifrado de Información
 * Ejercicio - Firmas Digitales JWT
 * Santiago Taracena Puga (20017)
 */

// Librerías necesarias para el frontend.
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

// Raíz de la app y de React.
const root = document.getElementById('root')
const reactRoot = ReactDOM.createRoot(root)

// Renderización de la raíz.
reactRoot.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
