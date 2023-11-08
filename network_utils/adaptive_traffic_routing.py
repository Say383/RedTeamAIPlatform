import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdaptiveTrafficRouter:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    def send_through_proxy(self, target_url):
        """Sends a request to the target URL through a randomly chosen proxy."""
        proxy = random.choice(self.proxy_list)
        try:
            response = requests.get(target_url, proxies={"http": proxy, "https": proxy})
            logging.info(f"Request sent through proxy {proxy} received response: {response.status_code}")
        except Exception as e:
            logging.error(f"Adaptive traffic routing failed: {e}")

# Example usage
if __name__ == "__main__":
    router = AdaptiveTrafficRouter(['http://proxy1:8080', 'http://proxy2:8080'])
    try:
        router.send_through_proxy('http://target_url')
    except Exception as e:
        logging.error(f"Traffic routing error: {e}")
