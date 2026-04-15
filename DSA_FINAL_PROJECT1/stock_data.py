import csv
import datetime
from dynamic_array import DynamicArray
from hash_map import HashMap


class StockData:
    """Stock data class for portfolio management"""
    
    def __init__(self, symbol, yahoo_symbol=None, sector=""):
        self.symbol = symbol  # PSX symbol (e.g., "OGDC")
        self.yahoo_symbol = yahoo_symbol or f"{symbol}.KA"  # Yahoo Finance symbol
        self.sector = sector
        self.price = 0.0
        self.volume = 0
        self.change_percent = 0.0
        self.previous_close = 0.0
        self.last_updated = None
        self.error = None
    
    def update_data(self, price, volume, change, prev_close):
        """Update stock data with real-time info"""
        self.price = price
        self.volume = volume
        self.change_percent = change
        self.previous_close = prev_close
        self.last_updated = datetime.datetime.now()
        self.error = None
    
    def set_error(self, error_msg):
        """Set error state"""
        self.error = error_msg
    
    def to_dict(self):
        result = HashMap()
        result.put("Symbol", self.symbol)
        result.put("Sector", self.sector)
        result.put("Current Price", self.price)
        result.put("Volume", self.volume)
        result.put("Change (%)", self.change_percent)
        result.put("Previous Close", self.previous_close)
        result.put("Last Updated", self.last_updated.isoformat() if self.last_updated else None)
        result.put("Error", self.error)
        return result
    
    def __repr__(self):
        return f"Stock({self.symbol}, {self.price}, {self.change_percent}%)"


class StockPortfolio:
    
    def __init__(self):
        self.stocks = DynamicArray()  # ✅ Using manual DynamicArray
    
    def add_stock(self, stock):
        """Add stock to portfolio (O(1) )"""
        self.stocks.append(stock)
    
    def get_stock(self, index):
        """Fast index access (O(1))"""
        if 0 <= index < len(self.stocks):
            return self.stocks[index]
        return None
    
    def get_stock_by_symbol(self, symbol):
        """Search stock by symbol (O(n))"""
        for i in range(len(self.stocks)):
            if self.stocks[i].symbol == symbol:
                return self.stocks[i]
        return None
    
    def get_all_stocks(self):
        """Return all stocks - FIXED: No built-in list"""
        # ✅ Return the DynamicArray directly for iteration
        return self.stocks
    
    def size(self):
        """Return number of stocks"""
        return len(self.stocks)
    
    def clear(self):
        """Clear all stocks"""
        self.stocks.clear()
    
    def to_dict_list(self):
        
        # ✅ Build result using DynamicArray
        result = DynamicArray()
        for i in range(len(self.stocks)):
            result.append(self.stocks[i].to_dict())
        return result