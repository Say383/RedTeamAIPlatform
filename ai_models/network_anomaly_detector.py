import argparse
import logging
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NetworkAnomalyDetector:
    def __init__(self, data_path, model_path=None):
        self.data_path = data_path
        self.model_path = model_path
        self.model = IsolationForest(n_estimators=100, contamination='auto')
        self.scaler = StandardScaler()

    def load_data(self):
        try:
            df = pd.read_csv(self.data_path)
            # Assuming 'target' is the label for anomalies (1 for anomalous, 0 for normal)
            X = df.drop('target', axis=1)
            y = df['target']
            return X, y
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise

    def preprocess_data(self, X):
        try:
            X_scaled = self.scaler.fit_transform(X)
            return X_scaled
        except Exception as e:
            logger.error(f"Failed to preprocess data: {e}")
            raise

    def split_data(self, X, y):
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self, X_train, y_train):
        try:
            self.model.fit(X_train)
            logger.info("Model trained successfully.")
        except Exception as e:
            logger.error(f"Failed to train model: {e}")
            raise

    def evaluate_model(self, X_test, y_test):
        try:
            y_pred = self.model.predict(X_test)
            # Map prediction labels to match the dataset labels (1 for anomalous, 0 for normal)
            y_pred = [1 if i == -1 else 0 for i in y_pred]
            report = classification_report(y_test, y_pred)
            logger.info(f"Classification report:\n{report}")
        except Exception as e:
            logger.error(f"Failed to evaluate model: {e}")
            raise

    def save_model(self):
        if self.model_path:
            try:
                joblib.dump((self.model, self.scaler), self.model_path)
                logger.info(f"Model saved to {self.model_path}.")
            except Exception as e:
                logger.error(f"Failed to save model: {e}")
                raise

    def load_model(self):
        if self.model_path and joblib.os.path.exists(self.model_path):
            try:
                self.model, self.scaler = joblib.load(self.model_path)
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise

    def predict(self, X_new):
        try:
            X_new_scaled = self.scaler.transform([X_new])
            prediction = self.model.predict(X_new_scaled)
            # Convert prediction to label
            prediction_label = 1 if prediction[0] == -1 else 0
            return prediction_label
        except Exception as e:
            logger.error(f"Failed to make prediction: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Network Anomaly Detector")
    parser.add_argument("--data", required=True, help="Path to the dataset")
    parser.add_argument("--model", help="Path to save/load the model")
    parser.add_argument("--predict", nargs='+', type=float, help="New data point for prediction")
    args = parser.parse_args()

    detector = NetworkAnomalyDetector(data_path=args.data, model_path=args.model)

    if args.predict:
        if not args.model:
            logger.error("Model path is required for prediction.")
            return
        detector.load_model()
        prediction_label = detector.predict(args.predict)
        logger.info(f"Prediction for the new data point: {'Anomaly' if prediction_label == 1 else 'Normal'}")
    else:
        X, y = detector.load_data()
        X_scaled = detector.preprocess_data(X)
        X_train, X_test, y_train, y_test = detector.split_data(X_scaled, y)
        detector.train_model(X_train, y_train)
        detector.evaluate_model(X_test, y_test)
        detector.save_model()

if __name__ == "__main__":
    main()
