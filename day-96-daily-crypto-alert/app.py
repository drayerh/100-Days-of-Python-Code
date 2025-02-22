import os
import requests
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///xrp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Twilio Client initialization
twilio_client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
USER_WHATSAPP_NUMBER = os.getenv("USER_WHATSAPP")

# Log environment variables
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"TWILIO_WHATSAPP_NUMBER: {TWILIO_WHATSAPP_NUMBER}")
logging.debug(f"USER_WHATSAPP_NUMBER: {USER_WHATSAPP_NUMBER}")

# Database Models
class DailyAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    analysis = db.Column(db.Text, nullable=False)

class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    analysis = db.Column(db.Text, nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# External API Config
COINGECKO_API = "https://api.coingecko.com/api/v3"
NEWSAPI_URL = "https://newsapi.org/v2/everything"
DEEPSEEK_API = "https://api.deepseek.com/"
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

def get_xrp_price():
    """Fetch current XRP price from CoinGecko"""
    response = requests.get(
        f"{COINGECKO_API}/simple/price?ids=ripple&vs_currencies=usd"
    )
    return response.json()['ripple']['usd']

def get_xrp_news():
    """Fetch latest XRP news from NewsAPI"""
    params = {
        'q': 'XRP OR Ripple',
        'sortBy': 'publishedAt',
        'apiKey': NEWSAPI_KEY
    }
    response = requests.get(NEWSAPI_URL, params=params)
    return response.json().get('articles', [])[:5]  # Get top 5 articles

def analyze_with_deepseek(text):
    """Analyze text using DeepSeek API"""
    headers = {'Authorization': f'Bearer {os.getenv("DEEPSEEK_API_KEY")}'}
    payload = {
        "text": text,
        "model": "deepseek-r1",
        "analysis_type": "financial_impact",
        "audience": "retail_investors"
    }
    response = requests.post(DEEPSEEK_API, json=payload, headers=headers)

    # Log the response for debugging
    app.logger.debug(f"DeepSeek API Response: {response.status_code} {response.text}")

    if response.status_code == 200:
        return response.json().get('analysis', 'No analysis available')
    else:
        app.logger.error(f"Failed to analyze with DeepSeek API: {response.status_code} {response.text}")
        return 'No analysis available'

def send_whatsapp_message(message):
    """Send message via Twilio WhatsApp API"""
    try:
        message = twilio_client.messages.create(
            body=message,
            from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
            to=f"whatsapp:{USER_WHATSAPP_NUMBER}"
        )
        return message.sid
    except Exception as e:
        app.logger.error(f"Failed to send WhatsApp message: {str(e)}")
        return None

def create_daily_alert():
    """Main function to create daily alert with WhatsApp notifications"""
    with app.app_context():
        new_articles = []
        price = get_xrp_price()
        news_articles = get_xrp_news()

        # Process news articles
        for article in news_articles:
            existing = NewsArticle.query.filter_by(title=article['title']).first()
            if not existing:
                analysis = analyze_with_deepseek(f"{article['title']} {article['description']}")
                news_entry = NewsArticle(
                    title=article['title'],
                    content=article['content'],
                    source=article['source']['name'],
                    timestamp=datetime.fromisoformat(article['publishedAt'].replace('Z', '')),
                    analysis=analysis
                )
                db.session.add(news_entry)
                new_articles.append({
                    'title': article['title'],
                    'source': article['source']['name'],
                    'analysis': analysis
                })

        # Create daily alert entry
        analysis = analyze_with_deepseek(f"Daily XRP price update: {price}")
        alert = DailyAlert(
            date=datetime.utcnow(),
            price=price,
            analysis=analysis
        )
        db.session.add(alert)
        db.session.commit()

        # Send WhatsApp notifications
        alert_message = (
            f"🚨 Daily XRP Alert 🚨\n"
            f"Date: {alert.date.strftime('%Y-%m-%d %H:%M')} GMT\n"
            f"Price: ${price:.4f}\n"
            f"Analysis: {alert.analysis[:480]}"
        )
        send_whatsapp_message(alert_message)

        # Send news alerts
        for article in new_articles:
            news_message = (
                f"📰 Breaking XRP News 📰\n"
                f"Title: {article['title'][:100]}\n"
                f"Source: {article['source']}\n"
                f"Analysis: {article['analysis'][:480]}"
            )
            send_whatsapp_message(news_message)

# Configure scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=create_daily_alert,
    trigger='cron',
    hour=1,
    minute=30,
    timezone='GMT'
)
scheduler.start()

# Routes
@app.route('/')
def dashboard():
    latest_alert = DailyAlert.query.order_by(DailyAlert.date.desc()).first()
    news = NewsArticle.query.order_by(NewsArticle.timestamp.desc()).limit(5).all()

    # Add logging to debug
    app.logger.debug(f"Latest Alert: {latest_alert}")
    app.logger.debug(f"News: {news}")

    return render_template('dashboard.html', alert=latest_alert, news=news)

@app.route('/history')
def history():
    alerts = DailyAlert.query.order_by(DailyAlert.date.desc()).all()
    return render_template('history.html', alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True)