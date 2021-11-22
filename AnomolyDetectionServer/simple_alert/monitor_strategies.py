import random
from ripe.atlas.sagan import PingResult, TracerouteResult
import requests
from datetime import datetime
import re
from abc import ABC, abstractmethod


class MonitorStrategy(ABC):

    @abstractmethod
    def collect_initial_dataset(self, collection, measurement_id):
        pass

    @abstractmethod
    def preprocess(self, measurement_result):
        pass

    @abstractmethod
    def store(self, collection, measurement_result):
        pass

    @abstractmethod
    def analyze(self, measurement_result):
        pass


class PingMonitorStrategy(MonitorStrategy):
    result_pattern = re.compile("{.*(stored_timestamp).*}")
    UNWANTED_PING_FIELDS = ["_on_error", "is_error", "seconds_since_sync", "_on_malformation", "is_malformed",
                            "raw_data", "error_message", "measurement_id", "firmware", "group_id",
                            "af", "bundle", "step", "packets", "protocol", "origin",
                            "destination_name", "destination_address", "packets_sent",
                            "packets_received", "packet_size"]

    def collect_initial_dataset(self, collection, measurement_id):
        """creates initial dataset"""
        print(f"collecting initial dataset for measurement: {measurement_id}")
        yesterday = int(datetime.now().timestamp()) - 24 * 60 * 60
        response = requests.get(
            f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results?start={yesterday}",
            stream=True)

        result_string = ""

        for i in response.iter_content(decode_unicode=True):
            result_string += i
            result = PingMonitorStrategy.result_pattern.search(result_string)
            if result:
                start, end = result.span()
                ping_result_raw = result_string[start:end]
                result_string = result_string[end:]
                result = self.preprocess(ping_result_raw)
                self.store(collection, result)

    def preprocess(self, measurement_result):
        """make measurment results consistent, make a dictionory of the object and keep all necessary fields"""
        result = PingResult(measurement_result)
        result_dict = result.__dict__
        result_dict["dropped_packets"] = result_dict["packets_sent"] - result_dict["packets_received"]
        for unwanted_field in PingMonitorStrategy.UNWANTED_PING_FIELDS:
            result_dict.pop(unwanted_field)

        return result_dict

    def store(self, collection, measurement_result):
        """store result in mongo_db"""
        collection.insert_one(measurement_result)

    def analyze(self, measurement_result):
        """check if result is anomality."""
        if random.random() > 0.999:
            return True
        else:
            return False


class TracerouteMonitorStrategy(MonitorStrategy):
    result_pattern = re.compile("{.*(stored_timestamp).*}")

    def collect_initial_dataset(self, collection, measurement_id):
        """creates initial dataset"""
        print(f"collecting initial dataset for measurement: {measurement_id}")
        yesterday = int(datetime.now().timestamp()) - 24 * 60 * 60
        response = requests.get(
            f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results?start={yesterday}",
            stream=True)

        result_string = ""

        for i in response.iter_content(decode_unicode=True):
            result_string += i
            result = TracerouteMonitorStrategy.result_pattern.search(result_string)
            if result:
                start, end = result.span()
                traceroute_result_raw = result_string[start:end]
                result_string = result_string[end:]
                result = self.preprocess(traceroute_result_raw)
                self.store(collection, result.raw_data)

    def preprocess(self, measurement_result):
        """make measurment results consistent, make a dictionory of the object and keep all necessary field"""
        return TracerouteResult(measurement_result, on_error=TracerouteResult.ACTION_IGNORE )

    def store(self, collection, measurement_result):
        """store result in mongo_db"""
        collection.insert_one(measurement_result)

    def analyze(self, measurement_result):
        """check if result is anomality."""
        if random.random() > 0.999:
            return True
        else:
            return False
