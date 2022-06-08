import enum


from abc import ABC, abstractmethod

from anomaly_detection_reworked.measurement_type import MeasurementType


class DetectionMethod(ABC):
    """ Interface for creating an algorithm to find anomalies in RIPE ATLAS Streaming API. """

    @abstractmethod
    def on_result_response(self, data: dict) -> None:
        """
        Method that will be called every time we receive a new result from the RIPE Streaming API.
        Data: dictionary
        """
        raise NotImplementedError()

    @abstractmethod
    def on_startup_event(self) -> None:
        """
        Method that will be called once the detection method has been loaded.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def get_measurement_type(self) -> MeasurementType:
        """
        Property which will be used to select corresponding Measurement IDs.
        """
        raise ValueError()

    def __str__(self) -> str:
        return "Class: " + str(self.__class__.__name__) + " " + str(self.get_measurement_type)




