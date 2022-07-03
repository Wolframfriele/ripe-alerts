from abc import ABC, abstractmethod


class MonitorStrategy(ABC):
    @abstractmethod
    def measurement_type(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def detection_type(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def detection_description(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def collect_initial_dataset(self, collection, measurement_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def preprocess(self, measurement_result) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def store(self, collection, measurement_result) -> None:
        raise NotImplementedError()

    @abstractmethod
    def analyze(self, collection):
        raise NotImplementedError()

    @abstractmethod
    def filter(self, df) -> list:
        raise NotImplementedError()
