import { Link, useLocation } from 'react-router-dom'
import { TrendingUp, Plus, LogOut, User, Shield } from 'lucide-react'
import { useInvestments } from '../context/InvestmentContext'
import { useState, useEffect } from 'react'
import axios from 'axios'

const Navbar = () => {
  const location = useLocation()
  const { logout } = useInvestments()
  const [isAdmin, setIsAdmin] = useState(false)
  const [loading, setLoading] = useState(true)

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  useEffect(() => {
    const checkAdminStatus = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          setLoading(false)
          return
        }

        const response = await axios.get(`${API_BASE_URL}/profile`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        setIsAdmin(response.data.is_admin === 'true')
      } catch (err) {
        console.error('Error checking admin status:', err)
        setIsAdmin(false)
      } finally {
        setLoading(false)
      }
    }

    checkAdminStatus()
  }, [])

  const isActive = (path) => {
    return location.pathname === path
  }

  const handleLogout = () => {
    logout()
  }

  return (
    <nav className='bg-white shadow-sm border-b border-gray-200'>
      <div className='container mx-auto px-4'>
        <div className='flex justify-between items-center h-16'>
          <div className='flex items-center space-x-4'>
            <Link to='/dashboard' className='flex items-center space-x-2 text-xl font-bold text-primary-600'>
              <TrendingUp className='w-6 h-6' />
              <span>Investment Tracker</span>
            </Link>
          </div>
          
          <div className='flex items-center space-x-4'>
            <Link
              to='/dashboard'
              className='px-3 py-2 rounded-md text-sm font-medium transition-colors'
            >
              Dashboard
            </Link>
            <Link
              to='/add'
              className='px-3 py-2 rounded-md text-sm font-medium transition-colors'
            >
              <Plus className='w-4 h-4 inline mr-1' />
              Add Investment
            </Link>
            <Link
              to='/profile'
              className='px-3 py-2 rounded-md text-sm font-medium transition-colors'
            >
              <User className='w-4 h-4 inline mr-1' />
              Profile
            </Link>
            {!loading && isAdmin && (
              <Link
                to='/admin'
                className='px-3 py-2 rounded-md text-sm font-medium transition-colors bg-yellow-50 text-yellow-700 hover:bg-yellow-100'
              >
                <Shield className='w-4 h-4 inline mr-1' />
                Admin
              </Link>
            )}
            <button
              onClick={handleLogout}
              className='px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors'
            >
              <LogOut className='w-4 h-4 inline mr-1' />
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
