import ipaddress
import http.client
import json

prefixes = []

def checkASbyIP(IP):
    conn = http.client.HTTPSConnection("stat.ripe.net")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/data/network-info/data.json?resource={}".format(IP), headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    jsondata = json.loads(data)
    return jsondata['data']['asns'][0]

def getPrefixesForAS(AS):
    ASlist = []
    conn = http.client.HTTPSConnection("stat.ripe.net")
    headers = {
    'cache-control': "no-cache"
    }
    conn.request("GET", "/data/announced-prefixes/data.json?resource=as{}".format(AS), headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    jsondata = json.loads(data) 
    for prefix in list(range(len(jsondata['data']['prefixes']))):
        ASlist.append(str(jsondata['data']['prefixes'][prefix]['prefix']))
    return ASlist

def findIPinMultiplePrefixes(IP, prefixes):
    print(prefixes)
    for prefix in prefixes:
        address_in_network = ipaddress.ip_address(IP) in ipaddress.ip_network(prefix)
        if address_in_network == True:
            break
            return True
    return False

list_of_prefixes = getPrefixesForAS(1103)
print(findIPinMultiplePrefixes('83.89.192.210', list_of_prefixes))
