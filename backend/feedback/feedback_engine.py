"""Contains the main class that deals with feedback and alert prediction"""
import pickle
from unicodedata import category
import pandas as pd
from database.models import Anomaly, Feedback
from anomaly_detection.anomaly_object import AnomalyObject
from xgboost import XGBClassifier

CLF_PATH = 'feedback/feedback_clf.pkl'
MIN_SAMPLES = 10


class FeedbackEngine:
    """
        System responsible for handeling user feedback on anomalies.
    """

    def __init__(self) -> None:
        self.clf = XGBClassifier(tree_method="hist" ,enable_categorical=True)
        self.train()

    def _encode(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        One hot encodes the categorical data points.
        """


    def _predict(self, anomaly: AnomalyObject) -> bool:
        """
        Predicts if an anomaly is alert worthy. If there are fewer than 5 points of feedback in the database,
        will always predict true, to get alerts to the user.

        Parameters:
                anomaly (AnomalyObject): An anomaly without a made prediction about the alert status.

        Returns:
                alert (bool): True if anomaly is alert worthy.
        """
        if len(Anomaly.objects.filter(feedback__isnull=False)) >= MIN_SAMPLES:
            df = anomaly.get_df()
            alert = self.clf.predict(df)[0]
            print(f"Enough samples predicted: {alert}")
        else:
            alert = True
        return alert

    def _get_feedback(self, feedback_id: int) -> bool:
        """
        Takes a feedback id, and returns the feedback response value.

        Parameters:
                feedback_id (int): The id associated with a feedback database entry.
        Returns:
                response (bool): The feedback given about the anomaly.
        """
        return Feedback.objects.get(anomaly=feedback_id).response

    def process_anomaly(self, anomaly: AnomalyObject) -> bool:
        """
        Processes new anomalies, by first running feature extraction (not yet implemented).
        It then predicts if a new anomaly is alert worthy and stores the result in the database.
        Lastly it broadcasts an alert if the anomaly was alert worthy.

        Parameters:
                anomaly (AnomalyObject): An anomaly without a made prediction about the alert status.

        Returns:
                alert (bool): True if anomaly is alert worthy.
        """
        anomaly.feature_extraction()
        alert = self._predict(anomaly)

        anomaly.update_predict(alert)
        anomaly.store()

        if alert:
            # IMPLEMENT LATER
            # send notification
            print('Anomaly found, notifiction will be send.')
        return alert

    def train(self) -> bool:
        """
        Trains the feedback engine using the anomalies in the database that have feedback.
        Needs atleast 5 points of feedback to be able to train.

        Returns:
                trained (bool): True if feedback engine is trained.
        """
        anomalies = Anomaly.objects.filter(feedback__isnull=False)

        if len(anomalies) >= MIN_SAMPLES:
            df = pd.DataFrame(list(anomalies.values("ip_address", "measurement_type", "detection_method",
                                                "mean_increase", "anomaly_score", "asn", "feedback")))
            df = df.astype({'ip_address': 'category', 'measurement_type': 'category', 'detection_method': 'category', 'asn': 'category'})
            df["feedback"] = df["feedback"].apply(self._get_feedback)
            y = df["feedback"]
            X = df.drop("feedback", axis=1)
            self.clf.fit(X, y)
            print("Feedback engine trained.")
            return True
        else:
            print(f"Training the feedback engine failed. Needed atleast 10 samples, got {len(anomalies)}.")
            return False