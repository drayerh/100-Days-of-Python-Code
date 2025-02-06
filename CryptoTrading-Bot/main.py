import os
import ccxt
import numpy as np
import pandas as pd
import pandas_ta as ta
from dotenv import load_dotenv
from datetime import datetime
import websockets
import logging
import asyncio
import json
from sklearn.preprocessing import MinMaxScaler
from transformers import pipeline

# Load environment variables
load_dotenv()

# Initialize Bybit testnet
exchange = ccxt.bybit({
    'apiKey': os.getenv('BYBIT_API_KEY'),
    'secret': os.getenv('BYBIT_API_SECRET'),
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
        'adjustForTimeDifference': True,
    },
    'urls': {
        'api': {
            'public': 'https://api-testnet.bybit.com',
            'private': 'https://api-testnet.bybit.com'
        }
    }
})

# Constants
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'
POSITION_SIZE = 0.1  # 10% of portfolio per trade
MAX_LEVERAGE = 3
STOP_LOSS_PCT = 0.02  # 2% stop loss
TAKE_PROFIT_RATIO = 2  # 2:1 risk-reward ratio

class TradingBot:
    def __init__(self):
        """Initialize the TradingBot with sentiment analyzer and scaler."""
        self.sentiment_analyzer = pipeline("sentiment-analysis",
                                           model="finiteautomata/bertweet-base-sentiment-analysis")
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    async def fetch_historical_data(self):
        """
        Fetch and preprocess historical data from the exchange.

        Returns:
            pd.DataFrame: DataFrame containing historical OHLCV data.
        """
        ohlcv = exchange.fetch_ohlcv(SYMBOL, TIMEFRAME, limit=500)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df

    def calculate_technical_indicators(self, df):
        """
        Calculate technical indicators using Pandas TA.

        Args:
            df (pd.DataFrame): DataFrame containing OHLCV data.

        Returns:
            pd.DataFrame: DataFrame with calculated technical indicators.
        """
        # Trend indicators
        df['ema20'] = ta.ema(df['close'], length=20)
        df['ema50'] = ta.ema(df['close'], length=50)
        df['adx'] = ta.adx(df['high'], df['low'], df['close'], length=14)['ADX_14']

        # Momentum indicators
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['macd'] = ta.macd(df['close'])['MACD_12_26_9']
        df['macdsignal'] = ta.macd(df['close'])['MACDs_12_26_9']
        df['macdhist'] = ta.macd(df['close'])['MACDh_12_26_9']

        # Volatility indicators
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)

        # Volume indicators
        df['obv'] = ta.obv(df['close'], df['volume'])

        return df.dropna()

    async def get_sentiment_score(self):
        """
        Fetch and analyze market sentiment (mock implementation).

        Returns:
            float: Sentiment score based on sample text analysis.
        """
        # In production, integrate with actual news/social media API
        sample_text = "Bitcoin shows strong bullish momentum amid institutional adoption"
        result = self.sentiment_analyzer(sample_text)
        sentiment_score = 1 if result[0]['label'] == 'POS' else -1
        return sentiment_score * result[0]['score']

    def generate_signal(self, df, sentiment_score):
        """
        Generate trading signal using combined strategy.

        Args:
            df (pd.DataFrame): DataFrame containing OHLCV data and technical indicators.
            sentiment_score (float): Sentiment score from sentiment analysis.

        Returns:
            str: Trading signal ('long', 'short', or 'neutral').
        """
        # Normalize indicators
        features = df[['rsi', 'macd', 'adx', 'atr']]
        scaled_features = self.scaler.fit_transform(features)

        # Strategy components
        trend_strength = df['adx'].iloc[-1] > 25
        trend_direction = df['ema20'].iloc[-1] > df['ema50'].iloc[-1]
        momentum = 70 > df['rsi'].iloc[-1] > 30
        volatility = df['atr'].iloc[-1] > df['atr'].mean()

        # Combined signal score
        signal_score = (
                0.4 * trend_strength +
                0.3 * trend_direction +
                0.2 * momentum +
                0.1 * volatility +
                0.2 * sentiment_score
        )

        if signal_score > 0.6:
            return 'long'
        elif signal_score < -0.6:
            return 'short'
        return 'neutral'

    async def manage_risk(self):
        """
        Dynamic risk management based on portfolio metrics.

        Returns:
            tuple: Position size, stop loss price, and take profit price.
        """
        balance = exchange.fetch_balance()['USDT']['total']
        position_size = float(balance) * POSITION_SIZE
        atr = self.df['atr'].iloc[-1]

        stop_loss_price = atr * 1.5
        take_profit_price = stop_loss_price * TAKE_PROFIT_RATIO

        return position_size, stop_loss_price, take_profit_price

    async def execute_trade(self, signal):
        """
        Execute trade with proper risk management.

        Args:
            signal (str): Trading signal ('long', 'short', or 'neutral').
        """
        if signal == 'neutral':
            return

        position_size, stop_loss, take_profit = await self.manage_risk()

        # Cancel existing orders
        exchange.cancel_all_orders(SYMBOL)

        # Calculate leverage
        leverage = min(MAX_LEVERAGE, int(position_size / (await self.get_current_price())))
        exchange.set_leverage(leverage, SYMBOL)

        # Place order
        order_type = 'limit' if leverage > 1 else 'market'
        order = exchange.create_order(
            SYMBOL,
            order_type,
            'buy' if signal == 'long' else 'sell',
            position_size,
            None,
            {
                'stopLoss': stop_loss,
                'takeProfit': take_profit
            }
        )
        return order

    async def get_current_price(self):
        """
        Fetch the current price of the symbol.

        Returns:
            float: Current price of the symbol.
        """
        ticker = exchange.fetch_ticker(SYMBOL)
        return ticker['last']

    async def run_strategy(self):
        """
        Main trading loop with reconnection logic and exponential backoff.
        """
        self.df = await self.fetch_historical_data()
        self.df = self.calculate_technical_indicators(self.df)

        max_retries = 10
        base_retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                logging.info(f"Attempt {attempt + 1} to connect to WebSocket")
                ws = await asyncio.wait_for(websockets.connect('wss://stream-testnet.bybit.com/v5/public/spot'),
                                            timeout=60)
                async with ws:
                    await ws.send(json.dumps({
                        "op": "subscribe",
                        "args": [f"trade.{SYMBOL}"]
                    }))
                    logging.info("WebSocket connection established and subscription message sent")

                    while True:
                        try:
                            # Update data
                            msg = await asyncio.wait_for(ws.recv(), timeout=15)
                            data = json.loads(msg)

                            # Log the received message for debugging
                            logging.info(f"Received message: {data}")

                            # Handle subscription error
                            if data.get('retCode') == 10404:
                                logging.error(f"Subscription error: {data}")
                                break

                            # Process real-time data
                            if 'data' in data:
                                trade = data['data'][0]
                                new_row = pd.DataFrame({
                                    'timestamp': [datetime.fromtimestamp(trade['timestamp'] / 1000)],
                                    'open': [trade['price']],
                                    'high': [trade['price']],
                                    'low': [trade['price']],
                                    'close': [trade['price']],
                                    'volume': [trade['size']]
                                }).set_index('timestamp')
                                self.df = pd.concat([self.df, new_row])

                            # Update indicators
                            self.df = self.calculate_technical_indicators(self.df)

                            # Get sentiment
                            sentiment_score = await self.get_sentiment_score()

                            # Generate signal
                            signal = self.generate_signal(self.df, sentiment_score)

                            # Execute trade
                            await self.execute_trade(signal)

                            await asyncio.sleep(60)  # Check every minute

                        except Exception as e:
                            logging.error(f"Error while receiving message: {str(e)}")
                            continue

            except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError,
                    websockets.exceptions.InvalidStatusCode, websockets.exceptions.WebSocketException) as e:
                retry_delay = base_retry_delay * (2 ** attempt)
                logging.error(f"Connection error: {str(e)}. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                continue

            finally:
                await ws.close()

            break  # Exit the loop if connection is successful

        else:
            logging.error("Max retries reached. Exiting...")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot = TradingBot()
    asyncio.run(bot.run_strategy())