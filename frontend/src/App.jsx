import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useInvestments, InvestmentProvider } from './context/InvestmentContext'
import Dashboard from './pages/Dashboard'
import AddInvestment from './pages/AddInvestment'
import EditPurchase from './pages/EditPurchase'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import Navbar from './components/Navbar'

// Protected Route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useInvestments()
  
  if (loading) {
    return <div className='min-h-screen flex items-center justify-center'>Loading...</div>
  }
  
  if (!isAuthenticated) {
    return <Navigate to='/login' replace />
  }
  
  return children
}

function App() {
  return (
    <InvestmentProvider>
      <Router>
        <div className='min-h-screen bg-gray-50'>
          <Routes>
            {/* Public routes */}
            <Route path='/login' element={<Login />} />
            <Route path='/register' element={<Register />} />
            
            {/* Protected routes */}
            <Route path='/' element={
              <ProtectedRoute>
                <div>
                  <Navbar />
                  <main className='container mx-auto px-4 py-8'>
                    <Dashboard />
                  </main>
                </div>
              </ProtectedRoute>
            } />
            <Route path='/dashboard' element={
              <ProtectedRoute>
                <div>
                  <Navbar />
                  <main className='container mx-auto px-4 py-8'>
                    <Dashboard />
                  </main>
                </div>
              </ProtectedRoute>
            } />
            <Route path='/add' element={
              <ProtectedRoute>
                <div>
                  <Navbar />
                  <main className='container mx-auto px-4 py-8'>
                    <AddInvestment />
                  </main>
                </div>
              </ProtectedRoute>
            } />
            <Route path='/edit-purchase/:purchaseId' element={
              <ProtectedRoute>
                <div>
                  <Navbar />
                  <main className='container mx-auto px-4 py-8'>
                    <EditPurchase />
                  </main>
                </div>
              </ProtectedRoute>
            } />
            <Route path='/profile' element={
              <ProtectedRoute>
                <div>
                  <Navbar />
                  <main className='container mx-auto px-4 py-8'>
                    <Profile />
                  </main>
                </div>
              </ProtectedRoute>
            } />
            
            {/* Redirect root to dashboard */}
            <Route path='*' element={<Navigate to='/dashboard' replace />} />
          </Routes>
        </div>
      </Router>
    </InvestmentProvider>
  )
}

export default App
