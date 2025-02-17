### Jojo API

JOJO API is a Python API client for interacting with the JOJO exchange. It provides the following features:

- Support for public endpoints:
  - Get exchange time
  - Get exchange info
  - Get orderbook depth
  - Get trade history
  - Get kline data
  - Get mark price
  - Get funding rate
  - Get risky accounts

- Support for private endpoints:
  - Account management
  - Order management (place/cancel orders etc.)
  - Position query
  - Balance query
  - Income records
  - Trade history

- Support for subaccount authorization
- Support for signature authentication
- Support for testnet and mainnet environments

### Installation

```bash
pip install -r requirements.txt
```

config `JOJO_API_BASE_URL` and `ACCOUNT_PRIVATE_KEY` in `.env`

### Usage

```python
python main.py
```
