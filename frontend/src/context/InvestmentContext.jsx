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

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  const fetchInvestments = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(`${API_BASE_URL}/investments/summary`)
      setInvestments(response.data)
    } catch (err) {
      setError('Failed to fetch investments')
      console.error('Error fetching investments:', err)
    } finally {
      setLoading(false)
    }
  }

  const addPurchase = async (purchaseData) => {
    try {
      setError(null)
      const response = await axios.post(`${API_BASE_URL}/purchase`, purchaseData)
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
      await axios.delete(`${API_BASE_URL}/purchase/${purchaseId}`)
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
      const response = await axios.put(`${API_BASE_URL}/purchase/${purchaseId}`, purchaseData)
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
      const response = await axios.get(`${API_BASE_URL}/investment/${ticker}/summary`)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to fetch investment details'
      setError(errorMessage)
      throw new Error(errorMessage)
    }
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

  useEffect(() => {
    fetchInvestments()
  }, [])

  const value = {
    investments,
    loading,
    error,
    fetchInvestments,
    addInvestment,
    addPurchase,
    deleteInvestment,
    deletePurchase,
    updatePurchase,
    getInvestmentDetails,
    clearError
  }

  return (
    <InvestmentContext.Provider value={value}>
      {children}
    </InvestmentContext.Provider>
  )
} 