import pyshark
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TrafficAnalyzer:
    def __init__(self, interface='eth0', bpf_filter='tcp'):
        self.interface = interface
        self.bpf_filter = bpf_filter

    def analyze_traffic(self):
        """Analyzes network traffic on the specified interface using the given BPF filter."""
        capture = pyshark.LiveCapture(interface=self.interface, bpf_filter=self.bpf_filter)
        for packet in capture.sniff_continuously(packet_count=50):  # Example: Capture only 50 packets
            logging.info(f"Captured packet: {packet}")

# Example usage
if __name__ == "__main__":
    analyzer = TrafficAnalyzer()
    try:
        analyzer.analyze_traffic()
    except Exception as e:
        logging.error(f"Traffic analysis failed: {e}")
