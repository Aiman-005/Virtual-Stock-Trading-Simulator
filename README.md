# 📈 Virtual Stock Trading Simulator

A feature rich stock market assistant system built in **Python** as part of the Data Structures & Algorithms course at FAST-NUCES Karachi. The system integrates real-time APIs, 5 custom-built data structures from scratch, and a Gemini AI-powered chatbot.

---

## About

This project applies DSA concepts in a real world financial context, users can trade PSX stocks with virtual money, get AI-powered stock advice, and predict 5 year profits using CAGR analysis. Every major data structure (Dynamic Array, HashMap, LinkedList, Stack, Priority Queue) was implemented from scratch without using built-in Python libraries.

---

## Features

### 🔐 User Authentication
- Signup / Login with secure password hashing
- Per user file-based persistent storage under `users_data/`
- Password masking during input

### 📊 Stock Data
- Fetches **real-time PSX stock data** (OGDC, HBL, PSO, LUCK, MCB, MARI, TRG, SYS, SEARL, FFC)
- Displays live price, sector, and % change per stock
- Data parsed from JSON/CSV using custom Dynamic Array and HashMap

### 🤖 AI Chatbot (Gemini API)
- Answers financial and stock-related questions in natural language
- No keyword matching — understands user intent via Gemini API
- Provides PSX-specific investment guidance

### 💹 Dummy Trading System
- Buy and sell PSX stocks with virtual PKR balance
- Deposit and withdraw money
- View full portfolio breakdown with current market value
- **Undo last action** (Stack-based): reverses buy, sell, deposit, withdraw
- **Redo last action** :re-applies the undone action

### 🔮 Stock Prediction (5-Year Profit)
- Enter investment amount and get top 3 recommended stocks
- Uses **Priority Queue (Max Heap)** to rank stocks by expected profit
- Calculates predicted price using CAGR (Compound Annual Growth Rate)
- Shows profit per share, shares affordable, and total profit

---

## Data Structures Implemented from Scratch

| Data Structure | Where Used | Why |
|---------------|-----------|-----|
| **Dynamic Array** | Storing stock datasets, user history, recommendations | O(1) access, auto-resizing for variable dataset sizes |
| **HashMap** | Stock symbol → price lookup | O(1) average lookup, avoids slow linear searches |
| **LinkedList** | Recent user actions, dynamic updates | O(1) insert/delete for frequently changing sequences |
| **Stack** | Undo/Redo functionality, navigation history | LIFO behavior, O(1) push/pop |
| **Priority Queue (Max Heap)** | Stock recommendations ranked by profit | O(log n) extraction of best stock vs O(n log n) repeated sorting |

---

## Project Structure

```
DSA_FINAL_PROJECT/
├── main.py               # Entry point
├── authentication.py     # Login/signup & password hashing
├── chatbot.py            # Gemini API chatbot
├── dummy.py              # Dummy trading system
├── dynamic_array.py      # Custom Dynamic Array implementation
├── hash_map.py           # Custom HashMap implementation
├── recommender.py        # Stock recommendation engine
├── stock_data.py         # Stock data management
├── fetch_psx_data.py     # PSX & Yahoo Finance API integration
├── user_menu.py          # User interface menus
├── user_storage.py       # Per-user file storage
├── password_utils.py     # Password hashing utilities
├── psx_stock_data.json   # Local PSX stock data
└── new_stockData.csv     # Historical stock data
```

---

## Sample Output

```
STOCK INVESTMENT SYSTEM
Loaded 3 existing user(s)
Loaded CAGR data for 10 stocks
Portfolio initialized with 10 stocks

TOP 3 RECOMMENDED STOCKS (PKR 1,200,000 investment)

RANK 1: FFC
  Current Price:       566.28 PKR
  CAGR:                129.69%
  Predicted 5Y Price:  36,205.28 PKR
  Total Profit:        75,519,041.64 PKR

RANK 2: HBL
  Current Price:       308.17 PKR
  CAGR:                63.04%
  Total Profit:        12,621,029.17 PKR

RANK 3: PSO
  Current Price:       456.13 PKR
  CAGR:                58.54%
  Total Profit:        10,815,359.55 PKR

Combined Profit: 98,955,430.37 PKR  |  ROI: 8246.3%
```

---

## Tech Stack

- Python 3
- Gemini API (AI Chatbot)
- Yahoo Finance API (Real-time stock prices)
- PSX local JSON/CSV data
- File handling for persistent user storage

## Setup & Run

```bash
# Clone the repo
git clone https://github.com/Aiman-005/Virtual-Stock-Trading-Simulator

# Install dependencies
pip install -r requirements.txt

# Run the project
python main.py
```

---

## Challenges Faced

- Handling API errors and network delays from Gemini and Yahoo Finance
- Implementing HashMap collision resolution from scratch
- Building Redo functionality on top of the Stack-based Undo system
- Password masking in console environment
- Debugging across multiple interconnected modules

---

## Future Improvements

- Allow chatbot to access user portfolio for personalized advice
- Support trading more than 10 stocks simultaneously
- Use 10–15 years of historical data for more accurate predictions
- Incorporate KSE-100 index and macroeconomic indicators
- Add company financial health metrics (revenue, debt, profit)

---

## Team

Built in a team of 3 as part of the **Data Structures & Algorithms** course at FAST-NUCES Karachi.

- Aiman Farooqui (24k-3077)
- Teammate (24k-3075)
- Teammate (24k-3101)

## Course

DSA — BS Software Engineering, FAST-NUCES Karachi (Semester 3)
