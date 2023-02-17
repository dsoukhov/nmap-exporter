from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import time
import subprocess
import sys
import os
import yaml
from xml.etree import ElementTree

class NmapCollector(object):
    @staticmethod
    def collect():
        g = GaugeMetricFamily(
            'nmap_host_up',
            'Up status of hosts (hosts are labels)',
            labels=["host"]
        )
        for host in config["hosts"]:
            print("nmap scan on {}".format(host))
            ip, port = host.split(":")
            filename = f"/tmp/nmap-exporter-output-{time.time()}"

            subprocess.Popen(
                ["nmap", "-oX", filename, "-sTU", "-Pn", "-p", port, ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ).wait()

            root_node = ElementTree.parse(filename).getroot()
            up_cnt = root_node.find("runstats").find("hosts").attrib["up"]
            g.add_metric([host], int(up_cnt))
            os.remove(filename)
            yield g

if __name__ == '__main__':
    cfgfile = sys.argv[1] if len(sys.argv) > 1 else "./nmap-prober.yml"
    with open(cfgfile, "r") as f:
        config = yaml.safe_load(f)
    if not config or type(config) is not dict:
        print("Unable to load config {}".format(cfgfile), file=sys.stderr)
        exit(0)
    print("running nmap prober on port {}".format(config["service_port"]))
    REGISTRY.register(NmapCollector)
    start_http_server(int(config["service_port"]))
    while True:
        time.sleep(1000)
