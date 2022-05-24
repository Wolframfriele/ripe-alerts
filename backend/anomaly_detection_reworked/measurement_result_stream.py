from ripe.atlas.cousteau import AtlasStream


def on_reconnect(*args):
    print("got in on_reconnect")
    print(args)
    raise ConnectionError("Reconnection")


class MeasurementResultStream:

    def __init__(self):
        self.stream = AtlasStream()
        self.stream.connect()
        # Bind function we want to run with every result message received
        self.stream.socketIO.on("connect", self.on_connect)
        self.stream.socketIO.on("disconnect", self.on_disconnect)
        self.stream.socketIO.on("reconnect", on_reconnect)
        self.stream.socketIO.on("error", self.on_error)
        self.stream.socketIO.on("close", self.on_close)
        self.stream.socketIO.on("connect_error", self.on_connect_error)
        self.stream.socketIO.on("atlas_error", self.on_atlas_error)
        self.stream.socketIO.on("atlas_unsubscribed", self.on_atlas_unsubscribe)
        # Subscribe to new stream
        self.stream.bind_channel("atlas_result", self.on_result_response)

        stream_parameters = {"msm": 9181642}
        self.stream.start_stream(stream_type="result", **stream_parameters)
        self.stream.timeout(seconds=None)  # Run forever

    def on_error(self, *args):
        print(args)
        raise ConnectionError("Error")

    def on_connect(self):
        print("Connected with the RIPE Atlas Streaming API")

    def on_close(self, *args):
        print("got in on_close")
        print(args)
        raise ConnectionError("Closed")

    def on_disconnect(self, *args):
        print("Disconnected with the RIPE Atlas Streaming API")
        pass

    def on_connect_error(*args):
        print("got in on_connect_error")
        print(args)
        # raise ConnectionError("Connection Error")

    def on_atlas_error(*args):
        print("got in on_atlas_error")
        print(args)

    def on_atlas_unsubscribe(*args):
        print("got in on_atlas_unsubscribe")
        print(args)
        # raise ConnectionError("Unsubscribed")

    def on_result_response(*args):
        """
        Function that will be called every time we receive a new result.
        Args is a tuple, so you should use args[0] to access the real message.
        """
        print(args[0])

    #
    # def start(self):
    #     self.stream.connect()
