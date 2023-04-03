# Python library interaction with openVPN manager interface

Futures:
- Async

# Example

```python
import asyncio

from py_ovpn_mi import VPNManager

async def main():
    a = VPNManager(host="127.0.0.1", port=80)
    await a.connect()

asyncio.run(main())

# Exceptions: ConnectionError
```

# Development

Links:
- https://openvpn.net/community-resources/management-interface/
- https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/

