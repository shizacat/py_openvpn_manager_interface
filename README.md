# Python library interaction with openVPN manager interface

Futures:
- Async
- Support tcp/unix_socket connection. ("unix:///path_socket", "tcp://host:port")

# Install

```bash
pip install ovpn-manager
```

# Example

```python
import asyncio

from py_ovpn_mi import VPNManager

async def main():
    a = VPNManager(url="tcp://127.0.0.1:80")
    await a.connect()

asyncio.run(main())

# Exceptions: ConnectionError
```

# Development

Links:
- https://openvpn.net/community-resources/management-interface/
- https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/

