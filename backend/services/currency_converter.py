import requests
import time
from typing import Optional, Tuple
from datetime import datetime, timedelta

# Cache for exchange rates to avoid too many API calls
_exchange_rate_cache = {}
_cache_duration = timedelta(hours=1)  # Cache for 1 hour

def clear_cache():
    """Clear the exchange rate cache"""
    global _exchange_rate_cache
    _exchange_rate_cache = {}

def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """
    Get exchange rate between two currencies
    """
    if from_currency == to_currency:
        return 1.0
    
    cache_key = f"{from_currency}_{to_currency}"
    current_time = datetime.now()
    
    # Check cache first
    if cache_key in _exchange_rate_cache:
        cached_rate, cached_time = _exchange_rate_cache[cache_key]
        if current_time - cached_time < _cache_duration:
            return cached_rate
    
    # Try multiple sources for exchange rate
    sources = [
        _try_exchange_rate_api,
        _try_fixer_api,
        _try_currency_api
    ]
    
    for source in sources:
        try:
            rate = source(from_currency, to_currency)
            if rate and rate > 0:
                # Cache the result
                _exchange_rate_cache[cache_key] = (rate, current_time)
                return rate
        except Exception as e:
            print(f"Exchange rate source {source.__name__} failed: {e}")
            continue
    
    # Fallback to hardcoded rates for common currencies
    fallback_rate = _get_fallback_rate(from_currency, to_currency)
    if fallback_rate:
        return fallback_rate
    
    # If no fallback rate is available, return 1.0 to avoid NaN
    print(f"Warning: No exchange rate available for {from_currency} to {to_currency}, using 1.0")
    return 1.0

def _try_exchange_rate_api(from_currency: str, to_currency: str) -> Optional[float]:
    """Try Exchange Rate API (free tier)"""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'rates' in data and to_currency in data['rates']:
            return float(data['rates'][to_currency])
        
        return None
    except Exception as e:
        raise Exception(f"Exchange Rate API error: {str(e)}")

def _try_fixer_api(from_currency: str, to_currency: str) -> Optional[float]:
    """Try Fixer API (free tier)"""
    try:
        # Using a demo API key - in production you'd want your own
        api_key = "demo"
        url = f"http://data.fixer.io/api/latest?access_key={api_key}&base={from_currency}&symbols={to_currency}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('success') and 'rates' in data and to_currency in data['rates']:
            return float(data['rates'][to_currency])
        
        return None
    except Exception as e:
        raise Exception(f"Fixer API error: {str(e)}")

def _try_currency_api(from_currency: str, to_currency: str) -> Optional[float]:
    """Try Currency API (free tier)"""
    try:
        url = f"https://api.currencyapi.com/v3/latest?apikey=demo&base_currency={from_currency}&currencies={to_currency}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'data' in data and to_currency in data['data']:
            return float(data['data'][to_currency]['value'])
        
        return None
    except Exception as e:
        raise Exception(f"Currency API error: {str(e)}")

def _get_fallback_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """Get fallback exchange rates for common currencies"""
    # Common exchange rates (approximate, should be updated regularly)
    fallback_rates = {
        'USD_EUR': 0.85,  # 1 USD = 0.85 EUR (approximate)
        'EUR_USD': 1.18,  # 1 EUR = 1.18 USD (approximate)
        'GBP_EUR': 1.17,  # 1 GBP = 1.17 EUR (approximate)
        'EUR_GBP': 0.85,  # 1 EUR = 0.85 GBP (approximate)
        'CHF_EUR': 0.92,  # 1 CHF = 0.92 EUR (approximate)
        'EUR_CHF': 1.09,  # 1 EUR = 1.09 CHF (approximate)
    }
    
    key = f"{from_currency}_{to_currency}"
    return fallback_rates.get(key)

def detect_currency_from_ticker(ticker: str) -> str:
    """
    Detect the currency based on ticker symbol
    """
    ticker = ticker.upper()
    
    # European exchanges typically trade in EUR
    european_suffixes = ['.AS', '.BR', '.DE', '.PA', '.SW', '.MC', '.IE', '.CO', '.VI']
    for suffix in european_suffixes:
        if ticker.endswith(suffix):
            return 'EUR'
    
    # Some London stocks trade in EUR (like BIRG.L)
    eur_london_stocks = ['BIRG.L', 'SMT.L', 'FCIT.L']  # Add more as needed
    if ticker in eur_london_stocks:
        return 'EUR'
    
    # London exchange typically trades in GBP
    if ticker.endswith('.L'):
        return 'GBP'
    
    # Swiss exchange typically trades in CHF
    if ticker.endswith('.SW'):
        return 'CHF'
    
    # US stocks (no suffix or common US suffixes)
    us_suffixes = ['.US', '.O', '.N', '.A', '.B']
    if not any(ticker.endswith(suffix) for suffix in ['.AS', '.BR', '.DE', '.PA', '.SW', '.MC', '.IE', '.CO', '.VI', '.L']):
        return 'USD'
    
    # Default to USD for unknown
    return 'USD'

def convert_price_to_eur(price: float, from_currency: str) -> float:
    """
    Convert a price from any currency to EUR
    """
    if from_currency == 'EUR':
        return price
    
    exchange_rate = get_exchange_rate(from_currency, 'EUR')
    if exchange_rate and exchange_rate > 0:
        return price * exchange_rate
    
    # If conversion fails, return original price
    print(f"Warning: Could not convert {price} {from_currency} to EUR, returning original price")
    return price

def get_price_with_currency_conversion(ticker: str, original_price: float) -> Tuple[float, str]:
    """
    Get the price converted to EUR if needed, along with the original currency
    """
    detected_currency = detect_currency_from_ticker(ticker)
    
    if detected_currency == 'EUR':
        return original_price, 'EUR'
    else:
        converted_price = convert_price_to_eur(original_price, detected_currency)
        return converted_price, detected_currency 