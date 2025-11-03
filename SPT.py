import yfinance as yf

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, symbol, quantity, buy_price):
        """Add stock to the portfolio (weighted-average buy price)."""
        symbol = symbol.upper()
        if symbol in self.portfolio:
            existing_qty = self.portfolio[symbol]['quantity']
            existing_bp  = self.portfolio[symbol]['buy_price']

            new_total_qty = existing_qty + quantity
            new_avg_price = ((existing_bp * existing_qty) + (buy_price * quantity)) / new_total_qty

            self.portfolio[symbol]['quantity']  = new_total_qty
            self.portfolio[symbol]['buy_price'] = new_avg_price
        else:
            self.portfolio[symbol] = {"quantity": quantity, "buy_price": buy_price}

    def remove_stock(self, symbol):
        """Remove stock from the portfolio."""
        symbol = symbol.upper()
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            print(f"{symbol} removed from portfolio.")
        else:
            print(f"{symbol} not found in the portfolio.")

    def fetch_live_price(self, symbol):
        """Fetch the latest close price via Yahoo Finance."""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            if not data.empty:
                return float(data["Close"].iloc[-1])
            print(f"No price data found for {symbol}.")
            return None
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def view_portfolio(self):
        """Display portfolio details with live prices."""
        if not self.portfolio:
            print("\nYour Portfolio is empty")
            return

        total_invested = 0.0
        total_value = 0.0

        print("\nStock Portfolio Summary:")
        print("-" * 60)
        print(f"{'Stock':<10}{'Qty':<10}{'Buy Price':<12}{'Live Price':<12}{'P/L':>10}")
        print("-" * 60)

        for symbol, details in self.portfolio.items():
            live_price = self.fetch_live_price(symbol)
            if live_price is None:
                continue

            qty = details["quantity"]
            invested = qty * details["buy_price"]
            current_value = qty * live_price
            profit_loss = current_value - invested

            total_invested += invested
            total_value += current_value

            print(f"{symbol:<10}{qty:<10}{details['buy_price']:<12.2f}{live_price:<12.2f}{profit_loss:>10.2f}")

        print("-" * 60)
        print(f"Total Invested:           ${total_invested:.2f}")
        print(f"Current Portfolio Value:  ${total_value:.2f}")
        print(f"Overall P/L:              ${total_value - total_invested:.2f}")
        print("-" * 60)

def main():
    portfolio = StockPortfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ").upper()
            quantity = int(input("Enter quantity: "))
            buy_price = float(input("Enter purchase price: "))
            portfolio.add_stock(symbol, quantity, buy_price)
            print(f"{symbol} added to portfolio.")
        elif choice == "2":
            symbol = input("Enter stock symbol to remove: ").upper()
            portfolio.remove_stock(symbol)
        elif choice == "3":
            portfolio.view_portfolio()
        elif choice == "4":
            print("Exiting Stock Portfolio Tracker. GoodBye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
