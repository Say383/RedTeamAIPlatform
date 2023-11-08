import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ThreatFeed:
    def __init__(self, feed_urls):
        self.feed_urls = feed_urls

    def gather_intelligence(self):
        """Gathers threat intelligence from various feeds."""
        all_feeds_data = []
        for url in self.feed_urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                feed_data = response.json()
                all_feeds_data.append(feed_data)
                logging.info(f"Threat intelligence gathered from {url}")
            except requests.RequestException as e:
                logging.error(f"Error gathering threat intelligence: {e}")
        return all_feeds_data

# Example usage
if __name__ == "__main__":
    feed_urls = [
        'https://threatfeed.example.com/feed.json',
        # ... other feed URLs
    ]
    threat_feed = ThreatFeed(feed_urls)
    try:
        threat_intelligence = threat_feed.gather_intelligence()
    except Exception as e:
        logging.error(f"Threat intelligence gathering error: {e}")
