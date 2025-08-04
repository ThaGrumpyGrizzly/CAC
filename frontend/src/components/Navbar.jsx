import { Link, useLocation } from 'react-router-dom'
import { TrendingUp, Plus, LogOut, User } from 'lucide-react'
import { useInvestments } from '../context/InvestmentContext'

const Navbar = () => {
  const location = useLocation()
  const { logout } = useInvestments()

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
