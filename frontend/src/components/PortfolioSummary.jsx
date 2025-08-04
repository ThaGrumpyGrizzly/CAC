import { TrendingUp, TrendingDown, DollarSign, PieChart, Receipt } from 'lucide-react'

const PortfolioSummary = ({ totalInvested, totalCost, totalCosts, totalCurrentValue, totalProfit, investmentCount }) => {
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2
    }).format(amount)
  }

  const profitPercentage = totalCost > 0 ? ((totalProfit / totalCost) * 100) : 0

  const summaryCards = [
    {
      title: 'Total Invested',
      value: formatCurrency(totalInvested),
      icon: DollarSign,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Total Cost',
      value: formatCurrency(totalCost),
      subtitle: totalCosts > 0 ? `+${formatCurrency(totalCosts)} fees` : '',
      icon: Receipt,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      title: 'Current Value',
      value: formatCurrency(totalCurrentValue),
      icon: PieChart,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'Total Profit/Loss',
      value: formatCurrency(totalProfit),
      icon: totalProfit >= 0 ? TrendingUp : TrendingDown,
      color: totalProfit >= 0 ? 'text-green-600' : 'text-red-600',
      bgColor: totalProfit >= 0 ? 'bg-green-50' : 'bg-red-50'
    },
    {
      title: 'Return',
      value: `${profitPercentage.toFixed(2)}%`,
      icon: totalProfit >= 0 ? TrendingUp : TrendingDown,
      color: totalProfit >= 0 ? 'text-green-600' : 'text-red-600',
      bgColor: totalProfit >= 0 ? 'bg-green-50' : 'bg-red-50'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
      {summaryCards.map((card, index) => {
        const IconComponent = card.icon
        return (
          <div key={index} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.title}</p>
                <p className={`text-2xl font-bold ${card.color}`}>{card.value}</p>
                {card.subtitle && (
                  <p className="text-xs text-gray-500 mt-1">{card.subtitle}</p>
                )}
              </div>
              <div className={`p-3 rounded-full ${card.bgColor}`}>
                <IconComponent className={`w-6 h-6 ${card.color}`} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default PortfolioSummary 