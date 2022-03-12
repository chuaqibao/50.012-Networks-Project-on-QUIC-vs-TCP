from os import write
import pyshark
from sys import argv
from typing import Dict, List
from pprint import pp
import json

protocol = ''

def read_packets(pcap: pyshark.FileCapture) -> List[Dict]:
    packets = []

    for pkt in pcap:
        if protocol == 'quic' and hasattr(pkt, 'udp'):
            udp_fields = pkt.udp._all_fields
            packet_info = {
                'timestamp': float(pkt.sniff_timestamp),
                #'time_relative': float(udp_fields['udp.time_relative']),
                'src': udp_fields['udp.srcport'],
                'dst': udp_fields['udp.dstport'],
                'packet_length': int(pkt.length)
            }

            quic_fields = pkt.quic._all_fields

            if 'quic.header_form' in quic_fields.keys():
                packet_info['header'] = int(quic_fields['quic.header_form'])
            if 'quic.connection.number' in quic_fields.keys():
                packet_info['connection_number'] = quic_fields['quic.connection.number']
            if 'quic.dcid' in quic_fields.keys():
                packet_info['dcid'] = quic_fields['quic.dcid']
            if 'quic.scid' in quic_fields.keys():
                packet_info['scid'] = quic_fields['quic.scid']
            if 'quic.packet_number' in quic_fields.keys():
                packet_info['packet_number'] = quic_fields['quic.packet_number']
            if 'quic.long.packet_type' in quic_fields.keys():
                packet_info['long_packet_type'] = quic_fields['quic.long.packet_type']
            if 'quic.long.reserved' in quic_fields.keys():
                packet_info['long_reserved_bits'] = quic_fields['quic.long.reserved']

            packets.append(packet_info)

        elif protocol == 'tcp':
            tcp_fields = pkt.tcp._all_fields
            packet_info = {
                'timestamp': float(pkt.sniff_timestamp),
                # 'time_relative': float(tcp_fields['tcp.time_relative']),
                'src': int(pkt.tcp.srcport),
                'dst': int(pkt.tcp.dstport),
                'seq_num': int(tcp_fields['tcp.seq']),
                'ack_num': int(tcp_fields['tcp.nxtseq']),
                'flags': tcp_fields['tcp.flags.str'].replace(u'\u00b7', '-')
            }
            packets.append(packet_info)
        else:
            continue

    return packets

def split_quic_tests(all_packets: List[Dict]) -> Dict:
    tests = {}
    packets = []
    i = 0
    conn_number = None
    test_label = ''

    for pkt in all_packets:
        # Check UDP connection number to determine if new test
        if ('connection_number' in pkt.keys() and pkt['connection_number'] != conn_number):
            if (len(packets) > 0):
                # Save packets from previous test
                test_label = "test_" + str(i)
                tests[test_label] = packets
                i += 1
                packets = []
            conn_number = pkt['connection_number']

        packets.append(pkt)

    # Save packets from last test
    test_label = "test_" + str(i)
    tests[test_label] = packets

    print(len(tests))
    return tests

def split_tcp_tests(all_packets: List[Dict]) -> Dict:
    tests = {}
    packets = []
    i = 0
    conn_tup = (-1, -1)

    for pkt in all_packets:
        # Check TCP source and destination tuple to determine if new test
        pkt_src = pkt['src']
        pkt_dest = pkt['dst']
        pkt_tup = (pkt_src, pkt_dest)
        
        if (sorted(conn_tup) != sorted(pkt_tup)):
            if (len(packets) > 0):
                # Save packets from previous test
                test_label = str(sorted(conn_tup))
                tests[test_label] = packets
                i += 1
                packets = []
            conn_tup = pkt_tup
        else:
            packets.append(pkt)
    return tests

def split_tests(all_packets: List[Dict]) -> Dict:
    if protocol == 'quic':
        tests = split_quic_tests(all_packets)
    else:
        tests = split_tcp_tests(all_packets)
    return tests

def get_handshake_packets(test_packets_dict: Dict) -> Dict:
    handshake_packets_dict = {}

    for test_key in test_packets_dict.keys():
        test_handshake_packets = []
        for pkt in test_packets_dict[test_key]:
            if protocol == 'quic' and pkt['header'] == 1:
                test_handshake_packets.append(pkt)
        handshake_packets_dict[test_key] = test_handshake_packets

    return handshake_packets_dict

def print_packets(packets_dict: Dict) -> None:
    for label in packets_dict.keys():
        print("\nPackets from " + label)
        for packet in packets_dict[label]:
            pp(packet)

def write_packets(packets_dict: Dict, output_file: str) -> None:
    with open(output_file, "w") as outfile:
        json.dump(packets_dict, outfile, indent=4)

if __name__ == "__main__":
    protocol, pcap_path, output_file = argv[1:]
    protocol = protocol.lower()

    print("Reading " + protocol + " packets...")

    pcap = pyshark.FileCapture(pcap_path)
    packets = read_packets(pcap)
    test_packets_dict = split_tests(packets)
    hs_packets_dict = get_handshake_packets(test_packets_dict)
    write_packets(hs_packets_dict, output_file)
