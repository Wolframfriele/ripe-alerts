import ipaddress

ip = ipaddress.ip_address('192.168.1.1')
prefix = ipaddress.ip_network('192.168.0.0/23')

address_in_network = ip in prefix

print(address_in_network)
