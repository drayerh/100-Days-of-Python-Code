# Daily Crypto Alert

## Overview

Daily Crypto Alert is a Flask-based application that provides daily alerts and news about XRP (Ripple) cryptocurrency. It fetches the latest price and news articles, analyzes them using the DeepSeek API, and sends notifications via WhatsApp using the Twilio API.

## Features

- Fetches the current XRP price from CoinGecko.
- Retrieves the latest XRP news articles from NewsAPI.
- Analyzes news articles and price updates using the DeepSeek API.
- Sends daily alerts and news updates via WhatsApp using Twilio.
- Stores alerts and news articles in a SQLite database.
- Provides a web dashboard to view the latest alerts and news.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/drayerh/100-Days-of-Python-Code.git
    cd day-96-daily-crypto-alert
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory and add the following variables:
    ```dotenv
    TWILIO_SID='your_twilio_sid'
    TWILIO_AUTH='your_twilio_auth_token'
    TWILIO_WHATSAPP_NUMBER='your_twilio_whatsapp_number'
    USER_WHATSAPP='your_whatsapp_number'
    DEEPSEEK_API_KEY='your_deepseek_api_key'
    NEWSAPI_KEY='your_newsapi_key'
    ```

5. Initialize the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. Run the application:
    ```sh
    flask run
    ```

## Usage

- Access the web dashboard at `http://127.0.0.1:5000/` to view the latest alerts and news.
- The application will automatically fetch and analyze data, and send WhatsApp notifications daily at the configured time.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.