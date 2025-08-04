import { Link, useLocation } from 'react-router-dom'
import { TrendingUp, Plus } from 'lucide-react'

const Navbar = () => {
  const location = useLocation()

  const isActive = (path) => {
    return location.pathname === path
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <Link to="/" className="flex items-center space-x-2 text-xl font-bold text-primary-600">
              <TrendingUp className="w-6 h-6" />
              <span>Investment Tracker</span>
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/') 
                  ? 'bg-primary-100 text-primary-700' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/add"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/add') 
                  ? 'bg-primary-100 text-primary-700' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Plus className="w-4 h-4 inline mr-1" />
              Add Investment
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 