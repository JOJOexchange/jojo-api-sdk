### Jojo API

JOJO API is a Python API client for interacting with the JOJO exchange. It provides the following features:

- System API:
  - Get exchange time
  - Get exchange info

- Public API:
  - Get orderbook data
  - Get trades history
  - Get kline data
  - Get mark price klines
  - Get funding rate
  - Get risky accounts
  - Get historical trades

- Account API:
  - Register and get account info

- Order API:
  - Build and place orders
  - Cancel single/all orders
  - Get order details
  - Get open orders
  - Get order history
  - Get user trades
  - Get positions
  - Get balances
  - Get income records

- Support for subaccount operations
- Support for signature authentication
- Support for both testnet and mainnet environments

### Installation

```bash
pip install -r requirements.txt
```

config `JOJO_API_BASE_URL` and `ACCOUNT_PRIVATE_KEY` in `.env`

### Usage

```python
python main.py
```
