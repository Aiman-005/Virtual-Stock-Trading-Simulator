import yfinance as yf
import time

async def fetch_yahoo_data(portfolio):
    """
    Fetch real-time data for all stocks in portfolio
    Returns: number of successful fetches
    """
    print(f"\n🔄 Fetching real-time data for {portfolio.size()} stocks...")
    
    success_count = 0
    
    for i in range(portfolio.size()):
        stock = portfolio.get_stock(i)
        
        try:
            print(f"   [{i+1}/{portfolio.size()}] {stock.symbol}...", end=" ")
            
            ticker = yf.Ticker(stock.yahoo_symbol)
            hist = ticker.history(period="5d")
            
            if len(hist) >= 2:
                latest = hist.iloc[-1]
                previous = hist.iloc[-2]
                
                current_price = latest['Close']
                previous_close = previous['Close']
                volume = latest['Volume']
                percent_change = ((current_price - previous_close) / previous_close) * 100
                
                stock.update_data(
                    price=float(current_price),
                    volume=int(volume),
                    change=round(percent_change, 2),
                    prev_close=float(previous_close)
                )
                success_count += 1
                print("✅")
                
            elif len(hist) == 1:
                latest = hist.iloc[-1]
                stock.update_data(
                    price=float(latest['Close']),
                    volume=int(latest['Volume']),
                    change=0.0,
                    prev_close=float(latest['Close'])
                )
                success_count += 1
                print("⚠️")
            else:
                stock.set_error("No data")
                print("❌")
                
        except Exception as e:
            stock.set_error(str(type(e).__name__))
            print(f"❌")
        
        time.sleep(0.3)
    
    print(f"✅ Successfully fetched {success_count}/{portfolio.size()} stocks\n")
    return success_count

