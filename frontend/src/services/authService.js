import { loginUser as firebaseLogin, registerUser as firebaseRegister } from './firebaseService'

// For now, we'll use the backend API instead of Firebase
const USE_BACKEND_API = true

// Supabase authentication functions (disabled for now)
const supabaseLogin = async (email, password) => {
  throw new Error('Supabase not configured')
}

const supabaseRegister = async (email, password, username) => {
  throw new Error('Supabase not configured')
}

// Backend API authentication functions
const backendLogin = async (email, password) => {
  const response = await fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password })
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Login failed')
  }
  
  const data = await response.json()
  localStorage.setItem('token', data.access_token)
  return { email }
}

const backendRegister = async (email, password, username) => {
  const response = await fetch('http://localhost:8000/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password, username })
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Registration failed')
  }
  
  return await response.json()
}

// Unified authentication service
export const loginUser = async (email, password) => {
  if (USE_BACKEND_API) {
    return await backendLogin(email, password)
  } else {
    return await firebaseLogin(email, password)
  }
}

export const registerUser = async (email, password, username) => {
  if (USE_BACKEND_API) {
    return await backendRegister(email, password, username)
  } else {
    return await firebaseRegister(email, password, username)
  }
}

export const getCurrentUser = () => {
  if (USE_BACKEND_API) {
    // Backend API user
    const token = localStorage.getItem('token')
    return token ? { token } : null
  } else {
    // Firebase user
    return auth.currentUser
  }
} 