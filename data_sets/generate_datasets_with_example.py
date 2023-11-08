import csv
import os
import random
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Constants for synthetic data generation
NETWORK_TRAFFIC_FEATURES = ['timestamp', 'source_ip', 'destination_ip', 'port', 'protocol', 'payload_size', 'flag', 'anomaly']
EXPLOIT_DATA_FEATURES = ['timestamp', 'exploit_type', 'target_service', 'success_probability']

# Directory structure constants
DATA_SETS_DIR = 'data_sets'
TRAINING_DATA_DIR = os.path.join(DATA_SETS_DIR, 'training_data')
VALIDATION_DATA_DIR = os.path.join(DATA_SETS_DIR, 'validation_data')

# Helper functions
def generate_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

def generate_port():
    return random.randint(1024, 65535)

def generate_protocol():
    return random.choice(['TCP', 'UDP', 'ICMP'])

def generate_payload_size():
    return random.randint(64, 1500)  # Typical payload size range in bytes

def generate_flag():
    return random.choice(['SYN', 'ACK', 'RST', 'FIN'])

def generate_anomaly():
    return random.choice([True, False])

def generate_exploit_type():
    return random.choice(['buffer_overflow', 'sql_injection', 'cross_site_scripting', 'privilege_escalation'])

def generate_target_service():
    return random.choice(['web_server', 'database', 'file_server', 'mail_server'])

def generate_success_probability():
    return round(random.uniform(0, 1), 2)

def create_network_traffic_data(num_records):
    records = []
    for _ in range(num_records):
        record = {
            'timestamp': datetime.now().isoformat(),
            'source_ip': generate_ip(),
            'destination_ip': generate_ip(),
            'port': generate_port(),
            'protocol': generate_protocol(),
            'payload_size': generate_payload_size(),
            'flag': generate_flag(),
            'anomaly': generate_anomaly()
        }
        records.append(record)
    return records

def create_exploit_data(num_records):
    records = []
    for _ in range(num_records):
        record = {
            'timestamp': datetime.now().isoformat(),
            'exploit_type': generate_exploit_type(),
            'target_service': generate_target_service(),
            'success_probability': generate_success_probability()
        }
        records.append(record)
    return records

def save_to_csv(records, headers, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

# Create synthetic data
network_traffic_data = create_network_traffic_data(1000)
exploit_data = create_exploit_data(1000)

# Ensure directories exist
os.makedirs(TRAINING_DATA_DIR, exist_ok=True)
os.makedirs(VALIDATION_DATA_DIR, exist_ok=True)

# Save data to CSV files
save_to_csv(network_traffic_data, NETWORK_TRAFFIC_FEATURES, os.path.join(TRAINING_DATA_DIR, 'network_traffic.csv'))
save_to_csv(exploit_data, EXPLOIT_DATA_FEATURES, os.path.join(TRAINING_DATA_DIR, 'exploit_data.csv'))

# Load the data into a pandas DataFrame
network_traffic_df = pd.read_csv(os.path.join(TRAINING_DATA_DIR, 'network_traffic.csv'))
exploit_data_df = pd.read_csv(os.path.join(TRAINING_DATA_DIR, 'exploit_data.csv'))

# Example: Using network_traffic_df for anomaly detection
# This is a placeholder for actual feature and label preparation
X = network_traffic_df.drop('anomaly', axis=1)  # Features
y = network_traffic_df['anomaly']  # Labels

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create a model and train it
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
print("Model accuracy:", model.score(X_test, y_test))
