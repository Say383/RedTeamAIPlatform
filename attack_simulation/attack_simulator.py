import random
import time
import argparse
import logging

# Define the available attack types
ATTACK_TYPES = {
    "SQL Injection": {"payloads": ["' OR 1=1 --", "UNION SELECT * FROM users", "DELETE FROM products"]},
    "Cross-Site Scripting": {"payloads": ["<script>alert('XSS')</script>", "<img src='x' onerror='alert(\"XSS\")'>"]},
    "Brute Force": {"payloads": ["admin:password", "user:12345", "root:toor"]}
}

class AttackSimulator:
    def __init__(self, target_system, attack_type, num_simulations, attack_speed, verbose):
        self.target_system = target_system
        self.attack_type = attack_type
        self.num_simulations = num_simulations
        self.attack_speed = attack_speed
        self.verbose = verbose

    def simulate_attack(self):
        logging.info(f"Simulating {self.attack_type} attacks on {self.target_system}")

        for i in range(self.num_simulations):
            payload = random.choice(ATTACK_TYPES[self.attack_type]["payloads"])
            if self.verbose:
                logging.info(f"Attack {i + 1}/{self.num_simulations} - Payload: {payload}")
            time.sleep(self.attack_speed)
        
        logging.info(f"Attack simulation on {self.target_system} completed")

def main():
    parser = argparse.ArgumentParser(description="Simulate attacks on a target system.")
    parser.add_argument("target_system", help="The target system to attack.")
    parser.add_argument("--attack-type", choices=ATTACK_TYPES.keys(), default="SQL Injection",
                        help="Type of attack to simulate (default: SQL Injection)")
    parser.add_argument("--num-simulations", type=int, default=1,
                        help="Number of attack simulations")
    parser.add_argument("--attack-speed", type=float, default=1.0,
                        help="Attack speed in seconds per simulation")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose mode to display detailed information")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    simulator = AttackSimulator(args.target_system, args.attack_type, args.num_simulations, args.attack_speed, args.verbose)
    simulator.simulate_attack()

if __name__ == "__main__":
    main()
