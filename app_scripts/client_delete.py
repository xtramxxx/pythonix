# coding: utf-8

from app_scripts.RosAPI import Core

__author__ = 'Jeka'

def ret_data(data):
            return_data = []
            for x in data:
                return_data.append(x)
            return return_data

# Удаление PPP учетки
def deletePPP(device_ip_address, port, device_login, device_password, ip_client):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ppp/secret/print", "=.proplist="+".id,remote-address",]))):
        try:
            if rule["remote-address"] == ip_client:
                mikrotik.response_handler(mikrotik.talk(["/ppp/secret/remove", "=.id=" + rule[".id"],]))
        except:
            pass


# Удаление адреса в Адрес лист
def deleteAddressList(device_ip_address, port, device_login, device_password, ip_client):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/print", "=.proplist="+".id,address",]))):
        try:
            if rule["address"] == ip_client:
                mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/remove", "=.id=" + rule[".id"],]))
        except:
            pass


if __name__ == '__main__':
    deletePPP('192.168.88.1', 8728, 'ubnt', 'ubnt', '10.10.10.10')
    deleteAddressList('192.168.88.1', 8728, 'ubnt', 'ubnt', '10.10.10.10')

    #clientOn('192.168.85.1', 8728, 'ubnt', 'ubnt', '172.16.16.10')