# web_interface.py

from flask import Flask, request, jsonify
import logging
from pentest_tools.scanner import NetworkScanner
from pentest_tools.exploiter import Exploiter
from pentest_tools.vulnerability_assessment import VulnerabilityAssessment
from pentest_tools.privilege_escalation import PrivilegeEscalator
from utilities.file_utils import save_results_to_file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the Flask app
app = Flask(__name__)

# Define a route for network scanning
@app.route('/scan-network', methods=['POST'])
def scan_network():
    network_scanner = NetworkScanner()
    targets = network_scanner.scan_network()
    logging.info(f"Scanned targets: {targets}")
    save_results_to_file("network_scan_results.txt", f"Scanned targets: {targets}")
    return jsonify({"message": "Network scan successful", "targets": targets}), 200

# Define a route for exploitation
@app.route('/exploit', methods=['POST'])
def exploit():
    data = request.json
    target = data.get('target')
    if target:
        exploiter = Exploiter()
        if exploiter.exploit_target(target):
            logging.info(f"Successfully exploited {target}")
            save_results_to_file("exploit_results.txt", f"Successfully exploited {target}")
            return jsonify({"message": f"Successfully exploited {target}"}), 200
        else:
            logging.warning(f"Failed to exploit {target}")
            save_results_to_file("exploit_results.txt", f"Failed to exploit {target}")
            return jsonify({"message": f"Failed to exploit {target}"}), 400
    else:
        return jsonify({"message": "Target not provided in the request"}), 400

# ... (Add routes for vulnerability assessment, privilege escalation, and other functionalities)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

