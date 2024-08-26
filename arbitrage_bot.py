import asyncio
import aiohttp
import json
from prettytable import PrettyTable

# Exchange API endpoints for fetching cryptocurrency prices
EXCHANGES = {
    'Binance': 'https://api.binance.com/api/v3/avgPrice?symbol=',
    'Kraken': 'https://api.kraken.com/0/public/Ticker?pair=',
    'BitFinex': 'https://api.bitfinex.com/v1/pubticker/',
    'Coinbase': 'https://api.coinbase.com/v2/prices/{}/spot',
    'Huobi': 'https://api.huobi.pro/market/detail/merged?symbol=',
    'Bitstamp': 'https://www.bitstamp.net/api/v2/ticker/',
    'CoinAPI': 'https://rest.coinapi.io/v1/exchangerate/{}/{}',
}

# List of cryptocurrency pairs to fetch prices for
CRYPTO_PAIRS = ['BTCUSD', 'ETHUSD', 'LTCUSD', 'ADAUSD', 'DOTUSD', 'XLMUSD', 'SOLUSD']

async def fetch_price(session, url, headers=None):
    """
    Fetches the price data from a given URL using aiohttp session.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        url (str): The URL to fetch data from.
        headers (dict, optional): Optional headers for the request.

    Returns:
        dict or None: The JSON response as a dictionary if the request was successful,
                      None otherwise.
    """
    try:
        async with session.get(url, headers=headers) as response:
            # Check if the content type is JSON
            if response.headers['Content-Type'].startswith('application/json'):
                return await response.json()
            else:
                # Attempt to parse the response as JSON in case of unexpected content type
                text = await response.text()
                return json.loads(text)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

async def get_prices(session, pair):
    """
    Fetches the cryptocurrency prices from multiple exchanges concurrently.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for the requests.
        pair (str): The cryptocurrency pair to fetch prices for (e.g., 'BTCUSD').

    Returns:
        dict: A dictionary with the pair as key and a nested dictionary of exchange prices.
    """
    tasks = [
        fetch_price(session, EXCHANGES['Binance'] + pair + 'T'),
        fetch_price(session, EXCHANGES['Kraken'] + pair.replace('BTC', 'XBT') + 'T'),
        fetch_price(session, EXCHANGES['BitFinex'] + pair.lower()),
        fetch_price(session, EXCHANGES['Coinbase'].format(pair.replace('USD', '-USD'))),
        fetch_price(session, EXCHANGES['Huobi'] + pair.lower()),
        fetch_price(session, EXCHANGES['Bitstamp'] + pair.lower() + '/'),
        fetch_price(session, EXCHANGES['CoinAPI'].format(pair[:3], pair[3:]), headers={'X-CoinAPI-Key': 'YOUR_API_KEY'}),  # Replace 'YOUR_API_KEY' with your CoinAPI key
    ]

    # Gather all fetch tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    prices = {}

    # Extract prices from each exchange's response
    prices['Binance'] = float(results[0]['price']) if results[0] and isinstance(results[0], dict) and 'price' in results[0] else None
    prices['Kraken'] = float(results[1]['result'][list(results[1]['result'].keys())[0]]['c'][0]) if results[1] and isinstance(results[1], dict) and 'result' in results[1] and results[1]['result'] else None
    prices['BitFinex'] = float(results[2]['last_price']) if results[2] and isinstance(results[2], dict) and 'last_price' in results[2] else None
    prices['Coinbase'] = float(results[3]['data']['amount']) if results[3] and isinstance(results[3], dict) and 'data' in results[3] and 'amount' in results[3]['data'] else None
    prices['Huobi'] = float(results[4]['tick']['close']) if results[4] and isinstance(results[4], dict) and 'tick' in results[4] and 'close' in results[4]['tick'] else None
    prices['Bitstamp'] = float(results[5]['last']) if results[5] and isinstance(results[5], dict) and 'last' in results[5] else None
    prices['CoinAPI'] = float(results[6]['rate']) if results[6] and isinstance(results[6], dict) and 'rate' in results[6] else None

    return {pair: prices}

async def fetch_prices():
    """
    Fetches the prices for all cryptocurrency pairs asynchronously.

    Returns:
        dict: A dictionary of all cryptocurrency pairs and their prices from different exchanges.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [get_prices(session, pair) for pair in CRYPTO_PAIRS]
        prices_list = await asyncio.gather(*tasks)

        # Combine all prices into a single dictionary
        prices = {}
        for price in prices_list:
            prices.update(price)
        
        return prices

def find_arbitrage_opportunities(prices):
    """
    Identifies potential arbitrage opportunities based on price differences between exchanges.

    Args:
        prices (dict): A dictionary of cryptocurrency pairs and their prices from different exchanges.

    Returns:
        list: A list of dictionaries representing arbitrage opportunities.
    """
    opportunities = []
    for pair, price_data in prices.items():
        available_prices = {exchange: price for exchange, price in price_data.items() if price is not None}

        if len(available_prices) > 1:
            min_price = min(available_prices.values())
            max_price = max(available_prices.values())
            if max_price > min_price:
                profit_pct = ((max_price - min_price) / min_price) * 100
                opportunities.append({
                    'pair': pair,
                    'buy_exchange': [ex for ex, price in available_prices.items() if price == min_price][0],
                    'sell_exchange': [ex for ex, price in available_prices.items() if price == max_price][0],
                    'profit_pct': profit_pct
                })
    
    return opportunities

def display_opportunities(opportunities):
    """
    Displays the identified arbitrage opportunities in a table format.

    Args:
        opportunities (list): A list of arbitrage opportunities to display.
    """
    if not opportunities:
        print("No arbitrage opportunities found.")
        return

    table = PrettyTable()
    table.field_names = ["Cryptocurrency Pair", "Buy From", "Sell To", "Profit Percentage"]

    for opportunity in opportunities:
        table.add_row([opportunity['pair'], opportunity['buy_exchange'], opportunity['sell_exchange'], f"{opportunity['profit_pct']:.2f}%"])

    print(table)

async def main():
    """
    Main function to continuously fetch prices and display arbitrage opportunities.
    """
    while True:
        print("\nFetching prices...")
        prices = await fetch_prices()
        opportunities = find_arbitrage_opportunities(prices)
        display_opportunities(opportunities)
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
