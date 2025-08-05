import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const InvestmentContext = createContext()

export const useInvestments = () => {
  const context = useContext(InvestmentContext)
  if (!context) {
    throw new Error('useInvestments must be used within an InvestmentProvider')
  }
  return context
}

export const InvestmentProvider = ({ children }) => {
  const [investments, setInvestments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://cac-production.up.railway.app'

  // Check if user is authenticated on mount
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setIsAuthenticated(true)
      fetchInvestments()
    } else {
      setLoading(false)
    }
  }, [])

  // Create axios instance with auth header
  const createAuthAxios = () => {
    const token = localStorage.getItem('token')
    return axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
  }

  const fetchInvestments = async () => {
    try {
      setLoading(true)
      setError(null)
      const authAxios = createAuthAxios()
      const response = await authAxios.get('/investments/summary')
      setInvestments(response.data)
    } catch (err) {
      if (err.response?.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('token')
        setIsAuthenticated(false)
        setUser(null)
      }
      setError('Failed to fetch investments')
      console.error('Error fetching investments:', err)
    } finally {
      setLoading(false)
    }
  }

  const addPurchase = async (purchaseData) => {
    try {
      setError(null)
      const authAxios = createAuthAxios()
      const response = await authAxios.post('/purchase', purchaseData)
      await fetchInvestments() // Refresh the list
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to add purchase'
      setError(errorMessage)
      throw new Error(errorMessage)
    }
  }

  const deletePurchase = async (purchaseId) => {
    try {
      setError(null)
      const authAxios = createAuthAxios()
      await authAxios.delete(`/purchase/${purchaseId}`)
      await fetchInvestments() // Refresh the list
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to delete purchase'
      setError(errorMessage)
      throw new Error(errorMessage)
    }
  }

  const updatePurchase = async (purchaseId, purchaseData) => {
    try {
      setError(null)
      const authAxios = createAuthAxios()
      const response = await authAxios.put(`/purchase/${purchaseId}`, purchaseData)
      await fetchInvestments() // Refresh the list
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to update purchase'
      setError(errorMessage)
      throw new Error(errorMessage)
    }
  }

  const getInvestmentDetails = async (ticker) => {
    try {
      setError(null)
      const authAxios = createAuthAxios()
      const response = await authAxios.get(`/investment/${ticker}/summary`)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to fetch investment details'
      setError(errorMessage)
      throw new Error(errorMessage)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/login`, {
        email,
        password
      })
      
      localStorage.setItem('token', response.data.access_token)
      setIsAuthenticated(true)
      await fetchInvestments()
      return response.data
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Login failed')
    }
  }

  const register = async (email, username, password) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/register`, {
        email,
        username,
        password
      })
      return response.data
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Registration failed')
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setIsAuthenticated(false)
    setUser(null)
    setInvestments([])
  }

  // Keep old methods for backward compatibility
  const addInvestment = async (investmentData) => {
    return addPurchase(investmentData)
  }

  const deleteInvestment = async (investmentId) => {
    return deletePurchase(investmentId)
  }

  const clearError = () => {
    setError(null)
  }

  const value = {
    investments,
    loading,
    error,
    isAuthenticated,
    user,
    fetchInvestments,
    addPurchase,
    deletePurchase,
    updatePurchase,
    getInvestmentDetails,
    login,
    register,
    logout,
    addInvestment,
    deleteInvestment,
    clearError
  }

  return (
    <InvestmentContext.Provider value={value}>
      {children}
    </InvestmentContext.Provider>
  )
}
