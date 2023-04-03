import unittest
from unittest.mock import AsyncMock

from py_ovpn_mi import VPNManager


class TestVpnManager(unittest.IsolatedAsyncioTestCase):
    async def test_cmd_kill(self):
        obj = VPNManager(host="127.0.0.1", port=1234)

        with self.subTest("Unknown"):
            obj.send_command = AsyncMock(return_value="")
            r = await obj.cmd_kill("test")
            self.assertEqual(r.status, "ERROR")

        with self.subTest("OK"):
            obj.send_command = AsyncMock(
                return_value="SUCCESS: common name 'd.test' found, 1 client(s) killed"  # noqa: E501
            )
            r = await obj.cmd_kill("test")
            self.assertEqual(r.status, "SUCCESS")

        with self.subTest("Error"):
            obj.send_command = AsyncMock(
                return_value="ERROR: common name 'd.test' not found"
            )
            r = await obj.cmd_kill("test")
            self.assertEqual(r.status, "ERROR")
