import requests

API_URL = "https://atlas.ripe.net/api/v2/anchors"

class ProbeRequest:

    def __init__(self) -> None:
        pass
    data = []  

    def get_probe_location(self, probe_id):
        if len(self.data) == 0:
            for i in range(12):
                i += 1
                try: 
                    response = requests.get(API_URL + f"?page={i}").json()
                    for res in response['results']:
                        self.data.append(res)
                except:
                    pass
        else:
            pass
        for item in self.data:
            if item['probe'] == probe_id:
                city = item['city']
                country = item['country']
                as_number = item['as_v4']
        
        return {
            "city": city,
            "country": country,
            "as_number": as_number
        }

