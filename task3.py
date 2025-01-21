import requests

key = 'YOUR_ALPHA-VANTAGE_API_KEY'
url = 'https://www.alphavantage.co/quary'

portfolio = {}

def get_stock_price(sym):
    """Fetch the current stock price from Alpha vantage."""
    params = {
        'function': 'THE_SERIES-INTRADAY',
        'Symbol' : sym,
        'internal': '1min',
        'apikey': key
    }
    try:
        response = requests.get(url , params=params)
        response.raise_for_status()
        data = response.json()
        if 'Time Series (1min)' in data:
            lastest_time = list(data['Time Series (1min)'].keys())[0]
            lastest_price = data['Time Series (1min)'][lastest_time]['1.open']
            return float(lastest_price)
        else:
            print(f"Error: {data.get('Error Message', 'Unable to fatch data')}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
    
def add_stock(sym, quantity):
    """Add or update a stock in the portfolio."""
    sym = sym.upper()
    price = get_stock_price(sym)
    if price is not None:
        if sym in portfolio:
            portfolio[sym]['quantity'] += quantity
        else:
            portfolio[sym] = {'quantity': quantity, 'price': price}
        print(f"Added {quantity} of {sym} to the portfolio.")
    else:
        print("Failed to add stock. Price data unavailable.")

def remove_stock(sym, quantity):
    """Remove or update a stock from the portfolio."""
    sym = sym.upper()
    if sym in portfolio:
        if portfolio[sym]['quantity'] >= quantity:
            portfolio[sym]['quantity'] -= quantity
            if portfolio[sym]['quantity'] == 0:
                del portfolio[sym]
            print(f"Removed{quantity} of {sym} from the portfolio.")
        else:
            print("Insufficient quantity to remove.")
    else:
        print("Stock not found in  portfolio.")

def print_portfolio():
    """Print the current portfolio."""
    if not portfolio:
        print("Porfolio is empty.")
        return
    for sym, data in portfolio.items():
        print(f"{sym}: quantity = {data['quantity']}, price = ${data['price']:.2f}")

def calculate_performance():
    """Calculate and print the total value of the portfolio."""
    total_value = 0
    for sym, data in portfolio.items():
        price = get_stock_price(sym)
        if price is not None:
            total_value += price * data['quantity']
        else:
            print(f"Warning: unable to fatch price for {sym}")
    print(f"Total portfolio value: ${total_value:.2f}")

def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove stock")
        print("3. view portfolio")
        print("4. Calculate Performance")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            sym = input("Enter your symbol: ")
            quantity = int(input("Enter quantity"))
            add_stock(sym, quantity)

        elif choice == '2':
            sym = input("Enter your symbol: ")
            quantity = int(input("Enter quantity"))
            remove_stock(sym, quantity)

        elif choice == '3':
            print_portfolio()

        elif choice == '4':
            calculate_performance()

        elif chocie == '5':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()