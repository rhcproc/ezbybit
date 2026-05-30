# ezbybit

A small Python wrapper around `pybit` for simple Bybit spot BTC/ETH market
orders.

## Installation

Install from PyPI once the first release is published:

```bash
pip install ezbybit
```

For local development:

```bash
python -m pip install -e .
```

## Usage

```python
from ezbybit import BybitClient

client = BybitClient(
    api_key="YOUR_BYBIT_API_KEY",
    api_secret="YOUR_BYBIT_API_SECRET",
    testnet=True,
)

print(client.get_available_budget_usdt())
```

Place a market buy order using 80% of available USDT:

```python
response = client.buy("BTC")
print(response)

response = client.buy("ETH")
print(response)
```

Sell available BTC or ETH:

```python
response = client.sell("BTC")
print(response)

response = client.sell("ETH")
print(response)
```

By default, `buy()` uses 80% of available USDT. Pass a different ratio with
`Decimal`:

```python
from decimal import Decimal

response = client.buy("ETH", Decimal("0.5"))
```

You can also run the local example with environment variables:

```bash
export BYBIT_API_KEY="YOUR_BYBIT_API_KEY"
export BYBIT_API_SECRET="YOUR_BYBIT_API_SECRET"
python examples/basic.py
```

The package also installs a small CLI:

```bash
ezbybit --version
```

## Build

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

## Publish

Publish to TestPyPI first:

```bash
python -m twine upload --repository testpypi dist/*
```

Then publish to PyPI:

```bash
python -m twine upload dist/*
```
