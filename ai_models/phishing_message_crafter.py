import argparse
from string import Template
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PhishingMessageCrafter:
    def __init__(self, template_path):
        self.template_path = template_path
        self.template = None
        self.load_template()

    def load_template(self):
        try:
            with open(self.template_path, 'r') as file:
                self.template = Template(file.read())
        except IOError as e:
            logger.error(f"Error reading template file: {e}")
            raise

    def craft_message(self, **kwargs):
        if not self.template:
            raise ValueError("Template has not been loaded properly.")
        return self.template.safe_substitute(**kwargs)

def main():
    parser = argparse.ArgumentParser(description="Phishing Message Crafter Tool for Red Team Training")
    parser.add_argument("--template", required=True, help="Path to the message template file")
    parser.add_argument("--output", required=True, help="Output file to save the crafted message")
    parser.add_argument("--variables", nargs='+', help="Variables to inject into the template. Format: key=value")

    args = parser.parse_args()
    
    # Parse the variables into a dictionary
    variables = {k: v for k, v in (var.split('=') for var in args.variables)}

    try:
        crafter = PhishingMessageCrafter(template_path=args.template)
        message = crafter.craft_message(**variables)
        
        with open(args.output, 'w') as file:
            file.write(message)
        
        logger.info(f"Crafted message has been saved to {args.output}")

    except Exception as e:
        logger.error(f"An error occurred while crafting the message: {e}")

if __name__ == "__main__":
    main()
