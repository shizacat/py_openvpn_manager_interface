import datetime
import unittest

from ovpn_manager import model


class TestModel(unittest.TestCase):
    def test_ovinfo_create(self):
        r = model.OVInfo.create_from_str(
            """
            TITLE,OpenVPN 2.4.12 x86_64-redhat-linux-gnu [Fedora EPEL patched] [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Mar 17 2022
            TIME,Fri Mar 31 15:54:52 2023,1680267292
            HEADER,CLIENT_LIST,Common Name,Real Address,Virtual Address,Virtual IPv6 Address,Bytes Received,Bytes Sent,Connected Since,Connected Since (time_t),Username,Client ID,Peer ID
            CLIENT_LIST,d.test,25.13.19.12:1194,172.20.100.17,,18229,7921,Fri Mar 31 15:54:33 2023,1680267273,UNDEF,7310,0
            HEADER,ROUTING_TABLE,Virtual Address,Common Name,Real Address,Last Ref,Last Ref (time_t)
            ROUTING_TABLE,172.20.100.17,d.test,95.53.79.72:1194,Fri Mar 31 15:54:44 2023,1680267284
            GLOBAL_STATS,Max bcast/mcast queue length,0
            END
            """
        )
        self.assertEqual(
            r.title,
            "OpenVPN 2.4.12 x86_64-redhat-linux-gnu [Fedora EPEL patched] [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Mar 17 2022"
        )
        self.assertEqual(
            r.time,
            datetime.datetime(2023, 3, 31, 15, 54, 52)
        )
        self.assertEqual(len(r.clients), 1)

        # Check the first client
        self.assertEqual(r.clients[0].common_name, "d.test")
        self.assertEqual(r.clients[0].real_address, "25.13.19.12")
        self.assertEqual(r.clients[0].virtual_address, "172.20.100.17")
        self.assertEqual(r.clients[0].virtual_ipv6_address, "")
        self.assertEqual(r.clients[0].bytes_received, 18229)
        self.assertEqual(r.clients[0].bytes_sent, 7921)
        self.assertEqual(
            r.clients[0].connected_since,
            datetime.datetime(2023, 3, 31, 15, 54, 33)
        )
        self.assertEqual(r.clients[0].username, "UNDEF")
        self.assertEqual(r.clients[0].client_id, 7310)
        self.assertEqual(r.clients[0].peer_id, 0)

    def test_ovinfo_create_empty(self):
        r = model.OVInfo.create_from_str(
            """
            TITLE,OpenVPN 2.4.12 x86_64-redhat-linux-gnu [Fedora EPEL patched] [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Mar 17 2022
            TIME,Fri Mar 31 15:54:52 2023,1680267292
            HEADER,CLIENT_LIST,Common Name,Real Address,Virtual Address,Virtual IPv6 Address,Bytes Received,Bytes Sent,Connected Since,Connected Since (time_t),Username,Client ID,Peer ID
            HEADER,ROUTING_TABLE,Virtual Address,Common Name,Real Address,Last Ref,Last Ref (time_t)
            GLOBAL_STATS,Max bcast/mcast queue length,0
            END
            """
        )
        self.assertEqual(
            r.title,
            "OpenVPN 2.4.12 x86_64-redhat-linux-gnu [Fedora EPEL patched] [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Mar 17 2022"
        )
        self.assertEqual(
            r.time,
            datetime.datetime(2023, 3, 31, 15, 54, 52)
        )
        self.assertEqual(len(r.clients), 0)

    def test_ovinfo_create_invalid(self):
        with self.assertRaises(ValueError):
            model.OVInfo.create_from_str(
                """
                Connect since is not a date

                TITLE,OpenVPN 2.4.12 x86_64-redhat-linux-gnu [Fedora EPEL patched] [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Mar 17 2022
                TIME,Fri Mar 31 15:54:52 2023,1680267292
                HEADER,CLIENT_LIST,Common Name,Real Address,Virtual Address,Virtual IPv6 Address,Bytes Received,Bytes Sent,Connected Since,Connected Since (time_t),Username,Client ID,Peer ID
                CLIENT_LIST,d.test,25.13.19.121194,172.20.100.17,,18229,7921,test - no date,1680267273,UNDEF,7310,0
                HEADER,ROUTING_TABLE,Virtual Address,Common Name,Real Address,Last Ref,Last Ref (time_t)
                ROUTING_TABLE,172.20.100.17,d.test,95.53.79.72:1194,Fri Mar 31 15:54:44 2023,1680267284
                GLOBAL_STATS,Max bcast/mcast queue length,0
                END
                """
            )
