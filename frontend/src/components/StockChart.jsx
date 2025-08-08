import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const StockChart = ({ data, chartType = 'bar', title }) => {
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D']

  const formatTooltip = (value, name) => {
    if (name === 'user_count') return [value, 'Users']
    if (name === 'purchase_count') return [value, 'Purchases']
    if (name === 'total_shares') return [value.toFixed(1), 'Shares']
    if (name === 'avg_buy_price') return [`€${value.toFixed(2)}`, 'Avg Buy Price']
    if (name === 'total_costs') return [`€${value.toFixed(2)}`, 'Total Invested']
    return [value, name]
  }

  if (chartType === 'pie') {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ ticker, total_shares }) => `${ticker} (${total_shares.toFixed(1)})`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="total_shares"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={formatTooltip} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    )
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="ticker" />
          <YAxis />
          <Tooltip formatter={formatTooltip} />
          <Bar dataKey="user_count" fill="#8884d8" name="Users" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default StockChart 