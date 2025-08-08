import React from 'react'

const MiniChart = ({ performance, isPositive }) => {
  // Generate mock data points for the mini chart
  const generateDataPoints = () => {
    const points = []
    const baseValue = 50
    const volatility = 15
    
    for (let i = 0; i < 8; i++) {
      const randomChange = (Math.random() - 0.5) * volatility
      const value = Math.max(10, Math.min(90, baseValue + randomChange))
      points.push(value)
    }
    
    // Ensure the last point reflects the performance
    if (isPositive) {
      points[points.length - 1] = Math.max(points[points.length - 1], 60)
    } else {
      points[points.length - 1] = Math.min(points[points.length - 1], 40)
    }
    
    return points
  }

  const dataPoints = generateDataPoints()
  const maxValue = Math.max(...dataPoints)
  const minValue = Math.min(...dataPoints)
  const range = maxValue - minValue

  return (
    <div className="w-16 h-8 bg-gray-50 rounded border">
      <svg width="64" height="32" className="w-full h-full">
        <polyline
          fill="none"
          stroke={isPositive ? "#10B981" : "#EF4444"}
          strokeWidth="1.5"
          points={dataPoints.map((value, index) => {
            const x = (index / (dataPoints.length - 1)) * 60 + 2
            const y = 30 - ((value - minValue) / range) * 24 - 4
            return `${x},${y}`
          }).join(' ')}
        />
      </svg>
    </div>
  )
}

export default MiniChart 