# onchainpay.io Python SDK

### Example

```python
from onchainpay_sdk import Client

client = Client("<your_public_key>", "<your_private_key>")
result = client.advanced_account.get_advanced_balances()
print(result)  # {"success": True, "response": {...}}
```

### Tests

```shell
pip install -r requirements.txt
python -m pytest tests/*
```