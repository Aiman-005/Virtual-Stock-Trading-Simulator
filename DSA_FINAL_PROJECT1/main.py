import asyncio
from authentication import UserLinkedList, signup, login
from user_menu import user_main_menu
from recommender import load_cagr_from_csv
from stock_data import StockPortfolio, StockData
from user_storage import UserStorage


async def main():
    print("\n" + "="*60)
    print("🚀 STOCK INVESTMENT SYSTEM")
    print("="*60)
    
    # Initialize user system (Linked List)
    user_list = UserLinkedList()
    
    # Initialize storage (creates UserStorage instance)
    storage = UserStorage()
    
    # Load existing users from files
    loaded_count = storage.load_all_users(user_list)
    if loaded_count > 0:
        print(f"✅ Loaded {loaded_count} existing user(s)")
    
    # Load historical data
    try:
        cagr_info = load_cagr_from_csv("new_stockData (2).csv")
        print(f"✅ Loaded CAGR data for {len(cagr_info)} stocks")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Initialize stock portfolio
    symbols_config = [
        ("OGDC", "OGDC.KA", "Oil & Gas"),
        ("HBL", "HBL.KA", "Banking"),
        ("PSO", "PSO.KA", "Oil Marketing"),
        ("LUCK", "LUCK.KA", "Cement"),
        ("MCB", "MCB.KA", "Banking"),
        ("MARI", "MARI.KA", "Oil & Gas"),
        ("TRG", "TRG.KA", "Technology"),
        ("SYS", "SYS.KA", "Technology"),
        ("SEARL", "SEARL.KA", "Textiles"),
        ("FFC", "FFC.KA", "Fertilizer")
    ]
    
    portfolio = StockPortfolio()
    for symbol, yahoo_symbol, sector in symbols_config:
        portfolio.add_stock(StockData(symbol, yahoo_symbol, sector))
    
    print(f"✅ Portfolio initialized with {portfolio.size()} stocks\n")
    
    # Main authentication loop
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. 📝 Sign Up (New User)")
        print("2. 🔐 Log In (Existing User)")
        print("3. 🚪 Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            user = signup(user_list, storage)
            if user:
                input("\nPress Enter to continue...")
                await user_main_menu(user, cagr_info, portfolio)
                # Save user data after logout
                storage.update_user(user)
        
        elif choice == "2":
            user = login(user_list)
            if user:
                input("\nPress Enter to continue...")
                await user_main_menu(user, cagr_info, portfolio)
                # Save user data after logout
                storage.update_user(user)
        
        elif choice == "3":
            print("\n" + "="*60)
            print("👋 Thank you for using Stock Investment System!")
            print("="*60)
            break
        
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()