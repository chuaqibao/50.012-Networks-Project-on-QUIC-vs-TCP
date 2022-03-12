# Experiment Results for Connection Establishment

## Introduction

After running the experiments to generate the pcap files, [pcapfix](https://f00l.de/hacking/pcapfix.php), an open-source tool, is used to analyse the pcap files. The original pcap generated via `tcpdump` cannot be analysed via [Wireshark](https://www.wireshark.org/) or `tcpdump`. This is because the packet size is too large and there is a packet size limit for both tools. Hence, [pcapfix](https://f00l.de/hacking/pcapfix.php) or [pyshark](https://github.com/KimiNewt/pyshark) can be used. In our analysis, we used pcapfix to fragment the large packets into smaller packets, allowing us to analyse via pyshark.


### Understanding the Contents in Each File

The original pcap files generated via `tcpdump` after running the scripts are [tcp_10_test.pcap](https://github.com/24kmystique/QUIC-vs-TCP-Protocol/blob/main/experiment%20results/connection%20establishment/tcp_10_test.pcap) and [quic_10_test.pcap](https://github.com/24kmystique/QUIC-vs-TCP-Protocol/blob/main/experiment%20results/connection%20establishment/quic_10_test.pcap). 

The final pcap files used to analyse the packets are [tcp_10_test_fixed.pcap](https://github.com/24kmystique/QUIC-vs-TCP-Protocol/blob/main/experiment%20results/connection%20establishment/tcp_10_test_fixed.pcap) and [quic_10_test_fixed.pcap](https://github.com/24kmystique/QUIC-vs-TCP-Protocol/blob/main/experiment%20results/connection%20establishment/quic_10_test_fixed.pcap).
