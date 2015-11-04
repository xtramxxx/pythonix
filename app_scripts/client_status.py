# coding: utf-8

from app_scripts.RosAPI import Core

__author__ = 'Jeka'

def ret_data(data):
            return_data = []
            for x in data:
                return_data.append(x)
            return return_data

# Поиск в ARP таблице
def getArp(device_ip_address, port, device_login, device_password, ip_client):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ip/arp/print", "=.proplist="+".id,address",]))):
        try:
            if rule["address"] == ip_client:
               return True
        except:
            pass


# Поиск в подключенных PPP
def getPPP(device_ip_address, port, device_login, device_password, ip_client):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ppp/active/print", "=.proplist="+".id,address",]))):
        try:
            if rule["address"] == ip_client:
               return True
        except:
            pass




if __name__ == '__main__':
    print getPPP('192.168.99.1', 8728, 'ubnt', 'ubnt', '172.16.15.78')
    import time
    time.sleep(1)
    #clientOn('192.168.85.1', 8728, 'ubnt', 'ubnt', '172.16.16.10')