#!/usr/bin/env python3
"""
Test currency detection and conversion for BIRG.L
"""
from services.currency_converter import detect_currency_from_ticker, convert_price_to_eur, get_exchange_rate
from services.finance_api import get_current_price

def test_birg_currency():
    ticker = "BIRG.L"
    
    print(f"Testing currency for {ticker}")
    print("=" * 50)
    
    # Test currency detection
    detected_currency = detect_currency_from_ticker(ticker)
    print(f"Detected currency: {detected_currency}")
    
    # Test exchange rate
    if detected_currency != 'EUR':
        rate = get_exchange_rate(detected_currency, 'EUR')
        print(f"Exchange rate {detected_currency} to EUR: {rate}")
    
    # Test price conversion
    test_price = 12.20  # Example GBP price
    converted_price = convert_price_to_eur(test_price, detected_currency)
    print(f"Original price: {test_price} {detected_currency}")
    print(f"Converted price: {converted_price:.2f} EUR")
    
    # Test actual price from API
    try:
        converted_price, original_price, original_currency = get_current_price(ticker)
        print(f"\nActual API result:")
        print(f"Original price: {original_price} {original_currency}")
        print(f"Converted price: {converted_price:.2f} EUR")
    except Exception as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    test_birg_currency() 