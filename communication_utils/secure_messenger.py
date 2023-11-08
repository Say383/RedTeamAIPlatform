from cryptography.fernet import Fernet
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureMessenger:
    def __init__(self, key):
        self.cipher_suite = Fernet(key)

    def encrypt_message(self, message):
        """Encrypts a message."""
        encrypted_message = self.cipher_suite.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        """Decrypts a message."""
        decrypted_message = self.cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message

# Example usage
if __name__ == "__main__":
    key = Fernet.generate_key()
    messenger = SecureMessenger(key)
    try:
        encrypted = messenger.encrypt_message("This is a secret message.")
        logging.info(f"Encrypted message: {encrypted}")
        decrypted = messenger.decrypt_message(encrypted)
        logging.info(f"Decrypted message: {decrypted}")
    except Exception as e:
        logging.error(f"Encryption/Decryption error: {e}")
