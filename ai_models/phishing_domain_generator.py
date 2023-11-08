import argparse
import logging
import random
import string

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PhishingDomainGenerator:
    def __init__(self, tld, wordlist, count):
        self.tld = tld
        self.wordlist = wordlist
        self.count = count

    def generate_domains(self):
        domains = []
        for _ in range(self.count):
            random_word = ''.join(random.choices(self.wordlist, k=random.randint(3, 10)))
            domain = f"{random_word}.{self.tld}"
            domains.append(domain)
        return domains

    def save_domains(self, domains, filename):
        try:
            with open(filename, 'w') as file:
                for domain in domains:
                    file.write(domain + '\n')
            logger.info(f"Domains have been saved to {filename}")
        except IOError as e:
            logger.error(f"Unable to write to file {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Phishing Domain Generator Tool")
    parser.add_argument("--tld", required=True, help="Top-level domain to use for the generated domains")
    parser.add_argument("--wordlist", required=True, type=str, help="Path to the wordlist file")
    parser.add_argument("--count", type=int, default=10, help="Number of domains to generate")
    parser.add_argument("--output", required=True, help="Output file to save the generated domains")
    args = parser.parse_args()

    try:
        # Read the wordlist
        with open(args.wordlist, 'r') as file:
            wordlist = [line.strip() for line in file.readlines()]

        generator = PhishingDomainGenerator(tld=args.tld, wordlist=wordlist, count=args.count)
        domains = generator.generate_domains()
        generator.save_domains(domains, args.output)

    except FileNotFoundError as e:
        logger.error(f"The wordlist file was not found: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
