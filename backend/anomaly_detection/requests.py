import requests

API_URL = "https://atlas.ripe.net/api/v2/anchors"

def get_probe_location(probe_id):
    data = []

    if len(data) == 0:
        for i in range(12):
            i += 1
            try: 
                response = requests.get(API_URL + f"?page={i}").json()
                for res in response['results']:
                    data.append(res)
            except:
                pass
    else:
        pass
    for item in data:
        if item['probe'] == probe_id:
            city = item['city']
            country = item['country']
            as_number = item['as_v4']
            print(country, city, as_number)
    
    return {
        "city": city,
        "country": country,
        "as_number": as_number
    }

