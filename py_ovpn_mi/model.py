import dataclasses
from enum import Enum
from datetime import datetime
from typing import List, Optional


class Status(Enum):
    """Status of openvpn management interface"""
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


@dataclasses.dataclass
class CmdResponse:
    """Answer from openvpn management interface"""
    status: Status
    message: str


@dataclasses.dataclass
class Client:
    """Openvpn client"""
    common_name: str
    real_address: str
    virtual_address: str
    virtual_ipv6_address: str
    bytes_received: int
    bytes_sent: int
    connected_since: datetime
    username: str
    client_id: int
    peer_id: int


@dataclasses.dataclass
class OVInfo:
    """Openvpn info"""
    title: str
    time: Optional[datetime] = None
    clients: List[Client] = dataclasses.field(default_factory=list)

    @staticmethod
    def create_from_str(data: str) -> "OVInfo":
        """Parse openvpn info

        Raises:
            ValueError: If error in format

        Example:
        TITLE,OpenVPN 2.4.12 x86_64-redhat-linux-gnu [Fedora EPEL patched] [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Mar 17 2022
        TIME,Fri Mar 31 15:54:52 2023,1680267292
        HEADER,CLIENT_LIST,Common Name,Real Address,Virtual Address,Virtual IPv6 Address,Bytes Received,Bytes Sent,Connected Since,Connected Since (time_t),Username,Client ID,Peer ID
        CLIENT_LIST,d.test,25.13.19.12:1194,172.20.100.17,,18229,7921,Fri Mar 31 15:54:33 2023,1680267273,UNDEF,7310,0
        HEADER,ROUTING_TABLE,Virtual Address,Common Name,Real Address,Last Ref,Last Ref (time_t)
        ROUTING_TABLE,172.20.100.17,d.test,95.53.79.72:1194,Fri Mar 31 15:54:44 2023,1680267284
        GLOBAL_STATS,Max bcast/mcast queue length,0
        END
        """
        title = ""
        time = None
        clients = []

        for line in data.splitlines():
            line = line.strip()

            if line.startswith("TITLE,"):
                title = line.split(",", 2)[1]
                continue
            if line.startswith("TIME,"):
                time = datetime.strptime(
                    line.split(",", 2)[1], "%a %b %d %H:%M:%S %Y")
                continue
            if line.startswith("CLIENT_LIST,"):
                line = line.split(",")
                client = Client(
                    common_name=line[1],
                    real_address=line[2].split(":")[0],  # 1.2.3.4:1194
                    virtual_address=line[3],
                    virtual_ipv6_address=line[4],
                    bytes_received=int(line[5]),
                    bytes_sent=int(line[6]),
                    connected_since=datetime.strptime(
                        line[7], "%a %b %d %H:%M:%S %Y"
                    ),
                    username=line[9],
                    client_id=int(line[10]),
                    peer_id=int(line[11]),
                )
                clients.append(client)
                continue
        return OVInfo(title=title, time=time, clients=clients)
