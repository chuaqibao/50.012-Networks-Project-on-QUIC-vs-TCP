from sys import argv
from typing import List, Dict, Tuple
import json

# Hardcoded file sizes
quic_packet_length = 1288

def calculate(packets: List[Dict]) -> Tuple[int, float]:
    client = packets[0]['src']
    server = packets[0]['dst']
    start = packets[0]['timestamp']
    end_handshake = -1
    prev_src = None
    prev_dst = None
    packets_count = len(packets)
    handshake_rtts = 0

    for i in range(1, packets_count):
        _src = packets[i]['src']
        _dst = packets[i]['dst']

        if (_src == server) and (_dst == client) and \
           (_src != prev_src) and (_dst != prev_dst):
            handshake_rtts += 1
            end_handshake = packets[i]['timestamp']

        prev_src = _src
        prev_dst = _dst

    return handshake_rtts, (end_handshake - start) / handshake_rtts

if __name__ == "__main__":
    packets_json, output_file = argv[1:]

    # Read packets from json file
    with open(packets_json, 'r') as f:
        packets_data = json.load(f)

    overall_rtt = 0
    total_tests = len(packets_data)
    individual_test_results = {}
    overall_results = {}

    # Get results
    for test, packets in packets_data.items():
        handshake_rtts, average_rtt = calculate(packets)
        individual_test_results[test] = {
            'handshake_rtts': handshake_rtts,
            'average_rtt': average_rtt,
        }
        overall_rtt += average_rtt

    # Get overall average RTT
    overall_avg_rtt = overall_rtt / total_tests

    overall_results = {
        'total_tests': total_tests,
        'overall_avg_rtt': overall_avg_rtt,
        'individual_test_results': individual_test_results
    }

    # Write output to json file
    with open(output_file, 'w') as outfile:
        json.dump(overall_results, outfile, indent=4)
    