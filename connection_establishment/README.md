# Experiment Setup for Connection Establishment

## Running the Experiment

### Steps to Run the Experiments for TCP and QUIC
1. At the start of the test for TCP, netem is used to configure network parameters such as bandwidth and delay
2. Start capturing network packets with tcpdump
3. Create a subprocess that runs a command to download the server’s html file. For TCP, wget is used while for QUIC, the chromium client is used. This command is repeated 10 times
4. Kill the process and stop the network capture. The resulting pcap file is used to analyse the handshake and packets exchanged between the client and server
5. Repeat steps 1-5 for QUIC


### Run and Analyse

#### Usage

```shell
./scripts/env_setup.sh
./scripts/run,sh
./scripts/analyse.sh
```

#### The Emulating Enviroments

1. Control Parameters
  **bandwidths** : Limiting the maximum link bitrate.
  **delay** : One-way delay to packets that are going from a server to client.
  **losses** : Drop packets that are going from a server to client.
  **spikes** : A period of time(default 200ms) when bandwidth drop to a certain percentage.
2. Parameters with values used in our experiments
  ```
  protocal = ['quic'] # change to 'tcp' when running the experiment for TCP
  bandwidths = ['100', '40', '5']
  delay = ['10', '50'] or ['10', '20', '40', '60', '80', '100', '120']
  losses = ['0.0', '5.0']
  ```

#### Details

1. Generate raw data
  This function is finished in `run_benchmark.py`, the scripts include three steps:
  * Generate the `Params Queue` from the arguments parsing
  * Configuration of local loopback interface for every params
  * Data captured with *tcpdump*, and stored into `./raw/` for every params.
2. Data Analysis  
  Use [pcapfix](https://f00l.de/hacking/pcapfix.php), an open-source tool, to analyse the pcap files. The original pcap generated via `tcpdump` cannot be analysed via [Wireshark](https://www.wireshark.org/) or `tcpdump`. This is because the packet size is too large and there is a packet size limit for both tools. Hence, [pcapfix](https://f00l.de/hacking/pcapfix.php) or [pyshark](https://github.com/KimiNewt/pyshark) can be used. In our analysis, we used pcapfix to fragment the large packets into smaller packets, allowing us to analyse via pyshark.

#### Debug
If the files labelled as "downloadx", where x is the test case number, in `tmp` [folder](https://github.com/24kmystique/QUIC-vs-TCP-Protocol/blob/main/connection_establishment/tmp) has a response code 404, `cd /tmp/quic-data` and include this in the file header: `X-Original-Url: https://www.example.org/`. 


## References

1. https://www.chromium.org/quic/playing-with-quic
2. http://cizixs.com/2017/10/23/tc-netem-for-terrible-network
3. http://linuxwiki.github.io/NetTools/tcpdump.html
4. http://dmdgeeker.com/post/tcpdump-basic-usage/
5. https://f00l.de/hacking/pcapfix.php
6. https://blogs.keysight.com/blogs/tech/nwvs.entry.html/2021/07/17/looking_into_quicpa-pUtF.html 
7. https://datatracker.ietf.org/doc/html/rfc9000
8. https://github.com/KimiNewt/pyshark 