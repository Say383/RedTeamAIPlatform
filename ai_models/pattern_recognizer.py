import argparse
import logging
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PatternRecognizer:
    def __init__(self, dataset_path=None, model_path=None):
        self.dataset_path = Path(dataset_path) if dataset_path else None
        self.model_path = Path(model_path) if model_path else None
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def load_dataset(self):
        if not self.dataset_path or not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
        return pd.read_csv(self.dataset_path)

    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        logger.info("Training completed.")
        predictions = self.model.predict(X_test)
        logger.info(f"Classification Report:\n{classification_report(y_test, predictions)}")

    def save_model(self):
        if not self.model_path:
            raise ValueError("Model path is not provided.")
        joblib.dump(self.model, self.model_path)
        logger.info(f"Model saved at {self.model_path}")

    def load_model(self):
        if not self.model_path or not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        self.model = joblib.load(self.model_path)
        logger.info("Model loaded.")

    def predict(self, features):
        return self.model.predict([features])

# Entry point of the script
def main(args):
    try:
        recognizer = PatternRecognizer(dataset_path=args.dataset, model_path=args.model)
        
        if args.train:
            dataset = recognizer.load_dataset()
            X = dataset.drop('target', axis=1)
            y = dataset['target']
            recognizer.train(X, y)
            recognizer.save_model()
        elif args.predict:
            recognizer.load_model()
            prediction = recognizer.predict(args.predict)
            logger.info(f"Prediction: {prediction}")
        else:
            logger.error("No action specified. Use --train to train a new model or --predict to make predictions.")
    except Exception as e:
        logger.exception("An error occurred: ", exc_info=e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pattern Recognizer Tool")
    parser.add_argument("--dataset", type=str, help="Path to the dataset file")
    parser.add_argument("--model", type=str, help="Path to save/load the model file")
    parser.add_argument("--train", action='store_true', help="Train the model with the provided dataset")
    parser.add_argument("--predict", nargs='+', type=float, help="Predict using a trained model with provided features")
    parsed_args = parser.parse_args()
    main(parsed_args)
