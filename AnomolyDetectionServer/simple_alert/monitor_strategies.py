import random
import re
import time
import requests
import numpy as np
import pandas as pd
from requests.exceptions import ChunkedEncodingError
from datetime import datetime, timedelta
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


class TracerouteMonitorStrategy(MonitorStrategy):
    result_pattern = re.compile("{.*(stored_timestamp).*}")
    UNWANTED_TRACEROUTE_FIELDS = ["raw_data"]

    def collect_initial_dataset(self, collection, measurement_id):
        """creates initial dataset"""
        print(f"collecting initial dataset for measurement: {measurement_id}")
        yesterday = int(datetime.now().timestamp()) - 24 * 60 * 60
        result_string = ""
        result_time = yesterday

        while True:
            try:
                response = requests.get(
                    f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results?start={result_time}",
                    stream=True)
                for i in response.iter_content(decode_unicode=True):
                    result_string += i
                    result = TracerouteMonitorStrategy.result_pattern.search(result_string)
                    if result:
                        start, end = result.span()
                        traceroute_result_raw = result_string[start:end]
                        result_string = result_string[end:]
                        result = self.preprocess(traceroute_result_raw)
                        result_time = result['created']
                        self.store(collection, result)
                break
            except ChunkedEncodingError:
                print("Oh no we lost connection, but we will try again")
                time.sleep(1)

    def preprocess(self, measurement_result):
        """make measurment results consistent, make a dictionory of the object and keep all necessary field"""
        result = TracerouteResult(measurement_result, on_error=TracerouteResult.ACTION_IGNORE)
        result_dict = result.__dict__
        for unwanted_field in TracerouteMonitorStrategy.UNWANTED_TRACEROUTE_FIELDS:
            result_dict.pop(unwanted_field)

        new_hops = []
        for hop in result_dict['hops']:
            hop = hop.__dict__
            hop['packets'] = [packet.__dict__ for packet in hop['packets']]
            for packet in hop['packets']:
                packet.pop("icmp_header")
            new_hops.append(hop)
        result_dict['hops'] = new_hops
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
        self.known_ip = {}
        self.own_as = None

    def collect_initial_dataset(self, collection, measurement_id):
        """creates initial dataset"""
        print(f"collecting initial dataset for measurement: {measurement_id}")
        yesterday = int(datetime.now().timestamp()) - 24 * 60 * 60
        result_string = ""
        result_time = yesterday

        while True:
            try:
                response = requests.get(
                    f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results?start={result_time}",
                    stream=True)
                for i in response.iter_content(decode_unicode=True):
                    result_string += i
                    result = TracerouteMonitorStrategy.result_pattern.search(result_string)
                    if result:
                        start, end = result.span()
                        traceroute_result_raw = result_string[start:end]
                        result_string = result_string[end:]
                        result = self.preprocess(traceroute_result_raw)
                        result_time = result['created']
                        self.store(collection, result)
                break
            except ChunkedEncodingError:
                print("Oh no we lost connection, but we will try again")
                time.sleep(1)
        

    def preprocess(self, single_result_raw):
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

        # Make a variable that has the last ip adres
        as_ip = measurement_result.destination_address

        hops.reverse()
        for idx, hop in enumerate(hops):
            # Check if ip in as number, use the first one thats different AS
            if not self.ip_in_as(hop['from'], as_ip):
                # print('Hop not in AS')
                pre_entry_hop_ip = hop['from']
                pre_entry_hop_min_rtt = hops[idx - 1]['min_rtt']
                if idx - 1 == -1:
                    pre_entry_hop_min_rtt = float('inf')
                pre_entry_as = self.get_as(pre_entry_hop_ip)
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

    def get_as(self, ip):
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
        in_as = False
        if self.own_as is None:
            self.own_as = self.get_as(goal_ip)
        if self.get_as(ip) == self.own_as:
            in_as = True
        return in_as

    def store(self, collection, measurement_result):
        """store result in mongo_db"""
        collection.insert_one(measurement_result)

    def analyze(self, collection, measurement_result):
        # yesterday = datetime.now() - timedelta(hours=24)
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
            if probes_in_as > 5:
                as_anomalies = single_as_df.groupby(pd.Grouper(freq="32T"))["level_shift"].agg("sum")
                if as_anomalies[-1] > (probes_in_as / 3):
                    print(f'Oh no, there seems to be an increase in RTT in neighboring AS: {as_num}')
