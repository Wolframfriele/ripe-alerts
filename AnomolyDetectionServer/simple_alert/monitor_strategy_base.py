import imp


from abc import ABC, abstractmethod


class MonitorStrategy(ABC):
    @abstractmethod
    def measurement_type(self) -> str:
        pass

    @abstractmethod
    def collect_initial_dataset(self, collection, measurement_id: str) -> None:
        pass

    @abstractmethod
    def preprocess(self, measurement_result) -> dict:
        pass

    @abstractmethod
    def store(self, collection, measurement_result) -> None:
        pass

    @abstractmethod
    def analyze(self, collection):
        pass

    @abstractmethod
    def filter(self, df) -> list:
        pass
