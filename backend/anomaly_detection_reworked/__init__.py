import os
import signal
import sys

import django

server_shutdown_event = django.dispatch.Signal()


def server_shutdown_event_handler(*args):
    if os.environ.get('RUN_MAIN') == 'true':
        server_shutdown_event.send(sender=server_shutdown_event.__class__)
    sys.exit(0)


signal.signal(signal.SIGINT, server_shutdown_event_handler)
