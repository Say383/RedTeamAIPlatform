import nmap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdvancedNetworkMapper:
    def __init__(self):
        self.scanner = nmap.PortScanner()

    def map_network(self, target_range):
        """Performs an advanced network mapping."""
        try:
            self.scanner.scan(hosts=target_range, arguments='-sV -sC -O -T4')
            for host in self.scanner.all_hosts():
                if self.scanner[host].state() == 'up':
                    logging.info(f"Host {host} is up.")
                    for proto in self.scanner[host].all_protocols():
                        lport = self.scanner[host][proto].keys()
                        for port in lport:
                            logging.info(f"Port {port} on {host} is {self.scanner[host][proto][port]['state']}")
        except nmap.PortScannerError as e:
            logging.error(f"Advanced network mapping failed: {e}")

# Example usage
if __name__ == "__main__":
    mapper = AdvancedNetworkMapper()
    try:
        mapper.map_network('192.168.1.0/24')
    except Exception as e:
        logging.error(f"Network mapping error: {e}")
