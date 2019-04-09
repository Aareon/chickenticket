from enum import Enum
from typing import List


class NetworkID(Enum):
    Main = 0
    Test = 1
    Reg = 2


class Command(Enum):
    Hello = 0x0000
    Ping = 0x0001
    GetVer = 0x0002
    AnnTx = 0x0003
    AnnSelf = 0x0004
    GetBlocksSince = 0x0005
    GetMempool = 0x0006


class MessageHeader:
    __slots__ = ("network", "command", "payload_size", "checksum")

    def __init__(self, network_id: NetworkID, command: Command, payload_size: int, checksum: int):
        self.network: int = network_id.value()
        self.command: int = command.value()
        self.payload_size = payload_size
        self.checksum = checksum
