
import csv
from datetime import datetime

CSV_FILE = "portfolio_summary.csv"


def get_positive_number(message):
    while True:
        try:
            value = float(input(message))
            if value > 0:
                return value
            print("Enter a number greater than zero.")
        except ValueError:
            print("Please enter a valid number.")


def calculate_portfolio(positions):
    results = []
    total_invested = 0
    total_value = 0

    for ticker, details in positions.items():
        shares = details["shares"]
        buy_price = details["buy_price"]
        current_price = details["current_price"]

        invested = shares * buy_price
        market_value = shares * current_price
        profit_loss = market_value - invested
        percentage = (profit_loss / invested) * 100

        total_invested += invested
        total_value += market_value

        results.append({
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "invested": invested,
            "market_value": market_value,
            "profit_loss": profit_loss,
            "percentage": percentage
        })

    return results, total_invested, total_value


def save_to_csv(results, total_invested, total_value):
    file_exists = False

    try:
        with open(CSV_FILE, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    fields = [
        "timestamp", "ticker", "shares", "buy_price",
        "current_price", "invested", "market_value",
        "profit_loss", "percentage"
    ]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        for item in results:
            row = {
                "timestamp": timestamp,
                "ticker": item["ticker"],
                "shares": item["shares"],
                "buy_price": item["buy_price"],
                "current_price": item["current_price"],
                "invested": round(item["invested"], 2),
                "market_value": round(item["market_value"], 2),
                "profit_loss": round(item["profit_loss"], 2),
                "percentage": round(item["percentage"], 2)
            }
            writer.writerow(row)

        profit = total_value - total_invested
        percentage = (profit / total_invested) * 100

        writer.writerow({
            "timestamp": timestamp,
            "ticker": "PORTFOLIO TOTAL",
            "shares": "",
            "buy_price": "",
            "current_price": "",
            "invested": round(total_invested, 2),
            "market_value": round(total_value, 2),
            "profit_loss": round(profit, 2),
            "percentage": round(percentage, 2)
        })


def main():
    positions = {}

    print("\n================================")
    print("   STOCK PORTFOLIO TRACKER")
    print("================================")

    while True:
        ticker = input("\nEnter stock ticker symbol: ").strip().upper()

        if not ticker or not ticker.replace(".", "").replace("-", "").isalnum():
            print("Please enter a valid ticker symbol.")
            continue

        if ticker in positions:
            print("Stock already entered.")
            continue

        buy_price = get_positive_number("Enter buying price: ")
        shares = get_positive_number("Enter number of shares: ")
        current_price = get_positive_number("Enter current price: ")

        positions[ticker] = {
            "buy_price": buy_price,
            "shares": shares,
            "current_price": current_price
        }

        choice = input("Add another stock? (yes/no): ").strip().lower()

        if choice not in ("yes", "y"):
            break

    results, total_invested, total_value = calculate_portfolio(positions)

    print("\n================================")
    print("      PORTFOLIO SUMMARY")
    print("================================")

    for item in results:
        print(f"\nStock: {item['ticker']}")
        print(f"Investment: Rs. {item['invested']:.2f}")
        print(f"Current Value: Rs. {item['market_value']:.2f}")
        print(f"Profit/Loss: Rs. {item['profit_loss']:.2f}")
        print(f"Return: {item['percentage']:.2f}%")

    profit = total_value - total_invested
    percentage = (profit / total_invested) * 100

    print("\n--------------------------------")
    print(f"Total Investment: Rs. {total_invested:.2f}")
    print(f"Total Value: Rs. {total_value:.2f}")
    print(f"Total Profit/Loss: Rs. {profit:.2f}")
    print(f"Overall Return: {percentage:.2f}%")
    print("--------------------------------")

    save_to_csv(results, total_invested, total_value)

    print("\nCSV file saved successfully!")
    print("Thank you for using the tracker!")


if __name__ == "__main__":
    main()
