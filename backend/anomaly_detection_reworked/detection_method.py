import enum


from abc import ABC, abstractmethod

from anomaly_detection_reworked.measurement_type import MeasurementType


class DetectionMethod(ABC):
    """ Interface for creating an algorithm to find anomalies in the data from RIPE ATLAS Streaming API. """

    @abstractmethod
    def describe(self) -> dict:
        """
        Method used to describe the detection method so that it can be stored in the database.
        Returns information (tuple): (type, description)
        """
        raise NotImplementedError()

    @abstractmethod
    def on_result_response(self, data: dict):
        """
        Method that will be called every time we receive a new result from the RIPE Streaming API.
        Data: dictionary
        """
        raise NotImplementedError()

    @abstractmethod
    def on_startup_event(self):
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

    def __eq__(self, other: object) -> bool:
        """
        Method that is used to compare two Detection Method by their values.
        @param other: The other Detection Method instance which will be compared to.
        @return: True if the instance is of the same class and contains the same measurement type.
        """
        return isinstance(other, self.__class__) and self.get_measurement_type == other.get_measurement_type
