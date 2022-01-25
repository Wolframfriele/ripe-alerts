import random
import re
import time
import requests
import numpy as np
import pandas as pd
import ijson
from urllib.request import urlopen
from requests.exceptions import ChunkedEncodingError
from datetime import datetime
from abc import ABC, abstractmethod
from ripe.atlas.sagan import PingResult, TracerouteResult
from adtk.detector import LevelShiftAD
from adtk.data import validate_series


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
    def analyze(self, collection):
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
        result_string = ""
        # to keep track of the latest time we received
        result_time = yesterday
        while True:
            try:
                response = requests.get(
                    f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results?start={result_time}",
                    stream=True)
                for i in response.iter_content(decode_unicode=True):
                    result_string += i
                    result = PingMonitorStrategy.result_pattern.search(result_string)
                    if result:
                        start, end = result.span()
                        ping_result_raw = result_string[start:end]
                        result_string = result_string[end:]
                        result = self.preprocess(ping_result_raw)
                        result_time = result['created']
                        self.store(collection, result)
                break
            except ChunkedEncodingError:
                print("Oh no we lost connection, but we will try again")
                time.sleep(1)

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


class PreEntryASMonitor(MonitorStrategy):
    def __init__(self) -> None:
        self.own_as = None

    def collect_initial_dataset(self, collection, measurement_id) -> None:
        """
        Collect data from the last day as a baseline.

        Parameters:
                collection (obj)

        Returns:
                anomalies (list): 
        """
        print(f"collecting initial dataset for measurement: {measurement_id}")
        yesterday = int(datetime.now().timestamp()) - 24 * 60 * 60
        result_time = yesterday

        while True:
            try:
                f = urlopen(f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results?start={result_time}")
                parser = ijson.items(f, 'item')
                for measurement_data in parser:
                    result = self.preprocess(measurement_data)
                    result_time = result['created']
                    self.store(collection, result)
                break
            except ChunkedEncodingError:
                print("Oh no we lost connection, but we will try again")
                time.sleep(1)

    def store(self, collection, measurement_result:dict) -> None:
        """store result in mongo_db"""
        collection.insert_one(measurement_result)        

    def preprocess(self, single_result_raw:dict):
        """
        Pre-processes json measurement data to only send out the relevant data.

        Parameters:
                single_result_raw (str): A dictionary object containing the results of one
                measurement point.

        Returns:
                clean_result (dict): 
        """
        measurement_result = TracerouteResult(single_result_raw,
                                              on_error=TracerouteResult.ACTION_IGNORE)
        hops = []
        for hop_object in measurement_result.hops:
            hop_number = hop_object.raw_data['hop']
            if 'error' in hop_object.raw_data:
                hops.append({
                    'hop': None,
                    'from': None,
                    'min_rtt': None,
                })
            else:
                try:
                    hop_pings = hop_object.raw_data['result']
                except KeyError:
                    print(hop_object.raw_data)

                hop_ip = None
                min_hop_rtt = float('inf')
                for ping in hop_pings:
                    if 'rtt' in ping:
                        if hop_ip == None:
                            hop_ip = ping['from']
                        if ping['rtt'] < min_hop_rtt:
                            min_hop_rtt = ping['rtt']

                min_hop_rtt = float(min_hop_rtt)
                hops.append({
                    'hop': hop_number,
                    'from': hop_ip,
                    'min_rtt': min_hop_rtt,
                })

        pre_entry_hop_min_rtt, pre_entry_hop_ip, pre_entry_as = np.nan, np.nan, np.nan

        as_ip = measurement_result.destination_address

        hops.reverse()
        for idx, hop in enumerate(hops):
            # Check if ip in as number, use the first one thats different AS
            as_look_up = ASLookUp()
            if not as_look_up.ip_in_as(hop['from'], as_ip):
                pre_entry_hop_ip = hop['from']
                pre_entry_hop_min_rtt = hops[idx - 1]['min_rtt']
                if idx - 1 == -1:
                    pre_entry_hop_min_rtt = float('inf')
                pre_entry_as = as_look_up.get_as(pre_entry_hop_ip)
                break
    
        clean_result = {
            'probe_id': measurement_result.probe_id,
            'created': measurement_result.created,
            'total_hops': measurement_result.total_hops,
            'pre_entry_hop_min_rtt': pre_entry_hop_min_rtt,
            'pre_entry_hop_ip': pre_entry_hop_ip,
            'pre_entry_as': pre_entry_as
        }
        return clean_result

    def analyze(self, collection):
        """
        Analyzes a series of measurements for anomalies.

        Parameters:
                collection (class): MongoDB collection object.

        Returns:
                anomalies (list): List containing all anomalies as dictionary objects: {
                    'as-number': AS number that contains the anomalie,
                    'time': highest time value for AS (latest measurement),
                    'description': Text description,
                    'score': The score; the percentage of probes with anomalie in as.
                }
        """
        min_score = 30 # minimum percentage of anomalies before alert
        anomalies = []
        all_measurements = []

        for measurement in collection.find():
            all_measurements.append(measurement)

        df: pd.DataFrame = pd.DataFrame(all_measurements)
        df_outlier = pd.DataFrame()

        level_shift = LevelShiftAD(c=10.0, side='positive', window=3)

        for probe_id in df["probe_id"].unique():
            single_probe = df[df["probe_id"] == probe_id]

            single_probe.set_index('created', inplace=True)
            ts = single_probe['pre_entry_hop_min_rtt']
            ts = validate_series(ts)

            try:
                single_probe["level_shift"] = level_shift.fit_detect(ts)
                df_outlier = df_outlier.append(single_probe)
            except RuntimeError:
                pass

        for as_num in df_outlier['pre_entry_as'].unique():
            single_as_df = df_outlier[df_outlier['pre_entry_as'] == as_num]
            probes_in_as = len(single_as_df['probe_id'].unique())
            alert_time = single_as_df.index.max()
            if probes_in_as > 5:
                as_anomalies = single_as_df.groupby(pd.Grouper(freq="32T"))["level_shift"].agg("sum")
                # look at last sum (current moment)
                score = round((as_anomalies[-1] / probes_in_as) * 100, 2)
                if score > min_score:
                    description = f'Oh no, there seems to be an increase in RTT in neighboring AS: {as_num}'
                    print(description)
                    anomalies.append({
                        'as-number': as_num,
                        'time': alert_time,
                        'description': description,
                        'score': score
                    })

        return anomalies


class ASLookUp:
    """Set of methods that help with converting ip adresses to as numbers."""
    def __init__(self) -> None:
        self.known_ip = {}
        self.own_as = None

    def get_as(self, ip):
        """
        Gets the AS number for an IP Adress.

        Parameters:
                ip (str): A valid IPv4 adress in the shape 192.0.0.1

        Returns:
                as number (str): The AS number that the IP is a part off
        """
        as_num = None
        if ip is not None:
            if ip in self.known_ip:
                as_num = self.known_ip[ip]
            else:
                r = requests.get(f"https://stat.ripe.net/data/network-info/data.json?resource={ip}").json()['data']['asns']
                if len(r) > 0:
                    as_num = r[0]
                else:
                    as_num = np.nan
                self.known_ip[ip] = as_num
        return as_num

    def ip_in_as(self, ip, goal_ip):
        """
        Determine if IP adress is in the same AS number, as an other IP adress.

        Parameters:
                ip (str): A valid IPv4 adress in the shape 192.0.0.1
                goal_ip (str): A valid IPv4 adress in the shape 168.0.0.1

        Returns:
                in_as (bool): True if both IP adresses are in the same AS number,
                otherwise False.
        """
        in_as = False
        if self.own_as is None:
            self.own_as = self.get_as(goal_ip)
        if self.get_as(ip) == self.own_as:
            in_as = True
        return in_as
