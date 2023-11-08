from cryptography.fernet import Fernet
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format=''%(asctime)s - %(levelname)s - %(message)s')

class DataEncryptor:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data):
        """Encrypts the given data."""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        logging.info("Data encrypted successfully.")
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """Decrypts the given data."""
        decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
        logging.info("Data decrypted successfully.")
        return decrypted_data

    def save_key_to_file(self, file_path):
        """Saves the encryption key to a file."""
        try:
            with open(file_path, 'wb') as file:
                file.write(self.key)
            logging.info(f"Key saved to {file_path}")
        except IOError as e:
            logging.error(f"Failed to save key: {e}")

    def load_key_from_file(self, file_path):
        """Loads the encryption key from a file."""
        try:
            with open(file_path, 'rb') as file:
                self.key = file.read()
                self.cipher_suite = Fernet(self.key)
            logging.info(f"Key loaded from {file_path}")
        except IOError as e:
            logging.error(f"Failed to load key: {e}")

    def encrypt_file(self, file_path):
        """Encrypts the contents of a file."""
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            encrypted_data = self.encrypt_data(file_data.decode())
            with open(file_path + '.enc', 'wb') as file:
                file.write(encrypted_data)
            logging.info(f"File encrypted: {file_path}")
        except IOError as e:
            logging.error(f"Failed to encrypt file: {e}")

# Example usage
if __name__ == "__main__":
    encryptor = DataEncryptor()
    sensitive_data = "Sensitive information to be encrypted"
    try:
        encrypted_data = encryptor.encrypt_data(sensitive_data)
        print(f"Encrypted Data: {encrypted_data}")
        decrypted_data = encryptor.decrypt_data(encrypted_data)
        print(f"Decrypted Data: {decrypted_data}")
    except Exception as e:
        logging.error(f"Encryption error: {e}")
