from types import LambdaType
from typing import Literal
import common
BINARY, *_ = common.get_input(__file__, lambda line: bin(int(line.strip(), 16))[2:])

import dataclasses
from typing import List, Union

@dataclasses.dataclass
class Packet:
    version: int
    type: int

@dataclasses.dataclass
class LiteralPacketContent:
    value: int

@dataclasses.dataclass
class LiteralPacket(Packet, LiteralPacketContent):
    ...

@dataclasses.dataclass
class OperatorPacketContent:
    sub_packets: List[Union['OperatorPacket', LiteralPacket]]

@dataclasses.dataclass
class OperatorPacket(Packet, OperatorPacketContent):
    ...

    @property
    def value(self) -> int:
        packet_value_iter = (
            packet.value
            for packet in
            self.sub_packets
        )

        match self.type:
            case 0:
                return sum(packet_value_iter)
            case 1:
                import math
                return math.prod(packet_value_iter)
            case 2:
                # Min
                return min(packet_value_iter)
            case 3:
                # Max
                return max(packet_value_iter)
            case 5:
                # >
                return (
                    1 if self.sub_packets[0].value > self.sub_packets[1].value else 0
                )
            case 6:
                # <
                return (
                    1 if self.sub_packets[0].value < self.sub_packets[1].value else 0
                )
            case 7:
                # ==
                return (
                    1 if self.sub_packets[0].value == self.sub_packets[1].value else 0
                )

import itertools

def take(stream, num: int) -> str:
    return ''.join(itertools.islice(stream, num))

def parse_literal_packet(binary: str) -> LiteralPacketContent:
    binary_stream = iter(binary)

    value_bin = ""
    while chunk := take(binary_stream, 5):
        value_bin += chunk[1:]
        if chunk[0] == '0':
            break

    value = int(value_bin, 2)

    return LiteralPacketContent(
        value=value,
    )

def parse_operator_packet(binary: str) -> OperatorPacketContent:
    binary_stream = iter(binary)

    length_type_id = int(next(binary_stream))
    if length_type_id == 0:
        # the next 15 bits are a number that represents the
        # total length in bits of the sub-packets contained by this packet.
        num_subpacket_bits = int(take(binary_stream, 15), 2)
        subpacket_string = take(binary_stream, num_subpacket_bits)
        subpacket_string_iter = iter(subpacket_string)
        sub_packets = parse_packets(subpacket_string_iter)

    else:
        # the next 11 bits are a number that represents the
        # number of sub-packets immediately contained by this packet.
        num_subpackets = int(take(binary_stream, 11), 2)
        sub_packets = [
            parse_next_packet(binary_stream)
            for _ in range(num_subpackets)
        ]

    return OperatorPacketContent(sub_packets=sub_packets)

def parse_next_packet(binary: str) -> Packet:
    binary_stream = iter(binary)

    version = int(take(binary_stream, 3), 2)
    type = int(take(binary_stream, 3), 2)

    if type == 4:
        lpc = parse_literal_packet(binary_stream)
        return LiteralPacket(
            version=version,
            type=type,
            value=lpc.value,
        )
    else:
        opc = parse_operator_packet(binary_stream)
        return OperatorPacket(
            version=version,
            type=type,
            sub_packets=opc.sub_packets,
        )

def parse_packets(binary) -> List[Packet]:
    binary_stream = iter(binary)
    
    packets = []

    while '1' in (peek := take(binary_stream, 6)):
        binary_stream = itertools.chain(peek, binary_stream)
        packets.append(parse_next_packet(binary_stream))
    return packets

packets = parse_packets(BINARY)

packet_version_sum = 0
def sum_packet_versions(packets: List[Packet]):
    packet_version_sum = 0
    for packet in packets:
        packet_version_sum += packet.version
        if isinstance(packet, OperatorPacket):
            packet_version_sum += sum_packet_versions(packet.sub_packets)
    return packet_version_sum

print("Part 1:", sum_packet_versions(packets))
print("Part 2:", packets[0].value)
