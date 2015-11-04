# coding: utf-8

from app_scripts.RosAPI import Core

__author__ = 'Jeka'

def ret_data(data):
            return_data = []
            for x in data:
                return_data.append(x)
            return return_data

# Включаем клиента
def clientOn(device_ip_address, port, device_login, device_password, ip_client):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/print", "=.proplist="+".id,address",]))):
        try:
            if rule["address"] == ip_client:
                mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/enable", "=.id=" + rule[".id"],]))
        except:
            pass


# Отключаем клиента
def clientOff(device_ip_address, port, device_login, device_password, ip_client):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/print", "=.proplist="+".id,address",]))):
        try:
            if rule["address"] == ip_client:
                mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/disable", "=.id=" + rule[".id"],]))
        except:
            pass


if __name__ == '__main__':
    clientOff('192.168.85.1', 8728, 'ubnt', 'ubnt', '172.16.16.10')
    import time
    time.sleep(1)
    #clientOn('192.168.85.1', 8728, 'ubnt', 'ubnt', '172.16.16.10')