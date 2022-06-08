class EventLogger:

    def on_reconnect(*args):
        print(args)
        print("Reconnecting to RIPE Atlas Streaming API")
        raise ConnectionError("Reconnection")

    def on_error(self, *args):
        print(args)
        print("A connection error occurred at the RIPE Atlas Streaming API.")
        raise ConnectionError("Error")

    def on_connect(self):
        print("Successfully connected to the RIPE Atlas Streaming API.")

    def on_close(self, *args):
        print("Connection to RIPE Atlas Streaming API has been closed.")
        print(args)
        raise ConnectionError("Closed")

    def on_disconnect(self, *args):
        print("Disconnected from the RIPE Atlas Streaming API.")

    def on_connect_error(*args):
        print("Error while connecting to RIPE Atlas Streaming API.")
        print(args)
        raise ConnectionError("Connection Error")

    def on_atlas_error(*args):
        print("A RIPE Atlas Streaming API error occurred.")
        print(args)

    def on_atlas_unsubscribe(*args):
        print("Unsubscribed to channel")
        print(args)
        # raise ConnectionError("Unsubscribed")