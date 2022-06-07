import abc


class DetectionMethod(abc.ABC):

    @abc.abstractmethod
    def on_result_response(self, data):
        """
        Method that will be called every time we receive a new result from the RIPE Streaming API.
        Data: dictionary
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def on_detection_method_loaded(self):
        """
        Method that will be called once the detection method is loaded
        """
        raise NotImplementedError()
