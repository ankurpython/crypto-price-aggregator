# Crypto Price Aggregator

A Python application that aggregates real-time Bitcoin (BTC) pricing data from multiple exchanges and calculates the optimal cost to buy or revenue from selling a specified quantity of Bitcoin.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

To check if Python is installed:
```bash
python --version
# or
python3 --version
```

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ankurpython/crypto-price-aggregator.git
cd crypto-price-aggregator
```

### 2. Create a Virtual Environment

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
Run the script with default settings (10 BTC):
```bash
python crypto_pricing.py
```

### Custom Quantity
Specify a custom quantity of Bitcoin:
```bash
python crypto_pricing.py --qty 5
python crypto_pricing.py --qty 25.75
```

### Example Output
```
To buy 10 BTC: $1,126,888.25
To sell 10 BTC: $1,126,210.96
```


## Project Structure
```
crypto-price-aggregator/
├── crypto_pricing.py    # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── venv/              # Virtual environment (created during setup)
```

## Notes

- Prices are in USD
- The tool provides market prices based on current order books

## Thank you
