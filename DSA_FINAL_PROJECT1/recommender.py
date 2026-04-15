import csv
import datetime
from dynamic_array import DynamicArray
from hash_map import HashMap

CSV_PATH = "new_stockData (2).csv"

def insertion_sort_by_date(arr):
    """
    Manual insertion sort - sorts (date, price) tuples by date
    O(n²) time complexity, but works for small datasets
    WHY: Avoids built-in sort() function
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Compare dates (first element of tuple)
        while j >= 0 and arr[j][0] > key[0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# ---------------------- LOAD CSV + CALCULATE CAGR ----------------------

def load_cagr_from_csv(csv_path: str):
    """Calculate CAGR from historical CSV data"""
    rows_by_symbol = HashMap()
    
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row["Stock"]
            date = datetime.date.fromisoformat(row["Date"])
            price = float(row["Close"])
            
            # Get existing list or create new DynamicArray
            if rows_by_symbol.contains(symbol):
                points = rows_by_symbol.get(symbol)
            else:
                points = DynamicArray()
                rows_by_symbol.put(symbol, points)
            
            points.append((date, price))
    
    cagr_info = HashMap()
    symbols = rows_by_symbol.keys()
    
    for i in range(len(symbols)):
        symbol = symbols[i]
        points = rows_by_symbol.get(symbol)
        
        
        points_list = []
        for j in range(len(points)):
            points_list.append(points[j])
        
        # ✅ Use manual insertion sort instead of built-in sort()
        insertion_sort_by_date(points_list)
        
        first_date, first_price = points_list[0]
        last_date, last_price = points_list[-1]
        
        years = (last_date - first_date).days / 365.25
        
        if years > 0 and first_price > 0:
            cagr = (last_price / first_price) ** (1 / years) - 1
        else:
            cagr = 0
        
        # Store as HashMap
        info = HashMap()
        info.put("cagr", cagr)
        info.put("last_price", last_price)
        cagr_info.put(symbol, info)
    
    return cagr_info


# ---------------------- MAX HEAP (PRIORITY QUEUE) ----------------------

class Node:
    """Node for priority queue"""
    def __init__(self, priority: float, payload: dict):
        self.priority = priority
        self.payload = payload


class MaxHeap:
    """Max Heap implementation for priority queue"""
    
    def __init__(self):
        self.arr = DynamicArray()  # Using custom dynamic array
    
    def push(self, node: Node):
        """Insert node into heap - O(log n)"""
        self.arr.append(node)
        self._up(len(self.arr) - 1)
    
    def pop_max(self):
        """Extract maximum element - O(log n)"""
        if self.arr.is_empty():
            return None
        
        root = self.arr[0]
        last = self.arr.pop()
        
        if not self.arr.is_empty():
            self.arr[0] = last
            self._down(0)
        
        return root
    
    def _up(self, idx: int):
        """Bubble up to maintain heap property"""
        while idx > 0:
            parent = (idx - 1) // 2
            if self.arr[idx].priority > self.arr[parent].priority:
                self.arr[idx], self.arr[parent] = self.arr[parent], self.arr[idx]
                idx = parent
            else:
                break
    
    def _down(self, i: int):
        """Bubble down to maintain heap property"""
        n = len(self.arr)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            largest = i
            
            if left < n and self.arr[left].priority > self.arr[largest].priority:
                largest = left
            if right < n and self.arr[right].priority > self.arr[largest].priority:
                largest = right
            
            if largest == i:
                break
            
            self.arr[i], self.arr[largest] = self.arr[largest], self.arr[i]
            i = largest
    
    def size(self):
        """Return heap size"""
        return len(self.arr)


# ---------------------- PREDICTION FUNCTION ----------------------

def predict_price(current_price, cagr, years=5):
    """Predict future price using CAGR"""
    return current_price * ((1 + cagr) ** years)


# ---------------------- MAIN RECOMMENDER ----------------------

def recommend_best(portfolio, cagr_info, user_amount: float, years=5, top_k=3):
    """
    Recommend best stocks using Priority Queue (Max Heap)
    
    Args:
        portfolio: StockPortfolio with real-time data
        cagr_info: Historical CAGR data (HashMap)
        user_amount: Investment amount
        years: Investment horizon
        top_k: Number of top stocks to recommend
    
    Returns:
        List of recommended stocks with profit calculations
    """
    
    heap = MaxHeap()
    
    print(f"\n📊 Analyzing stocks using Priority Queue (Max Heap)...")
    print("="*70)
    
    # Build priority queue
    # ✅ FIXED: Iterate properly over DynamicArray
    for i in range(len(portfolio.stocks)):
        stock = portfolio.stocks[i]
        symbol = stock.symbol
        
        # Skip if no real-time price
        if stock.price <= 0 or stock.error:
            print(f"⚠️  {symbol}: Skipped (no valid price)")
            continue
        
        # Get CAGR from historical data
        if not cagr_info.contains(symbol):
            print(f"⚠️  {symbol}: Skipped (no historical data)")
            continue
        
        stock_info = cagr_info.get(symbol)
        cagr = stock_info.get("cagr")
        current_price = stock.price
        
        # Predict 5-year price
        predicted_price = predict_price(current_price, cagr, years)
        profit_per_share = predicted_price - current_price
        
        # Calculate how many shares can be bought
        shares_affordable = int(user_amount // current_price)
        
        if shares_affordable == 0:
            print(f"⚠️  {symbol}: Can't afford (price: {current_price:.2f} PKR)")
            continue
        
        # Total expected profit
        total_expected_profit = profit_per_share * shares_affordable
        
        # Create payload HashMap
        payload = HashMap()
        payload.put("symbol", symbol)
        payload.put("current_price", current_price)
        payload.put("cagr", cagr)
        payload.put("predicted_price", predicted_price)
        payload.put("profit_per_share", profit_per_share)
        payload.put("shares_affordable", shares_affordable)
        payload.put("total_expected_profit", total_expected_profit)
        
        node = Node(priority=total_expected_profit, payload=payload)
        
        heap.push(node)
        print(f"✅ {symbol}: Expected profit = {total_expected_profit:,.0f} PKR")
    
    print("="*70)
    print(f"🔧 Priority Queue built with {heap.size()} stocks")
    print(f"🔝 Extracting top {top_k} recommendations...\n")
    
    # Extract top K stocks - ✅ Using DynamicArray
    results = DynamicArray()
    for i in range(min(top_k, heap.size())):
        node = heap.pop_max()
        if node:
            results.append(node.payload)
    
    return results


# ---------------------- STOCK PREDICTION MENU ----------------------

async def stock_prediction_menu(portfolio, cagr_info):
    """Stock prediction menu"""
    from yahoo_fetch import fetch_yahoo_data
    
    print("\n" + "="*70)
    print("📊 5-YEAR PROFIT PREDICTION (Priority Queue)")
    print("="*70)
    
    success = await fetch_yahoo_data(portfolio)
    
    if success == 0:
        print("❌ Could not fetch real-time data.")
        return
    
    try:
        amount = float(input("\n💰 Enter investment amount (PKR): "))
        
        if amount <= 0:
            print("❌ Amount must be positive!")
            return
        
        recs = recommend_best(
            portfolio=portfolio,
            cagr_info=cagr_info,
            user_amount=amount,
            years=5,
            top_k=3
        )
        
        print("\n" + "="*70)
        print("⭐ TOP 3 RECOMMENDED STOCKS")
        print("="*70)
        
        if len(recs) == 0:
            print("❌ No stocks available for your amount.")
        else:
            for i in range(len(recs)):
                r = recs[i]
                print(f"\n🏆 RANK {i+1}: {r.get('symbol')}")
                print(f"   Current Price:        {r.get('current_price'):>10,.2f} PKR")
                print(f"   CAGR:                 {r.get('cagr')*100:>10.2f}%")
                print(f"   Predicted 5Y Price:   {r.get('predicted_price'):>10,.2f} PKR")
                print(f"   Profit per Share:     {r.get('profit_per_share'):>10,.2f} PKR")
                print(f"   Shares Affordable:    {r.get('shares_affordable'):>10,}")
                print(f"   💰 Total Profit:       {r.get('total_expected_profit'):>10,.2f} PKR")
                print("-"*70)
            
            total = 0
            for i in range(len(recs)):
                total += recs[i].get('total_expected_profit')
            
            print(f"\n💎 Combined Profit: {total:,.2f} PKR")
            print(f"📈 ROI: {(total/amount)*100:.1f}%")
        
        print("="*70)
        print("\n⚠️  Disclaimer: Based on historical data.")
        
    except ValueError:
        print("❌ Invalid amount!")
    except Exception as e:
        print(f"❌ Error: {e}")