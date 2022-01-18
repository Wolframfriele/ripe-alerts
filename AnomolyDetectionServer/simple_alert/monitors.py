import datetime
import os
import time

from dotenv import load_dotenv
from pymongo import MongoClient, DESCENDING
from ripe.atlas.cousteau import *
import threading
import multiprocessing
from .monitor_strategies import MonitorStrategy

username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')


class Measurement:
    def __init__(self, id, type):
        self.id = id
        self.type = type


class Monitor:

    def __init__(self, measurement: Measurement, alert_configurations, strategy: MonitorStrategy):

        self.measurement = measurement
        self.strategy = strategy

        # variables related to mongo db should be initialized when we start a monitoring process
        self.client: MongoClient = None
        self.database = None
        self.process: multiprocessing.Process = None
        self.collection = None

    def __str__(self):
        return f"Montitor for {self.measurement.type} measurement: {self.measurement.id}"

    def on_result_response(self, *args):
        """
        Function called every time we receive a new result.
        Store the result in the corresponding Mongodb collection.
        """
        measurement_result = self.strategy.preprocess(args[0])
        print('Received result')
        self.strategy.store(self.collection, measurement_result)
        is_anomality = self.strategy.analyze(self.collection, measurement_result)
        if is_anomality:
            print("oh no, something went wrong, alert is being generated")

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

    def init_db(self):
        self.client = MongoClient(f'mongodb://{username}:{password}@mongodb')
        self.database = self.client['Atlas_Results']
        self.collection = self.database[f'{self.measurement.type} measurement: {self.measurement.id}']
        self.collection.create_index([("created", DESCENDING)])

    def monitor(self):

        self.init_db()

        yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
        count = self.collection.count_documents(filter={"created": {"$lt": yesterday}})
        if count == 0:
            self.strategy.collect_initial_dataset(self.collection, self.measurement.id)

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

        stream_parameters = {"msm": self.measurement.id}
        atlas_stream.start_stream(stream_type="result", **stream_parameters)

        # run forever
        atlas_stream.timeout(seconds=None)
        # Shut down everything
        atlas_stream.disconnect()

    def start(self):
        # x = threading.Thread(target=self.monitor)
        # x.start()
        print(f"Starting {self}")
        self.process = multiprocessing.Process(target=self.monitor, name=self)
        self.process.start()

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

