import requests
import time
from typing import Dict, Optional

class StockPriceService:
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_price(self, ticker: str) -> Optional[float]:
        """Get current stock price for a given ticker"""
        try:
            # Clean ticker symbol
            clean_ticker = ticker.upper().replace('.BR', '').replace('.L', '')
            
            # Map common tickers to Yahoo Finance symbols
            ticker_mapping = {
                'NKE': 'NKE',
                'BEL': 'BEL.BR',
                'BIRG': 'BIRG.L',
                'COLR': 'COLR.BR',
                # Add more mappings as needed
            }
            
            yahoo_symbol = ticker_mapping.get(clean_ticker, clean_ticker)
            
            url = f"{self.base_url}{yahoo_symbol}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'chart' in data and 'result' in data['chart']:
                    result = data['chart']['result'][0]
                    if 'meta' in result and 'regularMarketPrice' in result['meta']:
                        return float(result['meta']['regularMarketPrice'])
            
            return None
            
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            return None
    
    def get_batch_stock_prices(self, tickers: list) -> Dict[str, float]:
        """Get current prices for multiple tickers"""
        prices = {}
        
        for ticker in tickers:
            price = self.get_stock_price(ticker)
            if price is not None:
                prices[ticker] = price
            time.sleep(0.1)  # Rate limiting
        
        return prices

# Global instance
stock_price_service = StockPriceService() 