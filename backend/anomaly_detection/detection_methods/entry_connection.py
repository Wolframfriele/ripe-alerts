"""
Plugin File for the Entry Connection detection method. 
"""
import time
import ijson
import numpy as np
import pandas as pd
from urllib.request import urlopen
from requests.exceptions import ChunkedEncodingError
from datetime import datetime
from ripe.atlas.sagan import TracerouteResult
from adtk.detector import LevelShiftAD
from adtk.data import validate_series
from ..as_tools import ASLookUp
from datetime import datetime, timedelta
from ..monitor_strategy_base import MonitorStrategy


class DetectionMethod(MonitorStrategy):
    def __init__(self) -> None:
        self.own_as = None
        self.as_look_up = ASLookUp()

    def measurement_type(self) -> str:
        return 'traceroute'

    def collect_initial_dataset(self, collection, measurement_id: str) -> None:
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
                f = urlopen(
                    f"https://atlas.ripe.net/api/v2/measurements/\
                        {measurement_id}/results?start={result_time}")
                parser = ijson.items(f, 'item')
                for measurement_data in parser:
                    result = self.preprocess(measurement_data)
                    result_time = result['created']
                    self.store(collection, result)
                break
            except ChunkedEncodingError:
                print("Oh no we lost connection, but we will try again")
                time.sleep(1)

    def store(self, collection, measurement_result: dict) -> None:
        """store result in mongo_db"""
        collection.insert_one(measurement_result)

    def preprocess(self, single_result_raw: dict) -> dict:
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
        user_ip = measurement_result.destination_address

        hops = self.clean_hops(measurement_result.hops)
        entry_rtt, entry_ip, entry_as = self.find_network_entry_hop(
            hops, user_ip)
        
        return {
            'probe_id': measurement_result.probe_id,
            'created': measurement_result.created,
            'entry_rtt': entry_rtt,
            'entry_ip': entry_ip,
            'entry_as': entry_as
        }

    def clean_hops(self, hops: list) -> list:
        """
        Takes the raw hops from Sagan Traceroute object, and processes the data.

        Parameters:
                hops (list): A list with raw hop data.

        Returns:
                cleanend_hops (list): contains dict objects with {hop(id), ip, min_rtt}  
        """
        cleaned_hops = []
        for hop_object in hops:
            if 'error' in hop_object.raw_data:
                cleaned_hops.append({
                    'hop': hop_object.raw_data['hop'],
                    'ip': None,
                    'min_rtt': None,
                })
            else:
                hop_packets = hop_object.raw_data['result']
                hop_ip = None
                min_hop_rtt = float('inf')
                for packet in hop_packets:
                    if 'rtt' in packet:
                        if packet['rtt'] < min_hop_rtt:
                            hop_ip = packet['from']
                            min_hop_rtt = packet['rtt']
                min_hop_rtt = float(min_hop_rtt)
                if min_hop_rtt == float('inf'):
                    min_hop_rtt = None
                cleaned_hops.append({
                    'hop': hop_object.raw_data['hop'],
                    'ip': hop_ip,
                    'min_rtt': min_hop_rtt,
                })
        return cleaned_hops

    def find_network_entry_hop(self, hops: list, user_ip: str):
        """
        Takes a list of cleaned hops and returns the values of the hop at the edge 
        of the users network.

        Parameters:
                hops (list): A list with cleaned hop data.

        Returns:
                entry_rtt (float): min round trip time at network entry hop.
                entry_ip (str): ip adress of the router before entering your network.
                entry_as (str): as number of the neighboring network connection.
        """
        entry_rtt, entry_ip, entry_as = [np.nan] * 3
        user_as = self.as_look_up.get_as(user_ip)

        hops.reverse()
        for idx, hop in enumerate(hops):
            hop_as = self.as_look_up.get_as(hop['ip'])
            if hop_as != user_as:
                entry_ip = hop['ip']
                entry_rtt = hops[idx - 1]['min_rtt']
                if idx - 1 == -1:
                    entry_rtt = float('inf')
                break
        if isinstance(entry_ip, str):
            entry_as = hop_as
        else:
            entry_ip = np.nan
        return entry_rtt, entry_ip, entry_as

    def analyze(self, collection) -> pd.DataFrame:
        """
        Analyzes a series of measurements for anomalies.

        Parameters:
                collection (class): MongoDB collection object.

        Returns:
                df_outlier (pandas.DataFrame: A DataFrame similar
                to input dataframe, with the LevelShift anomaly
                detection results added for all succesfully
                analyzed time series.
        """
        all_measurements = []

        qdate = datetime.now() - timedelta(days=1)
        for measurement in collection.find({"created": {"$lt": qdate}}):
            all_measurements.append(measurement)

        df = pd.DataFrame(all_measurements)

        level_shift = LevelShiftAD(c=10.0, side='positive', window=3)
        df_outlier = pd.DataFrame()

        for probe_id in df["probe_id"].unique():
            single_probe = df[df["probe_id"] == probe_id].copy()
            single_probe.set_index('created', inplace=True)
            time_series = single_probe['entry_rtt']
            time_series = validate_series(time_series)

            try:
                level_anomalies = level_shift.fit_detect(time_series)
                single_probe["level_shift"] = level_anomalies
                df_outlier = pd.concat([df_outlier, single_probe])

            except RuntimeError:
                pass

        return df_outlier

    def filter(self, df_outlier: pd.DataFrame, plot_results=False) -> list:
        """
        Filters through anomalies and returns the alerts.

        Parameters:
                df_outlier (pandas.DataFrame): Dataframe with anomalies
                boolean for all measurement points.

        Returns:
                anomalies (list): A list with all anomalies organized
                with description, and if the anomalie should be alerted.
        """
        MIN_ALERT_SCORE = 30
        MIN_ANOMALY_SCORE = 5
        anomalies = []

        unique_as_nums = df_outlier['entry_as'].unique()
        for as_num in unique_as_nums:
            single_as_df = df_outlier[df_outlier['entry_as'] == as_num]
            probes_in_as = len(single_as_df['probe_id'].unique())

            if probes_in_as > 4:
                as_anomalies = single_as_df.groupby(pd.Grouper(freq="20T"))[
                    "level_shift"].agg("sum")
                if plot_results:
                    try:
                        as_anomalies.plot()
                    except:
                        pass
                score = round((as_anomalies[-3] / probes_in_as) * 100, 2)
                alert_time = as_anomalies.index[-3]
                print(f'Entry connection anomaly score for {as_num}: {score}')
                if score > MIN_ANOMALY_SCORE:
                    alert = score > MIN_ALERT_SCORE
                    print(f'Anomaly at {alert_time.strftime("%d/%m/%Y, %H:%M:%S")} \
                        in AS{as_num}. Problem with {as_anomalies[-3]} probes. \
                            Percentage of AS: {score}')
                    description = f'Oh no, there seems to be an increase in RTT \
                        in neighboring AS: {as_num}'
                    anomalies.append({
                        'as-number': as_num,
                        'time': alert_time,
                        'description': description,
                        'score': score,
                        'alert': alert
                    })
        return anomalies
