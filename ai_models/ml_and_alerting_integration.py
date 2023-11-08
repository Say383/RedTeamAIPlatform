import argparse
import logging
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import smtplib
from email.message import EmailMessage

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MLAlertingSystem:
    def __init__(self, data_path, model_path=None, alert_email=None):
        self.data_path = data_path
        self.model_path = model_path
        self.model = RandomForestClassifier(n_estimators=100)
        self.alert_email = alert_email

    def load_and_prepare_data(self):
        try:
            df = pd.read_csv(self.data_path)
            X = df.drop('target', axis=1)
            y = df['target']
            return train_test_split(X, y, test_size=0.2, random_state=42)
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def train_model(self, X_train, y_train):
        try:
            self.model.fit(X_train, y_train)
            logger.info("Model trained successfully.")
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise

    def evaluate_model(self, X_test, y_test):
        try:
            predictions = self.model.predict(X_test)
            report = classification_report(y_test, predictions)
            logger.info(f"Model Evaluation:\n{report}")
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            raise

    def save_model(self):
        if self.model_path:
            try:
                joblib.dump(self.model, self.model_path)
                logger.info(f"Model saved to {self.model_path}.")
            except Exception as e:
                logger.error(f"Error saving model: {e}")
                raise

    def load_model(self):
        if self.model_path and joblib.os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                raise

    def predict_and_alert(self, features):
        try:
            prediction = self.model.predict([features])
            if prediction[0] == 1:  # Assuming 1 indicates a positive alert
                self.send_alert(features)
            return prediction
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise

    def send_alert(self, features):
        if self.alert_email:
            try:
                msg = EmailMessage()
                msg.set_content(f"Alert: Suspicious activity detected.\nFeatures: {features}")
                msg['Subject'] = "Security Alert"
                msg['From'] = "alert@example.com"
                msg['To'] = self.alert_email

                s = smtplib.SMTP('localhost')
                s.send_message(msg)
                s.quit()
                logger.info("Alert sent.")
            except Exception as e:
                logger.error(f"Error sending alert: {e}")
                raise
        else:
            logger.info("Alert email is not configured.")

def main():
    parser = argparse.ArgumentParser(description="ML and Alerting Integration System")
    parser.add_argument("--data", required=True, help="Path to the dataset")
    parser.add_argument("--model", help="Path to save/load the model")
    parser.add_argument("--email", help="Alert email address")
    parser.add_argument("--predict", nargs='+', type=float, help="Features for prediction")
    args = parser.parse_args()

    system = MLAlertingSystem(data_path=args.data, model_path=args.model, alert_email=args.email)

    if args.predict:
        if not args.model:
            logger.error("Model path is required for prediction.")
            return
        system.load_model()
        prediction = system.predict_and_alert(args.predict)
        logger.info(f"Prediction: {prediction}")
    else:
        X_train, X_test, y_train, y_test = system.load_and_prepare_data()
        system.train_model(X_train, y_train)
        system.evaluate_model(X_test, y_test)
        system.save_model()

if __name__ == "__main__":
    main()
