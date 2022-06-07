from abc import ABC, abstractmethod


class DetectionMethod(ABC):

    @abstractmethod
    def on_result_response(self, data) -> None:
        """
        Method that will be called every time we receive a new result from the RIPE Streaming API.
        Data: dictionary
        """
        raise NotImplementedError()

    @abstractmethod
    def on_detection_method_loaded(self) -> None:
        """
        Method that will be called once the detection method is loaded.
        """
        raise NotImplementedError()
