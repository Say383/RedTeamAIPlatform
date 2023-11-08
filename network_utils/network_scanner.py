import nmap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkScanner:
    def __init__(self):
        self.scanner = nmap.PortScanner()

    def scan_hosts(self, network_range):
        """Scans the network range for active hosts."""
        logging.info(f"Scanning for active hosts in the network range: {network_range}")
        self.scanner.scan(hosts=network_range, arguments='-sn')
        active_hosts = [(x, self.scanner[x]['status']['state']) for x in self.scanner.all_hosts() if self.scanner[x]['status']['state'] == 'up']
        logging.info(f"Active hosts: {active_hosts}")
        return active_hosts

    def scan_ports(self, target_ip):
        """Scans the target IP for open ports and services."""
        logging.info(f"Scanning {target_ip} for open ports and services.")
        self.scanner.scan(hosts=target_ip, arguments='-sV')
        scan_data = self.scanner[target_ip]
        for protocol in scan_data.all_protocols():
            lport = scan_data[protocol].keys()
            for port in lport:
                logging.info(f"Port {port} is {scan_data[protocol][port]['state']}, service: {scan_data[protocol][port]['name']}")
        return scan_data

# Example usage
if __name__ == "__main__":
    scanner = NetworkScanner()
    network = '192.168.1.0/24'
    try:
        hosts = scanner.scan_hosts(network)
        for host, status in hosts:
            if status == 'up':
                scanner.scan_ports(host)
    except Exception as e:
        logging.error(f"Network scanning failed: {e}")
