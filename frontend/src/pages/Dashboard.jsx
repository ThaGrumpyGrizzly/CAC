import { useInvestments } from '../context/InvestmentContext'
import { RefreshCw, TrendingUp, TrendingDown, DollarSign, PieChart } from 'lucide-react'
import { Link } from 'react-router-dom'
import InvestmentCard from '../components/InvestmentCard'
import PortfolioSummary from '../components/PortfolioSummary'
import LoadingSpinner from '../components/LoadingSpinner'

const Dashboard = () => {
  const { investments, loading, error, fetchInvestments } = useInvestments()

  const handleRefresh = () => {
    fetchInvestments()
  }

  if (loading) {
    return <LoadingSpinner />
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-4">{error}</div>
        <button onClick={handleRefresh} className="btn-primary">
          <RefreshCw className="w-4 h-4 inline mr-2" />
          Retry
        </button>
      </div>
    )
  }

  const totalInvested = investments.reduce((sum, inv) => {
    return sum + (inv.total_amount * inv.average_price)
  }, 0)

  const totalCosts = investments.reduce((sum, inv) => {
    return sum + (inv.total_costs || 0)
  }, 0)

  const totalCost = totalInvested + totalCosts

  const totalCurrentValue = investments.reduce((sum, inv) => {
    return sum + (inv.total_value || 0)
  }, 0)

  const totalProfit = totalCurrentValue - totalCost

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Portfolio Dashboard</h1>
        <button 
          onClick={handleRefresh}
          className="btn-secondary flex items-center"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </button>
      </div>

      {/* Portfolio Summary */}
      <PortfolioSummary 
        totalInvested={totalInvested}
        totalCost={totalCost}
        totalCosts={totalCosts}
        totalCurrentValue={totalCurrentValue}
        totalProfit={totalProfit}
        investmentCount={investments.length}
      />

      {/* Investments List */}
      <div className="card">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Your Investments</h2>
          <span className="text-sm text-gray-500">
            {investments.length} investment{investments.length !== 1 ? 's' : ''}
          </span>
        </div>

        {investments.length === 0 ? (
          <div className="text-center py-12">
            <PieChart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No investments yet</h3>
            <p className="text-gray-500 mb-4">
              Start tracking your investments by adding your first position.
            </p>
            <Link to="/add" className="btn-primary">
              Add Your First Investment
            </Link>
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {investments.map((investment, index) => (
              <InvestmentCard 
                key={investment.id || `investment-${index}`} 
                investment={investment} 
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard 