# coding: utf-8

from app_scripts.RosAPI import Core

__author__ = 'Jeka'

def ret_data(data):
            return_data = []
            for x in data:
                return_data.append(x)
            return return_data


# Обновление логина клиента
def updateLogin(device_ip_address, port, device_login, device_password, login_client_old, login_client_new):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ppp/secret/print", "=.proplist="+".id,name",]))):
        try:
            if rule["name"] == login_client_old:
                print "Update login" + rule[".id"]
                mikrotik.response_handler(mikrotik.talk(["/ppp/secret/set", "=name=" + login_client_new, "=.id=" + rule[".id"],]))
        except:
            pass


# Обновляем IP адрес в Address List
def updateIP(device_ip_address, port, device_login, device_password, ip_client_old, ip_client_new):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/print", "=.proplist="+".id,address",]))):
        try:
            if rule["address"] == ip_client_old:
                print "Update IP" + rule[".id"]
                mikrotik.response_handler(mikrotik.talk(["/ip/firewall/address-list/set", "=address=" + ip_client_new, "=.id=" + rule[".id"],]))
        except:
            pass


# Обновляем IP адрес в PPP
def updatePPPIP(device_ip_address, port, device_login, device_password, ip_client_old, ip_client_new):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ppp/secret/print", "=.proplist="+".id,remote-address",]))):
        try:
            if rule["remote-address"] == ip_client_old:
                print "Update IP" + rule[".id"]
                mikrotik.response_handler(mikrotik.talk(["/ppp/secret/set", "=remote-address=" + ip_client_new, "=.id=" + rule[".id"],]))
        except:
            pass


# Обновляем Пароль в PPP
def updatePPPassword(device_ip_address, port, device_login, device_password, password_client_old, password_client_new):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ppp/secret/print", "=.proplist="+".id,password",]))):
        print rule
        try:
            if rule["password"] == password_client_old:
                print "Update IP" + rule[".id"]
                mikrotik.response_handler(mikrotik.talk(["/ppp/secret/set", "=password=" + password_client_new, "=.id=" + rule[".id"],]))
        except:
            pass


if __name__ == "__main__":
    #updateLogin('192.168.88.1', 8728, 'ubnt', 'ubnt', 'vz_go55', 'vz_go575')
    updatePPPassword('192.168.88.1', 8728, 'ubnt', 'ubnt', '10.2.2.2', '10.2.2.3')