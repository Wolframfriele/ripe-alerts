"""Contains a datastructure for anomalies"""
import pandas as pd
from database.models import Anomaly, AutonomousSystem, DetectionMethod


class AnomalyObject:

    def __init__(self, time, ip_address, measurement_type, detection_method: DetectionMethod, mean_increase, anomaly_score, asn, description=None, prediction_value=None) -> None:
        self.time = time
        self.ip_address = ip_address
        self.measurement_type = measurement_type
        self.detection_method = detection_method
        self.mean_increase = mean_increase
        self.anomaly_score = anomaly_score
        self.asn = asn
        self.description = description
        self.prediction_value = prediction_value

    def feature_extraction(self) -> None:
        """
        NOT YET IMPLEMENTED
        Will extracts extra information about the anomaly and store it in anomaly object.
        """
        pass
        # NOT YET IMPLEMENTED
        # Needed functionality
        # Check how long since last anomaly
        # check how long since last anomaly in same AS

    def get_df(self) -> pd.DataFrame:
        """
        Returns the dataframe version of an anomaly.

        Returns:
                data (DataFrame): A pandas dataframe containing the anomaly data
        """
        data = {
            "ip_address": self.ip_address,
            "measurement_type": self.measurement_type,
            "detection_method": self.detection_method.type,
            "mean_increase": self.mean_increase,
            "anomaly_score": self.anomaly_score,
            "asn": self.asn,
        }
        df = pd.DataFrame(data)
        df = df.astype({'ip_address': 'category', 'measurement_type': 'category', 'detection_method': 'category', 'asn': 'category'})
        return df

    def update_predict(self, prediction: bool) -> None:
        """
        Updates the predict value for the anomaly

        Parameters:
                prediction (bool): The prediction if the anomaly is alert worthy.
        """
        self.prediction_value = prediction

    def store(self) -> None:
        """
        Stores the anomaly in the database.
        """
        asn = AutonomousSystem.objects.all()[0]
        Anomaly.objects.create(
            time=self.time,
            ip_address=self.ip_address,
            autonomous_system=asn,
            description=self.description,
            measurement_type=self.measurement_type,
            detection_method_id=self.detection_method.id,
            mean_increase=self.mean_increase,
            anomaly_score=self.anomaly_score,
            prediction_value=self.prediction_value,
            asn=self.asn
        )
