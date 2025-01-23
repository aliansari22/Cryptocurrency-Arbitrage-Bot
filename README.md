# Cryptocurrency Arbitrage Bot

This Python application fetches cryptocurrency prices from various exchanges and identifies potential arbitrage opportunities. By leveraging asynchronous programming, it efficiently compares prices across multiple exchanges in real-time to help users spot differences that could be profitable.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Asynchronous Programming**: Utilizes Python’s `asyncio` and `aiohttp` libraries to fetch prices concurrently from multiple exchanges, significantly reducing the time needed to gather data.
- **Multi-Exchange Support**: Fetches cryptocurrency prices from popular exchanges including Binance, Kraken, BitFinex, Coinbase, Huobi, Bitstamp, and CoinAPI.
- **Real-Time Arbitrage Detection**: Continuously monitors and identifies arbitrage opportunities, displaying the buy and sell exchanges, and potential profit percentages.
- **Customizable Cryptocurrency Pairs**: Easily adjust the list of cryptocurrency pairs to monitor and add new pairs as needed.
- **User-Friendly Output**: Displays arbitrage opportunities in a clear and easy-to-read table format using PrettyTable.

## Installation

To use this application, you need to have Python 3.7 or higher installed. Follow these steps to install and run the application:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/aliansari22/Cryptocurrency-Arbitrage-Bot.git
   cd Cryptocurrency-Arbitrage-Bot
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the arbitrage bot, execute the following command:

```bash
python arbitrage_bot.py
```

The bot will continuously fetch prices from various exchanges and display potential arbitrage opportunities in the console every 10 seconds.

## Configuration

Before running the bot, ensure you have configured your API keys and settings where necessary:

1. **CoinAPI**: Obtain an API key from [CoinAPI](https://www.coinapi.io/) and replace `'YOUR_API_KEY'` in the `EXCHANGES` dictionary with your actual API key.

2. **Customize Cryptocurrency Pairs**: Modify the `CRYPTO_PAIRS` list in the script to add or remove cryptocurrency pairs according to your needs.

3. **Adjust Fetch Frequency**: By default, the bot fetches prices every 10 seconds. You can adjust this interval by changing the `await asyncio.sleep(10)` line in the `main` function to your desired value.

## Examples

When you run the bot, it outputs a table of potential arbitrage opportunities like this:

```
Fetching prices...
+---------------------+------------+---------+-------------------+
| Cryptocurrency Pair | Buy From   | Sell To | Profit Percentage |
+---------------------+------------+---------+-------------------+
| BTCUSD              | Kraken     | Binance | 1.25%             |
| ETHUSD              | Bitstamp   | Coinbase| 0.75%             |
+---------------------+------------+---------+-------------------+
```

This table indicates where to buy and sell to capitalize on the arbitrage opportunity, along with the potential profit percentage.

## Special Features

### Asynchronous Price Fetching

The bot uses **asynchronous programming** to fetch prices from multiple exchanges concurrently. This approach is faster and more efficient than sequential HTTP requests because it allows the bot to perform multiple network operations in parallel. By utilizing `asyncio` and `aiohttp`, the bot reduces the time it takes to gather price data from several exchanges, ensuring that the arbitrage calculations are based on the most up-to-date information available.

### Multi-Exchange Support

With support for various exchanges, the bot provides a comprehensive view of the market, increasing the chances of finding profitable arbitrage opportunities. Each exchange has its own API endpoint configured within the bot, making it easy to extend and support additional exchanges if needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Disclaimer

This tool is for educational purposes only. Trading cryptocurrencies involves significant risk, and there is no guarantee that arbitrage opportunities will be profitable. Use this tool at your own risk.
