# coding: utf-8

''' Скрипт для работы с клиентами в Mikrotik '''

from app_scripts.RosAPI import Core

__author__ = 'Jeka'

def ret_data(data):
            return_data = []
            for x in data:
                return_data.append(x)
            return return_data


# Добабление клиента
def addClient(device_ip_address, port, device_login, device_password, login_client, password_client,
        ip_client, ipv6_client, speed_up, speed_up_unity, speed_down, speed_down_unity):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    mikrotik.response_handler(mikrotik.talk(["/ppp/secret/add", "=name=" + login_client, "=password=" + password_client,
        "=local-address=" + device_ip_address, "=remote-address=" + ip_client,
        "=profile=" + str(speed_up)+speed_up_unity+str(speed_down)+speed_down_unity]))
    mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/add", "=address=" + ip_client, "=list=" + "internet",]))



if __name__ == "__main__":
    addClient('192.168.88.1', 8728, 'ubnt', 'ubnt', 'probz', 'probz', '10.2.2.2', '', '100', 'M', '100', 'M')
