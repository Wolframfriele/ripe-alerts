import re
from datetime import datetime
import requests
from ripe.atlas.sagan import TracerouteResult
result_pattern = re.compile("{.*(stored_timestamp).*}")


def collect_initial_dataset(measurement_id):

    print(f"collecting initial dataset for measurement: {measurement_id}")
    yesterday = int(datetime.now().timestamp()) - 24 * 60 * 60
    response = requests.get(
        f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results?start={yesterday}",
        stream=True)

    result_string = ""

    for i in response.iter_content(decode_unicode=True):
        result_string += i
        result = result_pattern.search(result_string)
        if result:
            start, end = result.span()
            traceroute_result_raw = result_string[start:end]
            result_string = result_string[end:]
            print(result_string, end="\n\n")
            print(traceroute_result_raw, end="\n\n")
            nice = TracerouteResult(traceroute_result_raw)


collect_initial_dataset(1790205)
