# mepost-sdk

## Overview
The `mepost-sdk` is a Python library designed to simplify interactions with the Mepost API for sending and managing emails.

## Installation
Install this package using pip:
```bash
pip install mepost-sdk
```

## Usage
Here is a quick example:

```python
Copy code
from mepost.client import MepostClient

client = MepostClient(api_key="your_api_key")
response = client.send_email(email_data)
print(response)
```
