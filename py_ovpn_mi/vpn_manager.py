import asyncio
from typing import Optional

from .model import OVInfo, CmdResponse


class VPNManager:

    # default_timeout = 5  # seconds

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        unix_socket: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self._host = host
        self._port = port
        self._unix_socket = unix_socket
        # self._timeout = timeout or self.default_timeout

        self._stream_reader: asyncio.StreamReader = None
        self._stream_writer: asyncio.StreamWriter = None

        self._check_connect()

    def _check_connect(self):
        if (
            (self._host is None or self._port is None) and
            self._unix_socket is None
        ):
            raise ValueError("Host or unix_socket must be set")

    async def send_command(self, command: str) -> str:
        """Send command to openvpn management interface and return response"""
        if self._stream_reader is None or self._stream_writer is None:
            await self.connect()

        self._stream_writer.write(command.encode())
        await self._stream_writer.drain()

        response = await self._stream_reader.read(-1)
        return response.decode()

    async def connect(self):
        if self._unix_socket is not None:
            reader, writer = await asyncio.open_unix_connection(
                self._unix_socket
            )
        else:
            reader, writer = await asyncio.open_connection(
                self._host, self._port
            )
        self._stream_reader, self._stream_writer = reader, writer

    async def close(self):
        self._stream_writer.close()
        await self._stream_writer.wait_closed()

    async def cmd_status(self) -> OVInfo:
        """Send status command to openvpn management interface

        Format, --status-version [n], we uses 2
        2 -- a more reliable format for external processing.
        Compared to version 1, the client list contains some additional fields:
        Virtual Address, Virtual IPv6 Address, Username, Client ID, Peer ID.
        Future versions may extend the number of fields.
        """
        return OVInfo.create_from_str(await self.send_command("status 2"))

    async def cmd_kill(self, common_name: str) -> CmdResponse:
        """Send kill command to openvpn management interface

        Example:
        SUCCESS: common name 'd.test' found, 1 client(s) killed

        """
        answer = await self.send_command(f"kill {common_name}")

        answer = answer.strip()
        if answer.startswith("SUCCESS:"):
            return CmdResponse(status="SUCCESS", message=answer[8:].strip())
        elif answer.startswith("ERROR:"):
            return CmdResponse(status="ERROR", message=answer[6:].strip())
        return CmdResponse(status="ERROR", message=f"Unknown error: {answer}")
