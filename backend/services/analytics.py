from typing import Dict, List, Optional
from datetime import datetime, timedelta

def calculate_profit(investment, current_price: float) -> float:
    """
    Calculate profit/loss for an investment
    """
    total_cost = investment.amount * investment.price_per_share + investment.costs
    current_value = investment.amount * current_price
    return round(current_value - total_cost, 2)

def calculate_profit_percentage(investment, current_price: float) -> float:
    """
    Calculate profit/loss percentage
    """
    total_cost = investment.amount * investment.price_per_share + investment.costs
    current_value = investment.amount * current_price
    if total_cost == 0:
        return 0
    return round(((current_value - total_cost) / total_cost) * 100, 2)

def calculate_total_portfolio_value(investments: List[Dict]) -> Dict:
    """
    Calculate total portfolio value and metrics
    """
    total_invested = 0
    total_current_value = 0
    total_profit = 0
    total_costs = 0
    
    for inv in investments:
        if inv.get('current_price') is not None:
            invested = inv['amount'] * inv['price_per_share']
            current_value = inv['amount'] * inv['current_price']
            profit = inv.get('profit', 0)
            costs = inv.get('costs', 0)
            
            total_invested += invested
            total_current_value += current_value
            total_profit += profit
            total_costs += costs
    
    total_cost = total_invested + total_costs
    
    total_profit_percentage = 0
    if total_cost > 0:
        total_profit_percentage = round(((total_current_value - total_cost) / total_cost) * 100, 2)
    
    return {
        'total_invested': round(total_invested, 2),
        'total_cost': round(total_cost, 2),
        'total_current_value': round(total_current_value, 2),
        'total_profit': round(total_profit, 2),
        'total_profit_percentage': total_profit_percentage,
        'total_costs': round(total_costs, 2),
        'investment_count': len(investments)
    }

def get_best_performing_investment(investments: List[Dict]) -> Optional[Dict]:
    """
    Get the best performing investment by profit percentage
    """
    if not investments:
        return None
    
    best_investment = None
    best_percentage = float('-inf')
    
    for inv in investments:
        if inv.get('current_price') is not None:
            percentage = calculate_profit_percentage(inv, inv['current_price'])
            if percentage > best_percentage:
                best_percentage = percentage
                best_investment = inv
    
    return best_investment

def get_worst_performing_investment(investments: List[Dict]) -> Optional[Dict]:
    """
    Get the worst performing investment by profit percentage
    """
    if not investments:
        return None
    
    worst_investment = None
    worst_percentage = float('inf')
    
    for inv in investments:
        if inv.get('current_price') is not None:
            percentage = calculate_profit_percentage(inv, inv['current_price'])
            if percentage < worst_percentage:
                worst_percentage = percentage
                worst_investment = inv
    
    return worst_investment

def calculate_risk_metrics(investments: List[Dict]) -> Dict:
    """
    Calculate basic risk metrics for the portfolio
    """
    if not investments:
        return {
            'volatility': 0,
            'diversification_score': 0,
            'risk_level': 'Low'
        }
    
    # Calculate portfolio weights
    total_value = sum(inv.get('total_value', 0) for inv in investments if inv.get('total_value'))
    
    if total_value == 0:
        return {
            'volatility': 0,
            'diversification_score': 0,
            'risk_level': 'Low'
        }
    
    weights = []
    for inv in investments:
        if inv.get('total_value'):
            weights.append(inv['total_value'] / total_value)
    
    # Simple diversification score (1 = perfectly diversified, 0 = concentrated)
    if len(weights) > 1:
        diversification_score = 1 - max(weights)
    else:
        diversification_score = 0
    
    # Simple risk level based on diversification
    if diversification_score > 0.7:
        risk_level = 'Low'
    elif diversification_score > 0.4:
        risk_level = 'Medium'
    else:
        risk_level = 'High'
    
    return {
        'volatility': 0,  # Would need historical data for real volatility
        'diversification_score': round(diversification_score, 2),
        'risk_level': risk_level,
        'number_of_positions': len(investments)
    }

def format_currency(amount: float, currency: str = 'EUR') -> str:
    """
    Format currency amounts
    """
    if currency == 'EUR':
        return f"€{amount:,.2f}"
    elif currency == 'USD':
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}" 