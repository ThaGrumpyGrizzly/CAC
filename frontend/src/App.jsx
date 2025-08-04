import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import AddInvestment from './pages/AddInvestment'
import EditPurchase from './pages/EditPurchase'
import Navbar from './components/Navbar'
import { InvestmentProvider } from './context/InvestmentContext'

function App() {
  return (
    <InvestmentProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/add" element={<AddInvestment />} />
              <Route path="/edit-purchase/:purchaseId" element={<EditPurchase />} />
            </Routes>
          </main>
        </div>
      </Router>
    </InvestmentProvider>
  )
}

export default App 