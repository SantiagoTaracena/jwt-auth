/**
 * Universidad del Valle de Guatemala
 * Cifrado de Información
 * Ejercicio - Firmas Digitales JWT
 * Santiago Taracena Puga (20017)
 */

// Librerías necesarias para el frontend.
import React, { useState } from 'react'
import axios from 'axios'

// Componente App principal en la aplicación.
const App = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [token, setToken] = useState('')
  const [message, setMessage] = useState('')

  // Función para manejar el registro de usuarios.
  const handleRegister = async () => {
    console.log(username, password)
    try {
      const response = await axios.post('http://localhost:5000/register', {
        username,
        password
      })
      setMessage(response.data.message)
    } catch (error) {
      setMessage(error.response.data.message)
    }
  }

  // Función para manejar el login de usuarios.
  const handleLogin = async () => {
    console.log(username, password)
    try {
      const response = await axios.post('http://localhost:5000/login', {
        username,
        password
      })
      if (response.data.token) {
        setToken(response.data.token)
        setMessage('Login successful')
      } else {
        setMessage('Could not login')
      }
    } catch (error) {
      setMessage(error.response.data.message)
    }
  }

  // Función para acceder a un recurso protegido.
  const handleProtected = async () => {
    try {
      const response = await axios.get('http://localhost:5000/protected', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      setMessage(response.data.message)
    } catch (error) {
      setMessage(error.response.data.message)
    }
  }

  // Interfaz de usuario del componente.
  return (
    <div>
      <h1>JWT Authentication Demo</h1>
      <div>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <button onClick={handleRegister}>Register</button>
        <button onClick={handleLogin}>Login</button>
      </div>
      {token && (
        <div>
          <button onClick={handleProtected}>Access Protected Resource</button>
        </div>
      )}
      {message && <p>{message}</p>}
    </div>
  )
}

// Exportación del componente.
export default App
