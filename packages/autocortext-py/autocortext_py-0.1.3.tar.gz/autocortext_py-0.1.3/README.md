## AutoCortext API CLient

This is a simple client for the AutoCortext API.

### Setup

1. An `.env` file with the variable `AUTOCORTEXT_API_KEY` set to a valid key.
1. An `.env` file with the variable `AUTOCORTEXT_ORG_ID` set to a valid organization ID.

### Example

Install the AutoCortext clinet using `pip`.

```shell
pip install autocortext-py
```

Use the client in your source code.

```python
from autocortext_py import AutoCortext
import os

query = '[{ "id":1, "content":"How can I assist you today?" ,"role":"assistant"}, { "id":2, "content":"The 24 volt power system for the conveyor is not powering on.","role":"user"}]'

client = AutoCortext()
res = client.troubleshoot(query)
print(res)
```
