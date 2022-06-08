from typing import List

from ripe.atlas.cousteau import AtlasStream

from anomaly_detection_reworked.event_logger import EventLogger


class MeasurementResultStream:

    def __init__(self, measurement_ids: List[int]):
        try:
            if len(measurement_ids) == 0:
                raise ValueError("At least one measurement ID is required to start up the Streaming API.")
            self.stream = AtlasStream()
            self.stream.connect()
            self.logger = EventLogger()
            # Bind function we want to run with every result message received
            self.stream.socketIO.on("connect", self.logger.on_connect)
            self.stream.socketIO.on("disconnect", self.logger.on_disconnect)
            self.stream.socketIO.on("reconnect", self.logger.on_reconnect)
            self.stream.socketIO.on("error", self.logger.on_error)
            self.stream.socketIO.on("close", self.logger.on_close)
            self.stream.socketIO.on("connect_error", self.logger.on_connect_error)
            self.stream.socketIO.on("atlas_error", self.logger.on_atlas_error)
            self.stream.socketIO.on("atlas_unsubscribed", self.logger.on_atlas_unsubscribe)
            self.stream.bind_channel("atlas_result", self.on_result_response)

            # Subscribe to new stream
            stream_parameters = {"msm": measurement_ids[0]}
            self.stream.start_stream(stream_type="result", **stream_parameters)
            for measurement_id in measurement_ids[1:]:
                stream_parameters = {"msm": measurement_id}
                self.stream.subscribe(stream_type="result", **stream_parameters)
            # stream_parameters = {"msm": 3534345}
            # self.stream.subscribe(stream_type="result", **stream_parameters)
            self.stream.timeout(seconds=None)  # Run forever
        except KeyboardInterrupt:
            self.logger.on_disconnect(None)

    def on_result_response(*args):
        """
        Function that will be called every time we receive a new result.
        Args is a tuple, so you should use args[0] to access the real message.
        """
        msm_id = args[1]['msm_id']

        # print(args[1])
        print(args[1])
        # pass
