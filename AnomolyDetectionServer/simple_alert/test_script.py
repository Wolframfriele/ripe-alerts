import imp
import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient, DESCENDING
from adtk.detector import LevelShiftAD
from adtk.data import validate_series

username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
measurement_id = '34761880'

yesterday = int(datetime.now().timestamp()) - 24 * 60 * 60 * 1000
result_string = ""
result_time = yesterday


client = MongoClient(f'mongodb://{username}:{password}@mongodb')
database = client['Atlas_Results']
collection = database[f'traceroute measurement: {measurement_id}']
collection.create_index([("created", DESCENDING)])

all_measurements = []

for measurement in collection.find():
    all_measurements.append(measurement)

df: pd.DataFrame = pd.DataFrame(all_measurements)

level_shift = LevelShiftAD(c=10.0, side='positive', window=3)

df_outlier = pd.DataFrame()
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

    