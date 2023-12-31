import argparse
import sys
import logging
import requests
import joblib
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from onnxruntime import InferenceSession

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CACHE_FILE = Path("api_cache.json")

class ThreatIntelligenceAPI:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.cache = self.load_cache()

    def load_cache(self):
        if CACHE_FILE.exists():
            with open(CACHE_FILE, 'r') as file:
                cache = json.load(file)
                return cache
        return {}

    def fetch_data(self):
        if self.api_endpoint in self.cache:
            logger.info("Using cached data.")
            return self.cache[self.api_endpoint]
        
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            data = response.json()
            self.cache[self.api_endpoint] = data
            self.save_cache()
            return data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")
        return None

    def save_cache(self):
        with open(CACHE_FILE, 'w') as file:
            json.dump(self.cache, file)

class StrategicDecisionMaker:
    def __init__(self, data_source, model_path):
        self.data_source = data_source
        self.model_path = Path(model_path)
        self.model = self.load_model()

    def load_model(self):
        if self.model_path.exists():
            try:
                session = InferenceSession(self.model_path)
                return session
            except Exception as e:
                logger.error(f"An error occurred loading the model: {e}")
                sys.exit(1)
        else:
            logger.info("No existing model found. A new model will be trained.")
            return RandomForestClassifier(n_estimators=100)

    def train_model(self, data, labels, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, random_state=42)
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        logger.info(f"New model trained with an accuracy of: {score}")
        initial_type = [('float_input', FloatTensorType([None, len(data[0])]))
        onnx = convert_sklearn(self.model, initial_types=initial_type)
        with open(self.model_path, "wb") as f:
            f.write(onnx.SerializeToString())

    def analyze_data(self, data):
        prediction = self.model.predict(data)
        return prediction

    def make_decision(self, analysis_result):
        decision = f"Strategic decision based on analysis: {analysis_result}"
        logger.info(f"Decision sent to dashboard: {decision}")
        return decision

def main():
    parser = argparse.ArgumentParser(description="Advanced Strategic Decision Maker for Cybersecurity Context")
    parser.add_argument("data_source", help="Path to the data source file")
    parser.add_argument("model_path", help="Path to the machine learning model file")
    parser.add_argument("--api_endpoint", help="Endpoint for fetching real-time threat intelligence data")
    parser.add_argument("--test_size", type=float, default=0.2, help="Test size for the train-test split")
    parser.add_argument("--n_estimators", type=int, default=100, help="Number of estimators for the RandomForestClassifier")
    args = parser.parse_args()
    
    api = ThreatIntelligenceAPI(api_endpoint=args.api_endpoint)
    real_time_data = api.fetch_data()
    
    if real_time_data is None:
        logger.error("Failed to fetch data from the API.")
        sys.exit(1)
    
    decision_maker = StrategicDecisionMaker(data_source=args.data_source, model_path=args.model_path)
    
    data_for_analysis = real_time_data["features"]
    labels_for_training = real_time_data["labels"]
    decision_maker.train_model(data_for_analysis, labels_for_training, test_size=args.test_size)
    
    analysis_result = decision_maker.analyze_data(data_for_analysis)
    decision = decision_maker.make_decision(analysis_result)
    logger.info(decision)

if __name__ == "__main__":
    main()
