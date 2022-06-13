from typing import List

from ripe.atlas.cousteau import AtlasStream

from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.event_logger import EventLogger
from anomaly_detection_reworked.measurement_type import MeasurementType


class MeasurementResultStream:

    def __init__(self, detection_methods: List[DetectionMethod]):
        """
        Initialize this instance before connecting to the RIPE ATLAS Streaming API.
        First, retrieve measurements IDs from database.
        Second, pre-generate Detection Method data for later use.
        Third, bind functions to the event logger and lastly connect to the Streaming API.
        """
        self.measurement_id_to_measurement_type: dict[int, MeasurementType] = {}  # Int represents a Measurement ID.
        self.measurement_type_to_detection_method: dict[MeasurementType, List[DetectionMethod]] = {}
        self.detection_methods = detection_methods

        from database.models import MeasurementCollection
        measurement_collections = MeasurementCollection.objects.all()  # Retrieve measurements from database.
        self.measurement_ids = list(measurement_collections.values_list('measurement_id', flat=True))
        if len(self.measurement_ids) == 0:
            print("Start-up canceled. At least one measurement ID is required to start up the Streaming API.")
            return

        # Generate a Dictionary. (Key: Measurement ID and Value: Measurement Type).
        list_id_type = list(measurement_collections.values_list('measurement_id', 'type'))
        self.measurement_id_to_measurement_type = {x[0]: MeasurementType.convert(x[1]) for x in list_id_type}

        # Precalculate a Dictionary for later use. (Key: Measurement Type and Value: Array of Detection Methods).
        for msm_type in MeasurementType:
            methods_list: list = []
            for method in self.detection_methods:
                if method.get_measurement_type == msm_type:
                    methods_list.append(method)
                self.measurement_type_to_detection_method[msm_type] = methods_list

        self.stream = AtlasStream()
        self.logger = EventLogger()
        self.stream.connect()
        # Bind functions we want to run with every result message received
        self.stream.socketIO.on("connect", self.logger.on_connect)
        self.stream.socketIO.on("disconnect", self.logger.on_disconnect)
        self.stream.socketIO.on("reconnect", self.logger.on_reconnect)
        self.stream.socketIO.on("error", self.logger.on_error)
        self.stream.socketIO.on("close", self.logger.on_close)
        self.stream.socketIO.on("connect_error", self.logger.on_connect_error)
        self.stream.socketIO.on("atlas_error", self.logger.on_atlas_error)
        self.stream.socketIO.on("atlas_unsubscribed", self.logger.on_atlas_unsubscribe)
        self.stream.bind_channel("atlas_result", self.on_result_response)
        try:
            # Start the stream, and add one measurement ID (we can't start with multiple IDs)
            stream_parameters = {"msm": self.measurement_ids[0]}
            self.stream.start_stream(stream_type="result", **stream_parameters)
            # Subscribe to stream with other IDs, and skip the first one.
            for measurement_id in self.measurement_ids[1:]:
                stream_parameters = {"msm": measurement_id}
                self.stream.subscribe(stream_type="result", **stream_parameters)

            self.stream.timeout(seconds=None)  # Run forever
        except KeyboardInterrupt:
            self.logger.on_disconnect(None)

    def on_result_response(self, *args):
        """
        Method that will be called every time we receive a new result.
        Args is a tuple, so you should use args[0] to access the real message.
        """
        result = args[0]
        msm_id = result['msm_id']
        detection_methods = self.get_corresponding_detection_methods(msm_id)
        for method in detection_methods:
            method.on_result_response(result)

    def get_corresponding_detection_methods(self, measurement_id: int) -> List[DetectionMethod]:
        """
        Method that will retrieve the corresponding Detection Methods based of the Measurement ID.
        Each Measurement ID has a Measurement Type.
        Each Detection Method has a Measurement Type.
        Measurement ID <-> MeasurementType <-> Detection Method.
        Since the detection methods and measurement IDs won't change at this point, I precalculated
        all the detection methods by MeasurementType in a dictionary, so I won't need a for-loop.
        """
        measurement_type: MeasurementType = self.measurement_id_to_measurement_type[measurement_id]
        methods: List[DetectionMethod] = self.measurement_type_to_detection_method[measurement_type]
        return methods
