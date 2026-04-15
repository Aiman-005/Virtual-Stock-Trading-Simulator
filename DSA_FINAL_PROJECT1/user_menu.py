from chatbot import ChatBot
from dummy import dummy_trading_menu
from recommender import stock_prediction_menu


async def user_main_menu(user_node, cagr_info, portfolio):
    
    while True:
        print("\n" + "="*60)
        print(f"👤 USER: {user_node.username}")
        print("="*60)
        print("1. 💬 ChatBot (Stock Recommender)")
        print("2. 🎮 Dummy Trading (Learn Trading)")
        print("3. 📊 Stock Prediction (5-Year Profit)")
        print("4. 🚪 Logout")
        print("="*60)
        
        choice = input("Enter your choice (1-4): ")
        
        # ChatBot
        if choice == "1":
            try:
                bot = ChatBot()
                await bot.start()
            except Exception as e:
                print(f"❌ ChatBot error: {e}")
        
        # Dummy Trading
        elif choice == "2":
             await dummy_trading_menu(user_node, portfolio)
        
        # Stock Prediction
        elif choice == "3":
            await stock_prediction_menu(portfolio, cagr_info)
        
        # Logout
        elif choice == "4":
            print(f"\n👋 Goodbye, {user_node.username}!")
            break
        
        else:
            print("❌ Invalid choice.")