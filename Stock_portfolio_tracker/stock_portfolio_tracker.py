# ============================================================
#         STOCK PORTFOLIO TRACKER
#         CodeAlpha Internship Project
#         Author: Siraj
#         Date: October 2026
# ============================================================
# This program lets you build a simple stock portfolio.
# You enter stock symbols and quantities, and it calculates
# the total value of your investment.
# No external libraries needed — just pure Python!
# ============================================================


# -------------------------------------------------------
# STEP 1: Define a dictionary of available stocks
#         Key   = Stock symbol (string)
#         Value = Stock price in USD (float)
# -------------------------------------------------------
STOCK_PRICES = {
    "AAPL":  189.30,   # Apple Inc.
    "TSLA":  177.82,   # Tesla Inc.
    "MSFT":  415.50,   # Microsoft Corporation
    "GOOGL": 175.98,   # Alphabet Inc. (Google)
    "AMZN":  196.45,   # Amazon.com Inc.
    "NVDA":  875.40,   # NVIDIA Corporation
    "META":  527.10,   # Meta Platforms Inc.
    "NFLX":  638.29,   # Netflix Inc.
}


# -------------------------------------------------------
# FUNCTION: display_available_stocks
# Shows all available stocks and their current prices.
# -------------------------------------------------------
def display_available_stocks():
    """Prints a formatted table of all available stocks."""
    print("\n" + "=" * 45)
    print("       [CHART]  AVAILABLE STOCKS  [CHART]")
    print("=" * 45)
    print(f"  {'SYMBOL':<8}  {'COMPANY / DESCRIPTION':<22}  {'PRICE (USD)':>10}")
    print("-" * 45)

    # A small lookup to show friendly company names
    company_names = {
        "AAPL":  "Apple Inc.",
        "TSLA":  "Tesla Inc.",
        "MSFT":  "Microsoft Corp.",
        "GOOGL": "Alphabet (Google)",
        "AMZN":  "Amazon.com Inc.",
        "NVDA":  "NVIDIA Corp.",
        "META":  "Meta Platforms",
        "NFLX":  "Netflix Inc.",
    }

    # Loop through each stock and print its details
    for symbol, price in STOCK_PRICES.items():
        company = company_names.get(symbol, "N/A")
        print(f"  {symbol:<8}  {company:<22}  ${price:>9.2f}")

    print("=" * 45)


# -------------------------------------------------------
# FUNCTION: get_stock_symbol
# Asks the user for a valid stock symbol.
# Keeps asking until a valid one is entered.
# -------------------------------------------------------
def get_stock_symbol():
    """Prompts the user for a stock symbol and validates it."""
    while True:
        # Strip whitespace and convert to UPPERCASE for consistency
        symbol = input("\n  Enter stock symbol (e.g. AAPL): ").strip().upper()

        if symbol == "":
            print("  [!]  No input detected. Please enter a stock symbol.")
        elif symbol not in STOCK_PRICES:
            print(f"  [X]  '{symbol}' is not in our stock list. Please try again.")
        else:
            return symbol  # Valid symbol found — return it


# -------------------------------------------------------
# FUNCTION: get_quantity
# Asks the user for the number of shares.
# Validates that the input is a positive whole number.
# -------------------------------------------------------
def get_quantity(symbol):
    """Prompts the user for a valid share quantity."""
    while True:
        raw = input(f"  Enter quantity of {symbol} shares: ").strip()

        # Check if the user typed anything at all
        if raw == "":
            print("  [!]  No quantity entered. Please enter a number.")
            continue

        # Try to convert the input to an integer
        try:
            quantity = int(raw)
            if quantity <= 0:
                print("  [X]  Quantity must be a positive number (at least 1).")
            else:
                return quantity  # Valid quantity — return it
        except ValueError:
            # The user typed something that isn't a number (e.g., "abc")
            print("  [X]  Invalid input. Please enter a whole number (e.g., 10).")


# -------------------------------------------------------
# FUNCTION: add_to_portfolio
# Adds a stock entry to the portfolio dictionary.
# If the stock already exists, increases its quantity.
# -------------------------------------------------------
def add_to_portfolio(portfolio, symbol, quantity):
    """
    Adds or updates a stock entry in the portfolio.

    portfolio : dict  — the current portfolio
    symbol    : str   — stock ticker symbol
    quantity  : int   — number of shares to add
    """
    if symbol in portfolio:
        # Stock already in portfolio — add more shares
        portfolio[symbol] += quantity
        print(f"  [OK]  Updated {symbol}: now holding {portfolio[symbol]} shares.")
    else:
        # New stock — add it with the given quantity
        portfolio[symbol] = quantity
        print(f"  [OK]  Added {symbol} x {quantity} shares to your portfolio.")


# -------------------------------------------------------
# FUNCTION: display_portfolio
# Prints a summary table of the entire portfolio.
# Returns the total investment value.
# -------------------------------------------------------
def display_portfolio(portfolio):
    """
    Displays the portfolio and calculates the total investment.

    portfolio : dict  — stock symbol mapped to quantity
    Returns   : float — total portfolio value
    """
    if not portfolio:
        print("\n  Your portfolio is empty. Add some stocks first!")
        return 0.0

    print("\n" + "=" * 58)
    print("            [BRIEFCASE]  YOUR STOCK PORTFOLIO  [BRIEFCASE]")
    print("=" * 58)
    print(f"  {'SYMBOL':<8} {'SHARES':>8} {'PRICE (USD)':>12} {'VALUE (USD)':>14}")
    print("-" * 58)

    total_value = 0.0  # Running total of the entire portfolio

    # Loop through each stock the user has added
    for symbol, quantity in portfolio.items():
        price       = STOCK_PRICES[symbol]       # Look up current price
        stock_value = quantity * price            # Calculate this stock's value
        total_value += stock_value               # Add to running total

        print(f"  {symbol:<8} {quantity:>8} ${price:>11.2f} ${stock_value:>13.2f}")

    print("-" * 58)
    print(f"  {'TOTAL PORTFOLIO VALUE':<40} ${total_value:>13.2f}")
    print("=" * 58)

    return total_value


# -------------------------------------------------------
# FUNCTION: save_portfolio_to_file
# Saves the portfolio summary to a .txt file.
# -------------------------------------------------------
def save_portfolio_to_file(portfolio, total_value):
    """
    Saves the portfolio summary to 'portfolio_summary.txt'.

    portfolio   : dict  — stock symbol mapped to quantity
    total_value : float — total investment value
    """
    filename = "portfolio_summary.txt"

    # 'with open(...)' automatically closes the file when done
    with open(filename, "w") as file:
        file.write("=" * 58 + "\n")
        file.write("         STOCK PORTFOLIO SUMMARY\n")
        file.write("         Generated by Stock Portfolio Tracker\n")
        file.write("=" * 58 + "\n")
        file.write(f"  {'SYMBOL':<8} {'SHARES':>8} {'PRICE (USD)':>12} {'VALUE (USD)':>14}\n")
        file.write("-" * 58 + "\n")

        for symbol, quantity in portfolio.items():
            price       = STOCK_PRICES[symbol]
            stock_value = quantity * price
            file.write(f"  {symbol:<8} {quantity:>8} ${price:>11.2f} ${stock_value:>13.2f}\n")

        file.write("-" * 58 + "\n")
        file.write(f"  {'TOTAL PORTFOLIO VALUE':<40} ${total_value:>13.2f}\n")
        file.write("=" * 58 + "\n")

    print(f"\n  [FILE]  Portfolio saved to '{filename}' successfully!")


# -------------------------------------------------------
# FUNCTION: ask_yes_no
# A helper to ask any yes/no question cleanly.
# -------------------------------------------------------
def ask_yes_no(question):
    """Returns True if user answers 'y', False if 'n'."""
    while True:
        answer = input(question).strip().lower()
        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        else:
            print("  [!]  Please enter 'y' for yes or 'n' for no.")


# -------------------------------------------------------
# MAIN PROGRAM
# This is where execution begins.
# -------------------------------------------------------
def main():
    """Main function that runs the Stock Portfolio Tracker."""

    # Welcome banner
    print("\n" + "=" * 45)
    print("   [MONEY]  STOCK PORTFOLIO TRACKER  [MONEY]")
    print("   CodeAlpha Internship Project")
    print("=" * 45)
    print("  Track your investments easily!")
    print("  Prices are hardcoded for demo purposes.")

    # portfolio is a dictionary:
    #   key   = stock symbol (e.g. "AAPL")
    #   value = total shares owned (e.g. 10)
    portfolio = {}

    # Show the user which stocks are available
    display_available_stocks()

    # ---- Main loop: keep showing menu until the user exits ----
    while True:
        print("\n" + "-" * 45)
        print("  What would you like to do?")
        print("  [1] Add a stock to portfolio")
        print("  [2] View current portfolio")
        print("  [3] Save & Exit")
        print("-" * 45)

        choice = input("  Enter your choice (1 / 2 / 3): ").strip()

        # ---- Option 1: Add a stock ----
        if choice == "1":
            symbol   = get_stock_symbol()                        # Get valid symbol
            quantity = get_quantity(symbol)                      # Get valid quantity
            add_to_portfolio(portfolio, symbol, quantity)        # Add to portfolio

        # ---- Option 2: View portfolio ----
        elif choice == "2":
            display_portfolio(portfolio)

        # ---- Option 3: Save & Exit ----
        elif choice == "3":
            # Show final portfolio before exiting
            total_value = display_portfolio(portfolio)

            # Only offer to save if there's something in the portfolio
            if portfolio:
                save_choice = ask_yes_no(
                    "\n  Would you like to save your portfolio to a .txt file? (y/n): "
                )
                if save_choice:
                    save_portfolio_to_file(portfolio, total_value)

            print("\n  [BYE]  Thank you for using the Stock Portfolio Tracker!")
            print("  Happy investing! [ROCKET]\n")
            break  # Exit the while loop — program ends here

        # ---- Invalid menu choice ----
        else:
            print("  [!]  Invalid choice. Please enter 1, 2, or 3.")


# -------------------------------------------------------
# Entry point — only runs main() if this file is executed
# directly (not imported as a module).
# -------------------------------------------------------
if __name__ == "__main__":
    main()
