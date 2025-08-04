import { useState, useEffect } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { useInvestments } from '../context/InvestmentContext'
import { ArrowLeft, Save, AlertCircle } from 'lucide-react'

const EditPurchase = () => {
  const navigate = useNavigate()
  const { purchaseId } = useParams()
  const [searchParams] = useSearchParams()
  const { getInvestmentDetails, updatePurchase, error, clearError } = useInvestments()
  const [loading, setLoading] = useState(false)
  const [purchase, setPurchase] = useState(null)
  const [formData, setFormData] = useState({
    amount: '',
    price_per_share: '',
    date: '',
    costs: '0'
  })

  // Load purchase data
  useEffect(() => {
    const loadPurchase = async () => {
      try {
        const ticker = searchParams.get('ticker')
        if (ticker && purchaseId) {
          const details = await getInvestmentDetails(ticker)
          const foundPurchase = details.purchases.find(p => p.id === purchaseId)
          if (foundPurchase) {
            setPurchase(foundPurchase)
            setFormData({
              amount: foundPurchase.amount.toString(),
              price_per_share: foundPurchase.price_per_share.toString(),
              date: foundPurchase.date,
              costs: foundPurchase.costs.toString()
            })
          }
        }
      } catch (error) {
        console.error('Error loading purchase:', error)
      }
    }

    loadPurchase()
  }, [purchaseId, searchParams, getInvestmentDetails])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    if (error) clearError()
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const updateData = {
        amount: parseFloat(formData.amount),
        price_per_share: parseFloat(formData.price_per_share),
        date: formData.date,
        costs: parseFloat(formData.costs) || 0
      }

      await updatePurchase(purchaseId, updateData)
      navigate('/')
    } catch (err) {
      console.error('Error updating purchase:', err)
    } finally {
      setLoading(false)
    }
  }

  const isFormValid = () => {
    return (
      formData.amount > 0 &&
      formData.price_per_share > 0 &&
      formData.date
    )
  }

  if (!purchase) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="text-center py-8">
          <div className="text-gray-600">Loading purchase details...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center mb-6">
        <button
          onClick={() => navigate('/')}
          className="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-3xl font-bold text-gray-900">
          Edit Purchase - {purchase.ticker}
        </h1>
      </div>

      {/* Form */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
              <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
              <div className="text-red-700">{error}</div>
            </div>
          )}

          {/* Ticker (Read-only) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Stock/ETF Ticker
            </label>
            <input
              type="text"
              value={purchase.ticker}
              readOnly
              className="input-field bg-gray-50"
            />
          </div>

          {/* Number of Shares */}
          <div>
            <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
              Number of Shares *
            </label>
            <input
              type="number"
              id="amount"
              name="amount"
              value={formData.amount}
              onChange={handleInputChange}
              placeholder="10"
              min="0.001"
              step="0.001"
              className="input-field"
              required
            />
          </div>

          {/* Price per Share */}
          <div>
            <label htmlFor="price_per_share" className="block text-sm font-medium text-gray-700 mb-2">
              Price per Share (€) *
            </label>
            <input
              type="number"
              id="price_per_share"
              name="price_per_share"
              value={formData.price_per_share}
              onChange={handleInputChange}
              placeholder="150.50"
              min="0.01"
              step="0.01"
              className="input-field"
              required
            />
          </div>

          {/* Purchase Date */}
          <div>
            <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-2">
              Purchase Date *
            </label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleInputChange}
              className="input-field"
              required
            />
          </div>

          {/* Additional Costs */}
          <div>
            <label htmlFor="costs" className="block text-sm font-medium text-gray-700 mb-2">
              Additional Costs (€)
            </label>
            <input
              type="number"
              id="costs"
              name="costs"
              value={formData.costs}
              onChange={handleInputChange}
              placeholder="5.00"
              min="0"
              step="0.01"
              className="input-field"
            />
            <p className="mt-1 text-sm text-gray-500">
              Brokerage fees, transaction costs, etc.
            </p>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!isFormValid() || loading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Updating...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4 mr-2" />
                  Update Purchase
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default EditPurchase 