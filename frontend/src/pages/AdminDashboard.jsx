import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { TrendingUp, Search, Filter, BarChart3, Users, DollarSign } from 'lucide-react'
import axios from 'axios'
import StockChart from '../components/StockChart'
import MiniChart from '../components/MiniChart'

const AdminDashboard = () => {
  const [stockAnalytics, setStockAnalytics] = useState([])
  const [filteredStocks, setFilteredStocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('user_count')
  const [sortOrder, setSortOrder] = useState('desc')
  const [totalUniqueUsers, setTotalUniqueUsers] = useState(0)
  const [showAdminButton, setShowAdminButton] = useState(false)
  const navigate = useNavigate()

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchStockAnalytics()
  }, [])

  useEffect(() => {
    filterAndSortStocks()
  }, [stockAnalytics, searchTerm, sortBy, sortOrder])

  const makeMeAdmin = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        setError('No authentication token found.')
        return
      }

      const headers = { Authorization: `Bearer ${token}` }
      const response = await axios.post(`${API_BASE_URL}/make-me-admin`, {}, { headers })
      
      if (response.status === 200) {
        alert('You are now an admin! Please refresh the page.')
        window.location.reload()
      }
    } catch (err) {
      console.error('Error making admin:', err)
      if (err.response?.status === 403) {
        alert('You are already an admin!')
      } else {
        alert('Failed to make admin: ' + (err.response?.data?.detail || err.message))
      }
    }
  }

  const testConnection = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`)
      console.log('Backend connection successful:', response.data)
      return true
    } catch (err) {
      console.error('Backend connection failed:', err)
      return false
    }
  }

  const fetchStockAnalytics = async () => {
    try {
      setLoading(true)
      
      // Test connection first
      const isConnected = await testConnection()
      if (!isConnected) {
        setError('Cannot connect to backend server. Please ensure the backend is running.')
        return
      }
      
      const token = localStorage.getItem('token')
      
      if (!token) {
        setError('No authentication token found. Please log in again.')
        navigate('/login')
        return
      }

      const headers = { Authorization: `Bearer ${token}` }
      console.log('Making request with token:', token.substring(0, 20) + '...')
      
      const response = await axios.get(`${API_BASE_URL}/admin/stock-analytics`, { headers })
      
      // Handle the new response structure
      const responseData = response.data
      if (responseData.stock_analytics) {
        setStockAnalytics(responseData.stock_analytics || [])
        setTotalUniqueUsers(responseData.total_unique_users || 0)
      } else {
        // Fallback for old format
        setStockAnalytics(responseData || [])
        setTotalUniqueUsers(0)
      }
    } catch (err) {
      console.error('Stock analytics fetch error:', err)
      console.error('Response data:', err.response?.data)
      console.error('Response status:', err.response?.status)
      
      if (err.code === 'ERR_NETWORK' || err.message.includes('Network Error')) {
        setError('Cannot connect to server. Please check if the backend is running.')
      } else if (err.response?.status === 401) {
        setError('Authentication failed. Please log in again.')
        localStorage.removeItem('token')
        navigate('/login')
      } else if (err.response?.status === 403) {
        setError('Access denied. Admin privileges required. Click "Make Me Admin" to get admin access.')
      } else {
        setError('Failed to fetch stock analytics: ' + (err.response?.data?.detail || err.message))
      }
    } finally {
      setLoading(false)
    }
  }

  const filterAndSortStocks = () => {
    let filtered = stockAnalytics.filter(stock => 
      stock.ticker.toLowerCase().includes(searchTerm.toLowerCase())
    )

    // Sort the filtered results
    filtered.sort((a, b) => {
      let aValue = a[sortBy]
      let bValue = b[sortBy]
      
      if (sortBy === 'avg_buy_price' || sortBy === 'current_price') {
        // For current_price, use mock data if not available
        if (sortBy === 'current_price') {
          aValue = a.current_price || a.avg_buy_price * 1.05
          bValue = b.current_price || b.avg_buy_price * 1.05
        }
        aValue = parseFloat(aValue) || 0
        bValue = parseFloat(bValue) || 0
      } else {
        aValue = parseInt(aValue) || 0
        bValue = parseInt(bValue) || 0
      }

      if (sortOrder === 'asc') {
        return aValue - bValue
      } else {
        return bValue - aValue
      }
    })

    setFilteredStocks(filtered)
  }

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortOrder('desc')
    }
  }

  const getSortIcon = (field) => {
    if (sortBy !== field) return null
    return sortOrder === 'asc' ? '↑' : '↓'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading stock analytics...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-xl mb-4">⚠️ {error}</div>
          <div className="space-y-4">
            <button
              onClick={makeMeAdmin}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 mr-4"
            >
              Make Me Admin
            </button>
            <button
              onClick={testConnection}
              className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 mr-4"
            >
              Test Connection
            </button>
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700"
            >
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Stock Analytics Dashboard</h1>
          <p className="text-gray-600">Monitor user investments and stock performance across the platform</p>
        </div>

        {/* Search and Filter Controls */}
        <div className="bg-white p-6 rounded-lg shadow mb-8">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="flex-1 max-w-md">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Search by ticker..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Filter className="h-5 w-5 text-gray-500" />
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
                >
                  <option value="user_count">Users</option>
                  <option value="avg_buy_price">Avg Buy Price</option>
                  <option value="current_price">Current Price</option>
                  <option value="ticker">Ticker</option>
                </select>
              </div>
              
              <button
                onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                {sortOrder === 'asc' ? '↑' : '↓'}
              </button>
            </div>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center">
              <BarChart3 className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Companies Invested</p>
                <p className="text-2xl font-bold text-gray-900">{stockAnalytics.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center">
              <Users className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Users</p>
                <p className="text-2xl font-bold text-gray-900">
                  {totalUniqueUsers}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-1 gap-6 mb-8">
          <StockChart 
            data={filteredStocks.slice(0, 8)} 
            chartType="pie" 
            title="Shares Distribution by Stock" 
          />
        </div>

        {/* Stock Analytics Table */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Stock Analytics</h2>
            <p className="text-sm text-gray-600 mt-1">
              Showing {filteredStocks.length} of {stockAnalytics.length} stocks
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('ticker')}
                  >
                    Ticker {getSortIcon('ticker')}
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('user_count')}
                  >
                    Users {getSortIcon('user_count')}
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('avg_buy_price')}
                  >
                    Avg Buy Price {getSortIcon('avg_buy_price')}
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('current_price')}
                  >
                    Current Price {getSortIcon('current_price')}
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Performance
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredStocks.map((stock, index) => {
                  const currentPrice = stock.current_price || stock.avg_buy_price * 1.05 // Fallback to mock data if no real price
                  const performance = currentPrice ? ((currentPrice - stock.avg_buy_price) / stock.avg_buy_price) * 100 : 0
                  const isPositive = performance >= 0
                  
                  return (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-bold text-gray-900">{stock.ticker}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <Users className="h-4 w-4 text-gray-400 mr-2" />
                          <span className="text-sm text-gray-900">{stock.user_count}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">€{stock.avg_buy_price.toFixed(2)}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {stock.current_price ? 
                            `€${stock.current_price.toFixed(2)}` : 
                            <span className="text-gray-400">€{currentPrice.toFixed(2)} (estimated)</span>
                          }
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-2">
                          <span className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                            {isPositive ? '+' : ''}{performance.toFixed(2)}%
                          </span>
                          <MiniChart 
                            performance={performance}
                            isPositive={isPositive}
                          />
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          
          {filteredStocks.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500">No stocks found matching your search criteria.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard 