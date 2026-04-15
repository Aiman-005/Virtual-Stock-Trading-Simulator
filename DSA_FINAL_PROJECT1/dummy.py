
from dynamic_array import DynamicArray


class Action:
    """Action class for undo/redo"""
    def __init__(self, action_type, symbol=None, quantity=None, amount=None):
        self.action_type = action_type
        self.symbol = symbol
        self.quantity = quantity
        self.amount = amount


class DummyTrader:

    class Stack:
        def __init__(self):
            self.data = DynamicArray()
        
        def push(self, value):
            """Push item onto stack - O(1)"""
            self.data.append(value)
        
        def pop(self):
            """Pop item from stack - O(1)"""
            if not self.is_empty():
                return self.data.pop()
            return None
        
        def peek(self):
            """View top item without removing - O(1)"""
            if not self.is_empty():
                return self.data[len(self.data) - 1]
            return None
        
        def is_empty(self):
            """Check if stack is empty - O(1)"""
            return len(self.data) == 0
        
        def size(self):
            """Return number of items - O(1)"""
            return len(self.data)
        
        def clear(self):
            """Clear all items - O(1)"""
            self.data.clear()
    
    def __init__(self, user_node):
        self.user = user_node
        # Initialize stacks if they don't exist
        if not hasattr(self.user, 'undo_stack') or not isinstance(self.user.undo_stack, DummyTrader.Stack):
            self.user.undo_stack = DummyTrader.Stack()
        if not hasattr(self.user, 'redo_stack') or not isinstance(self.user.redo_stack, DummyTrader.Stack):
            self.user.redo_stack = DummyTrader.Stack()
    
    def buy(self, symbol, qty, price):
        cost = qty * price
        if self.user.dummy_balance < cost:
            print("❌ Not enough balance!")
            return
        
        self.user.dummy_balance -= cost
        self.user.dummy_portfolio[symbol] = self.user.dummy_portfolio.get(symbol, 0) + qty
        
        # Save to undo stack
        self.user.undo_stack.push(Action("buy", symbol, qty, cost))
        self.user.redo_stack.clear()
        print(f"✅ Bought {qty} shares of {symbol} for PKR {cost:,.2f}")
    
    def sell(self, symbol, qty, price):
        if self.user.dummy_portfolio.get(symbol, 0) < qty:
            print("❌ Not enough shares!")
            return
        
        revenue = qty * price
        self.user.dummy_balance += revenue
        self.user.dummy_portfolio[symbol] = self.user.dummy_portfolio.get(symbol, 0) - qty
        
        # FIXED: Use remove() instead of del for HashMap
        if self.user.dummy_portfolio[symbol] == 0:
            self.user.dummy_portfolio.remove(action.symbol)
        
        self.user.undo_stack.push(Action("sell", symbol, qty, revenue))
        self.user.redo_stack.clear()
        print(f"✅ Sold {qty} shares of {symbol} for PKR {revenue:,.2f}")
    
    def deposit(self, amount):
        self.user.dummy_balance += amount
        self.user.undo_stack.push(Action("deposit", amount=amount))
        self.user.redo_stack.clear()
        print(f"✅ Deposited PKR {amount:,.2f}")
    
    def withdraw(self, amount):
        if self.user.dummy_balance < amount:
            print("❌ Not enough balance!")
            return
        
        self.user.dummy_balance -= amount
        self.user.undo_stack.push(Action("withdraw", amount=amount))
        self.user.redo_stack.clear()
        print(f"✅ Withdrew PKR {amount:,.2f}")
    
    def undo(self):
        if self.user.undo_stack.is_empty():
            print("❌ Nothing to undo.")
            return
        
        action = self.user.undo_stack.pop()
        
        if action.action_type == "buy":
            self.user.dummy_balance += action.amount
            self.user.dummy_portfolio[action.symbol] = self.user.dummy_portfolio.get(action.symbol, 0) - action.quantity
            
            # FIXED: Use remove() instead of del for HashMap
            if self.user.dummy_portfolio[action.symbol] == 0:
                self.user.dummy_portfolio.remove(action.symbol)
        
        elif action.action_type == "sell":
            self.user.dummy_balance -= action.amount
            self.user.dummy_portfolio[action.symbol] = self.user.dummy_portfolio.get(action.symbol, 0) + action.quantity
        
        elif action.action_type == "deposit":
            self.user.dummy_balance -= action.amount
        
        elif action.action_type == "withdraw":
            self.user.dummy_balance += action.amount
        
        self.user.redo_stack.push(action)
        print(f"↩  Undo: {action.action_type}")
    
    def redo(self):
        if self.user.redo_stack.is_empty():
            print("❌ Nothing to redo.")
            return
        
        action = self.user.redo_stack.pop()
        
        if action.action_type == "buy":
            self.user.dummy_balance -= action.amount
            self.user.dummy_portfolio[action.symbol] = self.user.dummy_portfolio.get(action.symbol, 0) + action.quantity
        
        elif action.action_type == "sell":
            # FIXED: Use .get() and remove() for HashMap compatibility
            self.user.dummy_balance += action.amount
            current_qty = self.user.dummy_portfolio.get(action.symbol, 0)
            self.user.dummy_portfolio[action.symbol] = current_qty - action.quantity
            
            # FIXED: Use remove() instead of del for HashMap
            if self.user.dummy_portfolio[action.symbol] <= 0:
                self.user.dummy_portfolio.remove(action.symbol)
        
        elif action.action_type == "deposit":
            self.user.dummy_balance += action.amount
        
        elif action.action_type == "withdraw":
            self.user.dummy_balance -= action.amount
        
        self.user.undo_stack.push(action)
        print(f"↪  Redo: {action.action_type}")
    
    def show_portfolio(self):
        print("\n" + "="*60)
        print(f"💼 {self.user.username}'s Portfolio")
        print("="*60)
        print(f"💰 Balance: PKR {self.user.dummy_balance:,.2f}")
        print(f"📊 Holdings:")
        
        # FIXED: Use HashMap's items() method which returns DynamicArray of tuples
        if self.user.dummy_portfolio and len(self.user.dummy_portfolio) > 0:
            items = self.user.dummy_portfolio.items()
            for i in range(len(items)):
                symbol, qty = items[i]
                print(f"   {symbol}: {qty} shares")
        else:
            print("   (No holdings)")
        print("="*60)



def display_available_stocks(portfolio):
    """Display all available stocks with current prices"""
    print("\n" + "="*80)
    print("📊 AVAILABLE STOCKS FOR TRADING")
    print("="*80)
    print(f"{'#':<4} {'Symbol':<10} {'Sector':<15} {'Price (PKR)':>15} {'Change':>12} {'Status':<15}")
    print("-"*80)
    
    available_count = 0
    
    for i in range(portfolio.size()):
        stock = portfolio.get_stock(i)
        
        if stock.error or stock.price <= 0:
            status = "❌ Not Available"
            price_str = "-"
            change_str = "-"
        else:
            available_count += 1
            status = "✅ Available"
            price_str = f"{stock.price:,.2f}"
            
            change = stock.change_percent
            if change > 0:
                change_str = f"🟢 +{change:.2f}%"
            elif change < 0:
                change_str = f"🔴 {change:.2f}%"
            else:
                change_str = f"⚪ {change:.2f}%"
        
        print(f"{i+1:<4} {stock.symbol:<10} {stock.sector:<15} {price_str:>15} {change_str:>12} {status:<15}")
    
    print("="*80)
    print(f"📈 {available_count}/{portfolio.size()} stocks available for trading")
    print("="*80)


async def dummy_trading_menu(user_node, portfolio):
    
    trader = DummyTrader(user_node)
    
    # Fetch latest prices on first load
    print("\n🔄 Fetching latest stock prices...")
    try:
        from yahoo_fetch import fetch_yahoo_data
        await fetch_yahoo_data(portfolio)
    except Exception as e:
        print(f"⚠  Could not fetch latest prices: {e}")
        print("Using cached prices (may be outdated)")
    
    while True:
        print("\n" + "="*60)
        print("💼 DUMMY TRADING MENU")
        print("="*60)
        print("1.  View Available Stocks")
        print("2.  Refresh Stock Prices")
        print("3.  Buy Stock")
        print("4.  Sell Stock")
        print("5.  Deposit Money")
        print("6.  Withdraw Money")
        print("7.  Undo Last Action")
        print("8.  Redo Last Action")
        print("9.  Show My Portfolio")
        print("10. Back to Main Menu")
        print("="*60)
        
        op = input("Choose an option (1-10): ")
        
        # View available stocks
        if op == "1":
            display_available_stocks(portfolio)
            input("\n📌 Press Enter to continue...")
        
        # Refresh prices
        elif op == "2":
            print("\n🔄 Refreshing stock prices...")
            try:
                from yahoo_fetch import fetch_yahoo_data
                success = await fetch_yahoo_data(portfolio)
                if success > 0:
                    print(f"✅ Updated {success} stocks")
                    display_available_stocks(portfolio)
                else:
                    print("❌ Could not fetch new prices")
            except Exception as e:
                print(f"❌ Error: {e}")
            input("\n📌 Press Enter to continue...")
        
        # Buy stock
        elif op == "3":
            display_available_stocks(portfolio)
            
            symbol = input("\n📈 Enter stock symbol (e.g., OGDC): ").upper()
            
            # Find stock in portfolio
            stock = portfolio.get_stock_by_symbol(symbol)
            
            if not stock:
                print(f"❌ Stock '{symbol}' not found in our list!")
                input("📌 Press Enter to continue...")
                continue
            
            if stock.error or stock.price <= 0:
                print(f"❌ '{symbol}' is not available for trading right now!")
                input("📌 Press Enter to continue...")
                continue
            
            # Show stock details
            print(f"\n{'='*60}")
            print(f"📊 Stock Details: {symbol}")
            print(f"{'='*60}")
            print(f"Current Price: PKR {stock.price:,.2f}")
            print(f"Change: {stock.change_percent:+.2f}%")
            print(f"Sector: {stock.sector}")
            print(f"Your Balance: PKR {user_node.dummy_balance:,.2f}")
            print(f"Max Affordable: {int(user_node.dummy_balance // stock.price)} shares")
            print(f"{'='*60}")
            
            try:
                qty = int(input("Enter quantity to buy: "))
                
                if qty <= 0:
                    print("❌ Quantity must be positive!")
                    continue
                
                # Calculate cost
                total_cost = qty * stock.price
                print(f"\n💰 Total Cost: PKR {total_cost:,.2f}")
                
                confirm = input("Confirm purchase? (y/n): ").lower()
                if confirm == 'y':
                    trader.buy(symbol, qty, stock.price)
                else:
                    print("❌ Purchase cancelled")
                    
            except ValueError:
                print("❌ Invalid quantity!")
            
            input("\n📌 Press Enter to continue...")
        
        # Sell stock
        elif op == "4":
            # Show user's current holdings
            print("\n" + "="*60)
            print("💼 YOUR CURRENT HOLDINGS")
            print("="*60)
            
            # FIXED: Use HashMap's methods
            if not user_node.dummy_portfolio or len(user_node.dummy_portfolio) == 0:
                print("❌ You don't own any stocks yet!")
                input("\n📌 Press Enter to continue...")
                continue
            
            # Display holdings with current prices
            holdings_found = False
            keys = user_node.dummy_portfolio.keys()
            
            for i in range(len(keys)):
                symbol = keys[i]
                qty = user_node.dummy_portfolio.get(symbol)
                
                # Get current price
                stock = portfolio.get_stock_by_symbol(symbol)
                if stock and stock.price > 0:
                    current_value = qty * stock.price
                    print(f"  {symbol}: {qty} shares @ PKR {stock.price:,.2f} = PKR {current_value:,.2f}")
                    holdings_found = True
                else:
                    print(f"  {symbol}: {qty} shares (price unavailable)")
            
            if not holdings_found:
                print("❌ No valid holdings found!")
                input("\n📌 Press Enter to continue...")
                continue
            
            print("="*60)
            
            symbol = input("\n📉 Enter stock symbol to sell: ").upper()
            
            if not user_node.dummy_portfolio.contains(symbol):
                print(f"❌ You don't own any {symbol} shares!")
                input("📌 Press Enter to continue...")
                continue
            
            owned_qty = user_node.dummy_portfolio.get(symbol)
            stock = portfolio.get_stock_by_symbol(symbol)
            
            if not stock or stock.price <= 0:
                print(f"❌ Cannot get current price for {symbol}")
                input("📌 Press Enter to continue...")
                continue
            
            # Show details
            print(f"\n{'='*60}")
            print(f"📊 Stock Details: {symbol}")
            print(f"{'='*60}")
            print(f"Shares Owned: {owned_qty}")
            print(f"Current Price: PKR {stock.price:,.2f}")
            print(f"Total Value: PKR {owned_qty * stock.price:,.2f}")
            print(f"{'='*60}")
            
            try:
                qty = int(input(f"Enter quantity to sell (max {owned_qty}): "))
                
                if qty <= 0:
                    print("❌ Quantity must be positive!")
                    continue
                
                if qty > owned_qty:
                    print(f"❌ You only own {owned_qty} shares!")
                    continue
                
                revenue = qty * stock.price
                print(f"\n💰 You will receive: PKR {revenue:,.2f}")
                
                confirm = input("Confirm sale? (y/n): ").lower()
                if confirm == 'y':
                    trader.sell(symbol, qty, stock.price)
                else:
                    print("❌ Sale cancelled")
                    
            except ValueError:
                print("❌ Invalid quantity!")
            
            input("\n📌 Press Enter to continue...")
        
        # Deposit money
        elif op == "5":
            try:
                amt = float(input("💵 Enter amount to deposit: "))
                if amt <= 0:
                    print("❌ Amount must be positive!")
                else:
                    trader.deposit(amt)
            except ValueError:
                print("❌ Invalid amount!")
            input("\n📌 Press Enter to continue...")
        
        # Withdraw money
        elif op == "6":
            print(f"\n💰 Current Balance: PKR {user_node.dummy_balance:,.2f}")
            try:
                amt = float(input("Enter amount to withdraw: "))
                if amt <= 0:
                    print("❌ Amount must be positive!")
                else:
                    trader.withdraw(amt)
            except ValueError:
                print("❌ Invalid amount!")
            input("\n📌 Press Enter to continue...")
        
        # Undo
        elif op == "7":
            trader.undo()
            input("\n📌 Press Enter to continue...")
        
        # Redo
        elif op == "8":
            trader.redo()
            input("\n📌 Press Enter to continue...")
        
        # Show portfolio
        elif op == "9":
            trader.show_portfolio()
            
            # Calculate total portfolio value
            total_value = user_node.dummy_balance
            print(f"\n📊 Portfolio Value Breakdown:")
            print(f"{'='*60}")
            
            # FIXED: Use HashMap's methods
            if user_node.dummy_portfolio and len(user_node.dummy_portfolio) > 0:
                keys = user_node.dummy_portfolio.keys()
                
                for i in range(len(keys)):
                    symbol = keys[i]
                    qty = user_node.dummy_portfolio.get(symbol)
                    
                    stock = portfolio.get_stock_by_symbol(symbol)
                    if stock and stock.price > 0:
                        value = qty * stock.price
                        total_value += value
                        print(f"  {symbol}: {qty} × PKR {stock.price:,.2f} = PKR {value:,.2f}")
            
            print(f"{'='*60}")
            print(f"💼 Total Portfolio Value: PKR {total_value:,.2f}")
            print(f"{'='*60}")
            
            input("\n📌 Press Enter to continue...")
        
        # Back to main menu
        elif op == "10":
            print("\n✅ Returning to main menu...")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1-10")
            input("\n📌 Press Enter to continue...")