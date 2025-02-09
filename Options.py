import yfinance as yf
import pandas as pd


def get_best_option(ticker_symbol):
    # Fetch stock data
    stock = yf.Ticker(ticker_symbol)
    stock_price = stock.history(period="1d")["Close"].iloc[-1]  # Get latest stock price

    # Get available expiration dates
    expiration_dates = stock.options

    best_option = None
    min_function_value = float("inf")

    # Loop through all expiration dates
    for exp_date in expiration_dates:
        try:
            # Get call options data
            option_chain = stock.option_chain(exp_date)
            calls = option_chain.calls

            # Loop through all available call options
            for _, row in calls.iterrows():
                strike_price = row["strike"]
                premium = row["lastPrice"] * 100  # Convert to per 100 options
                break_even = row["strike"] + row["lastPrice"]  # Break-even price (E)

                # Compute function value
                if strike_price != premium / 100:  # Avoid division by zero
                    function_value = (break_even * stock_price - (premium / 100)) / (strike_price - (premium / 100))

                    # Check if this option minimizes the function
                    if function_value < min_function_value:
                        min_function_value = function_value
                        best_option = {
                            "Expiration Date": exp_date,
                            "Strike Price": strike_price,
                            "Premium": premium,
                            "Break-even Price": break_even,
                            "Function Value": function_value
                        }
        except Exception as e:
            print(f"Error retrieving data for {exp_date}: {e}")

    return best_option


# Example Usage
ticker = input("Enter stock ticker symbol: ").upper()
best_option = get_best_option(ticker)

if best_option:
    print("\nBest Option Trade (Minimizing Function):")
    for key, value in best_option.items():
        print(f"{key}: {value}")
else:
    print("No valid options found.")