import paramiko
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureComm:
    def __init__(self, server_ip, username, key_file):
        self.server_ip = server_ip
        self.username = username
        self.key_file = key_file
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def establish_communication(self):
        """Establishes a secure SSH communication channel."""
        try:
            self.ssh_client.connect(hostname=self.server_ip, username=self.username, key_filename=self.key_file)
            logging.info(f"Secure communication established with {self.server_ip}")
        except Exception as e:
            logging.error(f"Failed to establish secure communication: {e}")
            raise

    def send_command(self, command):
        """Sends a command over the established secure channel."""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.read()

# Example usage
if __name__ == "__main__":
    comm = SecureComm('server_ip', 'username', '/path/to/private/key')
    try:
        comm.establish_communication()
        result = comm.send_command('id')
        logging.info(f"Command output: {result.decode().strip()}")
    except Exception as e:
        logging.error(f"Secure communication error: {e}")
    finally:
        comm.ssh_client.close()
