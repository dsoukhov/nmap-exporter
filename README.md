# nmap Prometheus Exporter
WIP nmap prometheus exporter to check if hosts are up

## Usage
* `pip3 install -r requirements.txt`
* `sudo python3 main.py <cfgfile> (default: ./nmap-prober.yml)`
Service runs on default port 7777

## Querying prometheus
You can use the following Prometheus query to get up status of hosts
* `nmap_host_up`
