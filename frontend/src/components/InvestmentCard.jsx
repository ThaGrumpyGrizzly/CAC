import { useState } from 'react'
import { useInvestments } from '../context/InvestmentContext'
import { useNavigate } from 'react-router-dom'
import { TrendingUp, TrendingDown, Trash2, AlertCircle, Plus, History, Edit } from 'lucide-react'

const InvestmentCard = ({ investment }) => {
  const { deletePurchase, getInvestmentDetails } = useInvestments()
  const navigate = useNavigate()
  const [isDeleting, setIsDeleting] = useState(false)
  const [showDetails, setShowDetails] = useState(false)
  const [purchaseHistory, setPurchaseHistory] = useState(null)
  const [loadingDetails, setLoadingDetails] = useState(false)

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this investment?')) {
      setIsDeleting(true)
      try {
        // Note: This will need to be updated to handle multiple purchases
        await deletePurchase(investment.id)
      } catch (error) {
        console.error('Error deleting investment:', error)
      } finally {
        setIsDeleting(false)
      }
    }
  }

  const handleViewDetails = async () => {
    if (!showDetails) {
      setLoadingDetails(true)
      try {
        const details = await getInvestmentDetails(investment.ticker)
        setPurchaseHistory(details.purchases)
      } catch (error) {
        console.error('Error fetching details:', error)
      } finally {
        setLoadingDetails(false)
      }
    }
    setShowDetails(!showDetails)
  }

  const handleAddToPosition = () => {
    // Navigate to add page with pre-filled ticker
    navigate(`/add?ticker=${encodeURIComponent(investment.ticker)}`)
  }

  const handleEditPurchase = (purchaseId) => {
    // Navigate to edit page with purchase data
    navigate(`/edit-purchase/${purchaseId}?ticker=${encodeURIComponent(investment.ticker)}`)
  }

  const handleDeletePurchase = async (purchaseId) => {
    const purchase = purchaseHistory?.find(p => p.id === purchaseId)
    const confirmMessage = purchase 
      ? `Are you sure you want to delete this purchase?\n\n${purchase.amount} shares at €${purchase.price_per_share} on ${purchase.date}`
      : 'Are you sure you want to delete this purchase?'
    
    if (window.confirm(confirmMessage)) {
      try {
        await deletePurchase(purchaseId)
        // Refresh the purchase history
        if (showDetails) {
          const details = await getInvestmentDetails(investment.ticker)
          setPurchaseHistory(details.purchases)
        }
      } catch (error) {
        console.error('Error deleting purchase:', error)
      }
    }
  }

  const formatCurrency = (amount, currency = 'EUR') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2
    }).format(amount)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const hasError = investment.error || investment.current_price === null

  return (
    <div className="card hover:shadow-lg transition-shadow duration-200">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{investment.ticker}</h3>
          <p className="text-sm text-gray-500">
            {investment.purchases?.length || 0} purchase{investment.purchases?.length !== 1 ? 's' : ''}
          </p>
        </div>
        <div className="flex space-x-1">
          <button
            onClick={handleAddToPosition}
            className="text-gray-400 hover:text-green-500 transition-colors p-1"
            title="Add to position"
          >
            <Plus className="w-4 h-4" />
          </button>
          <button
            onClick={handleViewDetails}
            className="text-gray-400 hover:text-blue-500 transition-colors p-1"
            title="View purchase history"
          >
            <History className="w-4 h-4" />
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="text-gray-400 hover:text-red-500 transition-colors p-1"
            title="Delete investment"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Error State */}
      {hasError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4 flex items-start">
          <AlertCircle className="w-4 h-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
          <div className="text-red-700 text-sm">
            {investment.error || 'Unable to fetch current price'}
          </div>
        </div>
      )}

      {/* Investment Details */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="text-gray-600">Total Shares:</span>
          <span className="font-medium">{investment.total_amount}</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-600">Average Price:</span>
          <span className="font-medium">{formatCurrency(investment.average_price)}</span>
        </div>

        {investment.total_costs > 0 && (
          <div className="flex justify-between">
            <span className="text-gray-600">Total Costs:</span>
            <span className="font-medium">{formatCurrency(investment.total_costs)}</span>
          </div>
        )}

        {!hasError && (
          <>
                     <div className="flex justify-between">
           <span className="text-gray-600">Current Price:</span>
           <span className="font-medium">
             {formatCurrency(investment.current_price)}
             {investment.original_price && investment.original_currency && investment.original_currency !== 'EUR' && (
               <span className="text-xs text-gray-500 ml-1">
                 ({formatCurrency(investment.original_price, investment.original_currency)})
               </span>
             )}
           </span>
         </div>

            <div className="flex justify-between">
              <span className="text-gray-600">Total Value:</span>
              <span className="font-medium">{formatCurrency(investment.total_value)}</span>
            </div>

            {/* Profit/Loss */}
            <div className="pt-3 border-t border-gray-200">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Profit/Loss:</span>
                <div className="flex items-center">
                  {investment.total_profit != null && investment.total_profit >= 0 ? (
                    <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-red-500 mr-1" />
                  )}
                  <span className={`font-semibold ${
                    investment.total_profit != null && investment.total_profit >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {investment.total_profit != null ? formatCurrency(investment.total_profit) : 'N/A'}
                  </span>
                </div>
              </div>
              
              {/* Profit Percentage */}
              <div className="flex justify-between items-center mt-1">
                <span className="text-gray-600">Return:</span>
                <span className={`text-sm font-medium ${
                  investment.profit_percentage != null && investment.profit_percentage >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {investment.profit_percentage != null ? `${investment.profit_percentage.toFixed(2)}%` : 'N/A'}
                </span>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Purchase History */}
      {showDetails && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Purchase History</h4>
          {loadingDetails ? (
            <div className="text-sm text-gray-500">Loading...</div>
          ) : purchaseHistory ? (
                         <div className="space-y-2">
               {purchaseHistory.map((purchase, index) => (
                 <div key={purchase.id} className="flex justify-between items-center text-sm border-b border-gray-100 pb-2">
                   <div className="flex-1">
                     <div className="flex items-center justify-between">
                       <div>
                         <span className="font-medium">{purchase.amount} shares</span>
                         <span className="text-gray-500 ml-2">at {formatCurrency(purchase.price_per_share)}</span>
                       </div>
                       <div className="flex space-x-1">
                         <button
                           onClick={() => handleEditPurchase(purchase.id)}
                           className="text-gray-400 hover:text-blue-500 transition-colors p-1"
                           title="Edit purchase"
                         >
                           <Edit className="w-3 h-3" />
                         </button>
                         <button
                           onClick={() => handleDeletePurchase(purchase.id)}
                           className="text-gray-400 hover:text-red-500 transition-colors p-1"
                           title="Delete purchase"
                         >
                           <Trash2 className="w-3 h-3" />
                         </button>
                       </div>
                     </div>
                     <div className="text-right mt-1">
                       <div className="text-gray-500">{formatDate(purchase.date)}</div>
                       {purchase.costs > 0 && (
                         <div className="text-xs text-gray-400">+{formatCurrency(purchase.costs)} fees</div>
                       )}
                     </div>
                   </div>
                 </div>
               ))}
             </div>
          ) : (
            <div className="text-sm text-gray-500">No purchase history available</div>
          )}
        </div>
      )}
    </div>
  )
}

export default InvestmentCard 