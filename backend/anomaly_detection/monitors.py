import datetime
import os
import time
from ripe.atlas.cousteau import *
import multiprocessing
from .monitor_strategy_base import MonitorStrategy
from database.models import MeasurementCollection, Anomaly, DetectionMethod, AutonomousSystem, Probe, MeasurementPoint, Hop
from .format import ProbeMeasurement, Hops


class DataManager:
    def __init__(self) -> None:
        pass

    def store(self, probe_measurement: ProbeMeasurement, measurement_id):
        obj, created_probe = Probe.objects.get_or_create(probe=probe_measurement.probe_id,
                                                    measurement_id=measurement_id,
                                                    as_number=1103, #dummy data
                                                    location='Amsterdam') # dummy data

        # print(probe_measurement.probe_id, measurement_id)
        # print(probe_measurement)
        # probe_measurement.save_to_database()

        # # probe = Probe.objects.create(probe=probe_measurement.probe_id,
        # #                                 measurement_id=measurement_id,
        # #                                 as_number=1103, #dummy data
        # #                                 location='Amsterdam') # dummy data
        # # probe.save()

        # print(Probe.objects.filter(probe=probe_measurement.probe_id, measurement_id=measurement_id))
        # if not Probe.objects.filter(probe=probe_measurement.probe_id, measurement_id=measurement_id).exists():
        #     print('test')

        # else:
        #     pass

        # probe_id = Probe.objects.get(probe=probe_measurement.probe_id, measurement_id=measurement_id)
        
        object, created_point = MeasurementPoint.objects.get_or_create(probe=obj,
                                        time=probe_measurement.created,
                                        round_trip_time_ms=probe_measurement.entry_rtt,
                                        hops_total=12)  # dummy data

        print('Probe ' + str(probe_measurement.probe_id) + ' is saved!')

        return object.id

    def store_hops(self, hops: Hops, measurementpoint_id):
        hop_data = Hop.objects.create(measurement_point_id=measurementpoint_id,
                        current_hop=hops.hop,
                        round_trip_time_ms=hops.min_rtt,
                        ip_address=hops.ip_address)
        hop_data.save()

    # def store(self, measurement_data, measurement_id):
    #     print('1')
    #     print(measurement_data)
    #     probe_number = measurement_data['probe_id']
    #     print(probe_number)
    #     probe = Probe(probe=probe_number,
    #                   measurement_id=measurement_id,
    #                   as_number=0000,  # dummy data
    #                   location='Amsterdam')  # dummy data
    #     probe.save()
    #     print('Probes are saved')

    #     probe_id = Probe.objects.get(probe=measurement_data['probe_id'], measurement_id=MeasurementCollection)

    #     MeasurementPoint.objects.create(probe_id=probe_id,
    #                                     time=measurement_data['created'],
    #                                     round_trip_time_ms=measurement_data['entry_rtt'],
    #                                     hops_total=12)  # dummy data
    #     print('Measurementpoints are saved')

    # def store(self, measurement_data, measurement_id):
    # print('1')
    # print(measurement_data)
    # probe = Probe(probe=measurement_data['probe_id'],
    #                 measurement_id=measurement_id,
    #                 as_number=0000, #dummy data
    #                 location='Amsterdam') #dummy data
    # probe.save()
    # print('Probes are saved')

    # probe_id = Probe.objects.get(probe=measurement_data['probe_id'], measurement_id=MeasurementCollection)

    # MeasurementPoint.objects.create(probe_id=probe_id,
    #                                 time=measurement_data['created'],
    #                                 round_trip_time_ms=measurement_data['entry_rtt'],
    #                                 hops_total=12) #dummy data
    # print('Measurementpoints are saved')


class Monitor:
    def __init__(self, MeasurementCollection: MeasurementCollection, strategy: MonitorStrategy):

        self.measurement = MeasurementCollection
        self.strategy = strategy

    def __str__(self):
        return f"Monitor for {self.measurement.type} measurement: {self.measurement.measurement_id}"

    def on_result_response(self, *args):
        """
        Function called every time we receive a new result.
        Store the result in the corresponding Mongodb collection.
        """
        measurement_result = self.strategy.preprocess(args[0])
        print('Received result')
        print(measurement_result)
        probe_mesh = ProbeMeasurement(**measurement_result)
        print(type(probe_mesh.entry_as))
        # hops = measurement_result[1]
        stored_data =  DataManager.store(self, probe_mesh, self.measurement.id)

        # for hop in hops:
        #     hop = Hops(**hop)
        #     DataManager.store_hops(self, hop, stored_data)

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

    def monitor(self):
        print("Starting monitor")
        # yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
        # count = self.collection.count_documents(filter={"created": {"$lt": yesterday}})
        # if count == 0:
        #     self.strategy.collect_initial_dataset(self.collection, self.measurement.measurement_id)

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

test = {'probe_id': 6660, 'created': datetime.datetime(2022, 4, 12, 8, 4, 41), 'entry_rtt': 'inf', 'entry_ip': '2401:ee00:104:3::2', 'entry_as': 'nan'}
probe_mesh = ProbeMeasurement(**test)

probe_mesh.save_to_database()
#DataManager().store(probe_mesh, 7)
