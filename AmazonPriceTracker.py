import requests as req
import bs4 as b4
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import logging
import schedule
import time
import winsound 


# Load environment variables from .env file
load_dotenv('Configuration.env')

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("price_tracker.log"),
        logging.StreamHandler()
    ]
)

# Fetch email credentials from environment variables
FROM_EMAIL_ADDRESS = os.getenv("FROM_EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL_ADDRESS = os.getenv("TO_EMAIL_ADDRESS")
frequency = 2500  # Set Frequency To 2500 Hertz 
duration = 1000  # Set Duration To 1000 ms == 1 second 

# Amazon product URL and target price
url = 'https://www.amazon.de/-/en/Court-Vision-Nature-Gymnastics-Shoes/dp/B09NMF4HWN/ref=sr_1_2?crid=LS686HYYEIIC&keywords=nike+shoes+mid'
TARGET_PRICE = 70.0  # Set your target price here


def exact_url(url):
    """Extract the exact product URL (up to the ASIN)"""
    index = url.find("B0")
    index = index + 10
    return url[:index]


def get_response(base_url):
    """Send a request to Amazon and return the response."""
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36'
    }
    try:
        response = req.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except req.RequestException as e:
        logging.error(f"Failed to fetch product details: {e}")
        return None


def extract_price(product_response):
    """Extract the product price from the Amazon page."""
    try:
        soup = b4.BeautifulSoup(product_response.text, features='lxml')
        price = soup.find("span", {"class": "a-offscreen"})
        if price:
            return float(price.text.replace("€", "").replace(",", "").strip())
    except Exception as e:
        logging.error(f"Failed to extract price: {e}")
    return None


def send_email_alert(price, product_url):
    """Send an email alert if the price is below the target."""
    msg = EmailMessage()
    msg['Subject'] = "Amazon Price Drop Alert!"
    msg['From'] = FROM_EMAIL_ADDRESS
    msg['To'] = TO_EMAIL_ADDRESS
    msg.set_content(f"The price dropped to €{price}! Check it here: {product_url}")
    print(FROM_EMAIL_ADDRESS)
    print(TO_EMAIL_ADDRESS)
    print(EMAIL_PASSWORD)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(FROM_EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            logging.info("Email sent successfully!")
    except smtplib.SMTPException as e:
        logging.error(f"Failed to send email: {e}")


def check_price():
    """Check the current price and send an email if below the target."""
    print('On check price')
    base_url = exact_url(url)
    product_response = get_response(base_url)
    print('On check price')
    if product_response:
        current_price = extract_price(product_response)
        print(current_price)
        if current_price:
            logging.info(f"Current price is €{current_price}")
            if current_price < TARGET_PRICE:
                logging.info(f"in email if €{TARGET_PRICE}")
                #send_email_alert(current_price, base_url)
                winsound.Beep(frequency, duration) 
        else:
            logging.warning("Price could not be extracted.")


# Schedule the price check every 1 minute (for testing)
schedule.every(1).minutes.do(check_price)


if __name__ == "__main__":
    
    logging.info("Starting Amazon Price Tracker...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Sleep to prevent high CPU usage
    except KeyboardInterrupt:
        logging.info("Amazon Price Tracker stopped.")
