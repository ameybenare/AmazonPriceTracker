# Amazon Price Tracker

## Description
This Python script tracks the price of a product on Amazon and alerts the user with sound notification if the price falls below a specified target. The code for sending email alert  is addedbut make sure to configure your account using app passwords to send emails.

## Features
- Tracks the price of any product on Amazon.
- Alerts user for price drops.
- Logs activities and errors.

## Requirements
- Python 3.x
- An Amazon product URL.
- Gmail account for sending email alerts with setup for app passwords.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/price-tracker.git
    cd price-tracker
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file with your email credentials.

## Usage
Run the script:
```bash
python price_tracker.py
