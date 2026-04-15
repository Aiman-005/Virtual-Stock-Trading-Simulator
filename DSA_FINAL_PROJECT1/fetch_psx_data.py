#fetch_psx_data
import json
import os
import time
import datetime

class StockData:
    """Dynamic array/vector to store stock information with fast index access"""
    
    def __init__(self, symbol, yahoo_symbol, sector=""):
        self.symbol = symbol          # PSX symbol
        self.yahoo_symbol = yahoo_symbol  # Yahoo Finance symbol
        self.sector = sector          # Stock sector
        self.price = 0.0              # Current price
        self.volume = 0               # Trading volume
        self.change_percent = 0.0     # Percentage change
        self.previous_close = 0.0     # Previous closing price
        self.last_updated = None      # Last update timestamp
        self.error = None             # Error message if any
    
    def update_data(self, price, volume, change, prev_close):
        """Update stock data"""
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
        """Convert to dictionary for JSON serialization"""
        return {
            "Symbol": self.symbol,
            "Sector": self.sector,
            "Current Price": self.price,
            "Volume": self.volume,
            "Change (%)": self.change_percent,
            "Previous Close": self.previous_close,
            "Last Updated": self.last_updated.isoformat() if self.last_updated else None,
            "Error": self.error
        }
    
    def __repr__(self):
        return f"Stock({self.symbol}, {self.price}, {self.change_percent}%)"


class StockPortfolio:
    """Dynamic array/vector container for managing multiple stocks"""
    
    def __init__(self):
        self.stocks = []  # Dynamic array (Python list acts as vector)
    
    def add_stock(self, stock):
        """Add stock to portfolio (O(1) amortized)"""
        self.stocks.append(stock)
    
    def get_stock(self, index):
        """Fast index access to stock (O(1))"""
        if 0 <= index < len(self.stocks):
            return self.stocks[index]
        return None
    
    def get_stock_by_symbol(self, symbol):
        """Search stock by symbol (O(n))"""
        for stock in self.stocks:
            if stock.symbol == symbol:
                return stock
        return None
    
    def get_all_stocks(self):
        """Return all stocks (O(1))"""
        return self.stocks
    
    def size(self):
        """Return number of stocks (O(1))"""
        return len(self.stocks)
    
    def clear(self):
        """Clear all stocks (O(1))"""
        self.stocks.clear()
    
    def to_dict_list(self):
        """Convert all stocks to list of dictionaries"""
        return [stock.to_dict() for stock in self.stocks]


# ============================================================================
# STOCK PORTFOLIO - Top 10 KSE-100 Stocks
# UBL replaced with MARI (Mari Petroleum) - more reliable on Yahoo Finance
# ============================================================================

def initialize_portfolio():
    """Initialize stock portfolio with KSE-100 stocks"""
    portfolio = StockPortfolio()
    
    # Add stocks with their Yahoo Finance symbols and sectors
    stocks_config = [
        ("OGDC", "OGDC.KA", "Oil & Gas"),
        ("HBL", "HBL.KA", "Banking"),
        ("PSO", "PSO.KA", "Oil Marketing"),
        ("LUCK", "LUCK.KA", "Cement"),
        ("MCB", "MCB.KA", "Banking"),
        ("MARI", "MARI.KA", "Oil & Gas"),  # Replaced UBL
        ("TRG", "TRG.KA", "Technology"),
        ("SYS", "SYS.KA", "Technology"),
        ("SEARL", "SEARL.KA", "Textiles"),
        ("FFC", "FFC.KA", "Fertilizer")
    ]
    
    for symbol, yahoo_symbol, sector in stocks_config:
        stock = StockData(symbol, yahoo_symbol, sector)
        portfolio.add_stock(stock)
    
    return portfolio


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def check_yfinance():
    """Check if yfinance is installed"""
    try:
        import yfinance as yf
        print("✅ yfinance is installed")
        return True
    except ImportError:
        print("❌ yfinance is NOT installed!")
        print("\n📦 Please install it:")
        print("   pip install yfinance")
        input("\nPress Enter to exit...")
        return False


def fetch_yahoo_data(portfolio):
    """Fetch data from Yahoo Finance for all stocks in portfolio"""
    import yfinance as yf
    
    print(f"🔄 Fetching data for {portfolio.size()} stocks from Yahoo Finance...")
    
    success_count = 0
    
    # Iterate through portfolio using index access (demonstrating fast access)
    for i in range(portfolio.size()):
        stock = portfolio.get_stock(i)  # O(1) index access
        
        try:
            print(f"   [{i+1}/{portfolio.size()}] Downloading {stock.symbol}...", end=" ")
            
            ticker = yf.Ticker(stock.yahoo_symbol)
            
            # Get historical data (last 5 days)
            hist = ticker.history(period="5d")
            
            if len(hist) >= 2:
                # Get latest and previous day
                latest = hist.iloc[-1]
                previous = hist.iloc[-2]
                
                current_price = latest['Close']
                previous_close = previous['Close']
                volume = latest['Volume']
                
                # Calculate percentage change
                percent_change = ((current_price - previous_close) / previous_close) * 100
                
                # Update stock data in portfolio
                stock.update_data(
                    price=float(current_price),
                    volume=int(volume),
                    change=round(percent_change, 2),
                    prev_close=float(previous_close)
                )
                success_count += 1
                print("✅")
                
            elif len(hist) == 1:
                # Only one day of data
                latest = hist.iloc[-1]
                stock.update_data(
                    price=float(latest['Close']),
                    volume=int(latest['Volume']),
                    change=0.0,
                    prev_close=float(latest['Close'])
                )
                success_count += 1
                print("⚠️ (limited data)")
            else:
                stock.set_error("No data available")
                print("❌")
                
        except Exception as e:
            stock.set_error(str(type(e).__name__))
            print(f"❌ ({type(e).__name__})")
        
        time.sleep(0.3)  # Small delay between requests
    
    print(f"\n✅ Successfully fetched {success_count}/{portfolio.size()} stocks\n")
    return success_count > 0


def display_data(portfolio):
    """Display stock data in formatted table"""
    
    print("\n" + "=" * 90)
    print("📈  PSX (KSE-100) STOCK DATA - Yahoo Finance")
    print(f"    Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"    Total Stocks: {portfolio.size()}")
    print("=" * 90)
    print(f"{'#':<4} {'Symbol':<8} {'Sector':<15} {'Price (PKR)':>13} {'Volume':>15} {'Change':>18}")
    print("-" * 90)
    
    success_count = 0
    
    # Display using index access (demonstrating vector-like behavior)
    for i in range(portfolio.size()):
        stock = portfolio.get_stock(i)  # Fast O(1) index access
        
        if stock.error:
            print(f"{i+1:<4} {stock.symbol:<8} {stock.sector:<15} {'-':>13} {'-':>15} {stock.error:>18}")
        else:
            success_count += 1
            change = stock.change_percent
            change_str = f"{change:+.2f}%"
            
            # Color indicators
            if change > 0:
                indicator = "🟢"
            elif change < 0:
                indicator = "🔴"
            else:
                indicator = "⚪"
            
            print(f"{i+1:<4} {stock.symbol:<8} {stock.sector:<15} {stock.price:>13,.2f} "
                  f"{stock.volume:>15,} {indicator} {change_str:>15}")
    
    print("=" * 90)
    print(f"✅ Successfully loaded {success_count}/{portfolio.size()} stocks")
    
    if success_count == 0:
        print("\n⚠️  No data available. Possible reasons:")
        print("   • Markets are closed (Trading: Mon-Fri, 9:15 AM - 3:30 PM PKT)")
        print("   • Weekend or public holiday")
        print("   • Internet connection issues")
    
    print("\n⏱️  Next update in 30 seconds... (Press Ctrl+C to stop)")
    print()
    
    # Save to JSON
    save_to_json(portfolio)


def save_to_json(portfolio):
    """Save portfolio data to JSON file"""
    try:
        file_path = os.path.join(os.getcwd(), "psx_stock_data.json")
        
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_stocks": portfolio.size(),
            "stocks": portfolio.to_dict_list()
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print(f"💾 Data saved to: {file_path}")
    except Exception as e:
        print(f"⚠️  Could not save JSON: {e}")


def main():
    """Main loop"""
    print("\n" + "="*70)
    print("🚀 PSX STOCK MONITOR (Yahoo Finance)")
    print("   Using Dynamic Array/Vector for Stock Storage")
    print("="*70 + "\n")
    
    # Check if yfinance is installed
    if not check_yfinance():
        return
    
    # Initialize portfolio (dynamic array)
    portfolio = initialize_portfolio()
    print(f"📊 Initialized portfolio with {portfolio.size()} stocks")
    print(f"   Storage: Dynamic Array (Vector) with O(1) index access\n")
    
    print("⏳ First fetch may take 10-20 seconds...\n")
    time.sleep(2)
    
    retry_count = 0
    max_retries = 3
    
    try:
        while True:
            try:
                # Fetch data for all stocks in portfolio
                success = fetch_yahoo_data(portfolio)
                
                if success:
                    clear_screen()
                    display_data(portfolio)
                    retry_count = 0
                    time.sleep(30)
                else:
                    retry_count += 1
                    print(f"\n⚠️  No data retrieved (attempt {retry_count}/{max_retries})")
                    
                    if retry_count >= max_retries:
                        print("\n❌ Multiple failures. Possible issues:")
                        print("   • Yahoo Finance may be blocking requests")
                        print("   • Markets are closed")
                        print("   • Internet connection problems")
                        print("\n   Continuing to retry every 60 seconds...")
                        time.sleep(60)
                        retry_count = 0
                    else:
                        print(f"   Retrying in 15 seconds...")
                        time.sleep(15)
                    
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                import traceback
                traceback.print_exc()
                print("\nRetrying in 30 seconds...")
                time.sleep(30)
            
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + "="*70)
        print("👋 PSX Stock Monitor stopped!")
        print(f"📄 Latest data saved in: psx_stock_data.json")
        print(f"📊 Total stocks monitored: {portfolio.size()}")
        print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

