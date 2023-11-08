import logging
import re
import os
import argparse
import subprocess
import sqlite3
import smtplib
import logging
from email.mime.text import MIMEText
from datetime import datetime

# Initialize the logger
logging.basicConfig(filename='nmap_parser.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Define command-line arguments
parser = argparse.ArgumentParser(description="Nmap Parser Tool")
parser.add_argument("--target", required=True, help="Target IP or range")
parser.add_argument("--output", required=True, help="Output file for scan results")
parser.add_argument("--custom-script", help="Path to custom Nmap script")
parser.add_argument("--email", help="Email address for notifications")
args = parser.parse_args()

# Function to run an Nmap scan
def run_nmap_scan(target, output_file, custom_script=None):
    command = ["nmap", "-oX", output_file]
    
    if custom_script:
        command.extend(["--script", custom_script])
    
    command.append(target)
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        logging.error(f"Nmap scan failed for target: {target}")
        raise Exception("Nmap scan failed.")
        
import re
import logging

# Initialize the logger
logging.basicConfig(filename='nmap_parser.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Function to parse Nmap scan results
def parse_nmap_output(nmap_output):
    results = []
    try:
        # Split the Nmap output into individual lines
        lines = nmap_output.split('\n')

        current_host = None
        current_port = None
        current_service = None

        for line in lines:
            # Detect the start of a new host section
            if re.match(r'^Nmap scan report for', line):
                if current_host:
                    results.append({
                        'host': current_host,
                        'port': current_port,
                        'service': current_service,
                    })
                current_host = line.split()[-1]
                current_port = None
                current_service = None
            elif re.match(r'^\d+/\w+', line):
                # Parse port and service information
                port_info = line.split()
                current_port = port_info[0].split('/')[0]
                current_service = port_info[-1]

        # Append the last host's information
        if current_host:
            results.append({
                'host': current_host,
                'port': current_port,
                'service': current_service,
            })

        logging.info("Parsed Nmap scan results")
        return results
    except Exception as e:
        logging.error(f"Failed to parse Nmap output. Error: {str(e)}")
        raise Exception("Failed to parse Nmap scan results")

# Function to save parsed results to a file
def save_results_to_file(results, output_file):
    try:
        with open(output_file, 'w') as file:
            for result in results:
                file.write(f"Host: {result['host']}, Port: {result['port']}, Service: {result['service']}\n")
        logging.info(f"Saved parsed Nmap results to {output_file}")
    except Exception as e:
        logging.error(f"Failed to save parsed results to {output_file}. Error: {str(e)}")
        raise Exception(f"Failed to save parsed results to {output_file}")

# Function to parse Nmap scan results
def parse_nmap_output(nmap_output):
    results = []
    try:
        # Split the Nmap output into individual lines
        lines = nmap_output.split('\n')

        current_host = None
        current_port = None
        current_service = None

        for line in lines:
            # Detect the start of a new host section
            if re.match(r'^Nmap scan report for', line):
                if current_host:
                    results.append({
                        'host': current_host,
                        'port': current_port,
                        'service': current_service,
                    })
                current_host = line.split()[-1]
                current_port = None
                current_service = None
            elif re.match(r'^\d+/\w+', line):
                # Parse port and service information
                port_info = line.split()
                current_port = port_info[0].split('/')[0]
                current_service = port_info[-1]

        # Append the last host's information
        if current_host:
            results.append({
                'host': current_host,
                'port': current_port,
                'service': current_service,
            })

        logging.info("Parsed Nmap scan results")
        return results
    except Exception as e:
        logging.error(f"Failed to parse Nmap output. Error: {str(e)}")
        raise Exception("Failed to parse Nmap scan results")

# Function to save parsed results to a file
def save_results_to_file(results, output_file):
    try:
        with open(output_file, 'w') as file:
            for result in results:
                file.write(f"Host: {result['host']}, Port: {result['port']}, Service: {result['service']}\n")
        logging.info(f"Saved parsed Nmap results to {output_file}")
    except Exception as e:
        logging.error(f"Failed to save parsed results to {output_file}. Error: {str(e)}")
        raise Exception(f"Failed to save parsed results to {output_file}")

# Main function
if __name__ == "__main__":
    target = args.target
    output_file = args.output
    custom_script = args.custom_script
    email = args.email
    
    try:
        # Create a timestamp for the scan
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Run the Nmap scan
        run_nmap_scan(target, output_file, custom_script)
        
        # Parse the scan output
        scan_results = parse_nmap_output(output_file)
        
        # If an email address is provided, send a notification
        if email:
            subject = f"Nmap Scan Completed for {target}"
            message = f"The Nmap scan for {target} completed at {timestamp}.\nResults: {scan_results}"
            send_email(subject, message, email)
            
        logging.info(f"Nmap scan completed for target: {target}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"An error occurred: {str(e)}")
