import datetime
import pytz
import os
import time
from django import db
from ripe.atlas.cousteau import *
import multiprocessing
from .monitor_strategy_base import MonitorStrategy
from database.models import MeasurementCollection, Anomaly, DetectionMethod, AutonomousSystem, Probe, MeasurementPoint, Hop
from .format import HopFormat, ProbeMeasurement, HopFormat
from .requests import ProbeRequest
from time import perf_counter


class DataManager:
    def __init__(self) -> None:
        pass

    #Saving the probe and measurementpoint data
    def store(self, probe_measurement: ProbeMeasurement, measurement_id, total_hops):
        start_store = perf_counter()
        probe_information = ProbeRequest().get_probe_location(probe_measurement.probe_id)
        get_location_time = perf_counter() - start_store

        print(f" Get location time - {get_location_time}")
        
        obj, created_probe = Probe.objects.get_or_create(probe=probe_measurement.probe_id,
                                                    measurement_id=measurement_id,
                                                    as_number=probe_information['as_number'],
                                                    country=probe_information['country'],
                                                    city=probe_information['city'])
        
        object, created_point = MeasurementPoint.objects.get_or_create(probe=obj,
                                        time=probe_measurement.created,
                                        round_trip_time_ms=probe_measurement.entry_rtt,
                                        hops_total=total_hops)

        # print('Probe ' + str(probe_measurement.probe_id) + ' is saved!')
        print(f" Probe {str(probe_measurement.probe_id)} + measurementpoints savetime - {perf_counter() - start_store}")
        return object.id

    #Saving the data from the hops
    def store_hops(self, hop: HopFormat, measurementpoint_id):
        try:
            hop_data = Hop.objects.create(measurement_point_id=measurementpoint_id,
                            current_hop=hop.hop,
                            round_trip_time_ms=hop.min_rtt,
                            ip_address=hop.ip_address,
                            as_number=hop.asn)
            hop_data.save()
        except ValueError:
            print(hop.ip_address)
            print(hop.asn)
            raise ValueError

class Monitor:
    def __init__(self, MeasurementCollection: MeasurementCollection, strategy: MonitorStrategy):

        self.measurement = MeasurementCollection
        self.strategy = strategy

    def __str__(self):
        return f"Monitor for {self.measurement.type} measurement: {self.measurement.measurement_id}"

    #Get the data from streaming API and starting the anomaly detction
    def on_result_response(self, *args):
        """
        Function called every time we receive a new result.
        Store the result in the corresponding Mongodb collection.
        """
        measurement_result = self.strategy.preprocess(args[0])
        print('Received result')
        probe_mesh = ProbeMeasurement(**measurement_result[0])
        hops = measurement_result[1]
        hop_total = len(hops)
        measurementpoint_id =  DataManager.store(self, probe_mesh, self.measurement.id, hop_total)
        for hop in hops:
            hop = HopFormat(**hop)
            DataManager.store_hops(self, hop, measurementpoint_id)

        return
        analyzed = self.strategy.analyze(measurement_result)
        anomalies = self.strategy.filter(analyzed)
        if len(anomalies) > 0:
            for anomaly in anomalies:
                detection_method = DetectionMethod.objects.get(type=self.measurement.type)

                Anomaly.objects.create(time=anomaly['alert_time'],
                                       ip_adress='127.0.0.1',  # Dummy data
                                       asn_settings_id=1234,
                                       description=anomaly['description'],
                                       measurement_type=self.measurement.type,
                                       detection_method_id=detection_method,
                                       medium_value=0,  # Dummy data
                                       value=0,  # Dummy data
                                       anomaly_score=0,  # Dummy data
                                       preditction_value=False,
                                       asn_error=1111)  # Dummy data

    def on_error(*args):
        "got in on_error"
        print(args)
        raise ConnectionError("Error")

    def on_connect(self, *args):
        print(f"{self}, connected with Ripe Atlas")

    def on_reconnect(*args):
        print("got in on_reconnect")
        print(args)
        raise ConnectionError("Reconnection")

    def on_close(*args):
        print("got in on_close")
        print(args)
        raise ConnectionError("Closed")

    def on_disconnect(self, *args):
        print("got in on_disconnect")
        print(args)
        time.sleep(2)
        print("reconnecting...")
        self.monitor()

    def on_connect_error(*args):
        print("got in on_connect_error")
        print(args)
        raise ConnectionError("Connection Error")

    def on_atlas_error(*args):
        print("got in on_atlas_error")
        print(args)

    def on_atlas_unsubscribe(*args):
        print("got in on_atlas_unsubscribe")
        print(args)
        raise ConnectionError("Unsubscribed")

    #Streaming API for monitoring measurementcollections
    def monitor(self):
        print("Starting monitor")
        timezone = pytz.timezone('UTC')

        count = MeasurementPoint.objects.filter(time__gt=(datetime.datetime.now(timezone)-datetime.timedelta(hours=24)))
        if not count.exists():
            print('collecting data')
            self.strategy.collect_initial_dataset(self.measurement.measurement_id)

        atlas_stream = AtlasStream()
        atlas_stream.connect()
        # Measurement results
        channel = "atlas_result"
        # Bind function we want to run with every result message received
        atlas_stream.socketIO.on("connect", self.on_connect)
        atlas_stream.socketIO.on("disconnect", self.on_disconnect)
        atlas_stream.socketIO.on("reconnect", self.on_reconnect)
        atlas_stream.socketIO.on("error", self.on_error)
        atlas_stream.socketIO.on("close", self.on_close)
        atlas_stream.socketIO.on("connect_error", self.on_connect_error)
        atlas_stream.socketIO.on("atlas_error", self.on_atlas_error)
        atlas_stream.socketIO.on("atlas_unsubscribed", self.on_atlas_unsubscribe)
        # Subscribe to new stream
        atlas_stream.bind_channel(channel, self.on_result_response)

        print(self.measurement)
        stream_parameters = {"msm": self.measurement.measurement_id}
        atlas_stream.start_stream(stream_type="result", **stream_parameters)

        # run forever
        atlas_stream.timeout(seconds=None)
        # Shut down everything
        atlas_stream.disconnect()

    def start(self):
        # x = threading.Thread(target=self.monitor)
        # x.start()
        print('Starting multithreading')
        print(f"Starting {self}")
        # db.connections.close_all()
        # self.process = multiprocessing.Process(target=self.monitor, name=self)
        # self.process.start()
        self.monitor()

    def end(self):
        print(f"Terminating {self}")
        self.process.terminate()

    def restart(self):
        self.end()
        self.start()

    def update_model(self):
        """this function needs to be called when feedback is given and model needs to be trained again.
            after training this function should restart the monitoring process
        """
        pass

# test = {'probe_id': 6660, 'created': datetime.datetime(2022, 4, 12, 8, 4, 41), 'entry_rtt': 'inf', 'entry_ip': '2401:ee00:104:3::2', 'entry_as': 'nan'}
# probe_mesh = ProbeMeasurement(**test)

# probe_mesh.save_to_database()
#DataManager().store(probe_mesh, 7)
