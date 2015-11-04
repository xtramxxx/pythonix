# coding: utf-8

''' Скрипт для работы с тарифами в Mikrotik '''

from app_scripts.RosAPI import Core

__author__ = 'Jeka'

def ret_data(data):
            return_data = []
            for x in data:
                return_data.append(x)
            return return_data


# Добабление правил шейпера при создании тарифа
def createTarifAddQueue(device_ip_address, port, device_login, device_password, speed_up, speed_up_unity, speed_down, speed_down_unity):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    mikrotik.response_handler(mikrotik.talk(["/ppp/profile/add", "=name=" + str(speed_up)+speed_up_unity+str(speed_down)+speed_down_unity,
        "=rate-limit=" + str(speed_up)+speed_up_unity+"/"+str(speed_down)+speed_down_unity,]))


# Удаление правил шейпера после удаления тарифа
def deleteTarifAndQueue(device_ip_address, port, device_login, device_password, speed_up, speed_up_unity, speed_down, speed_down_unity):
    mikrotik = Core(device_ip_address, port=port)
    mikrotik.login(device_login, device_password)
    for rule in ret_data(mikrotik.response_handler(mikrotik.talk(["/ppp/profile/print", "=.proplist="+".id,rate-limit",]))):
        try:
            if rule["rate-limit"] == str(speed_up)+speed_up_unity+"/"+str(speed_down)+speed_down_unity:
                mikrotik.response_handler(mikrotik.talk(["/ppp/profile/remove", "=.id=" + rule[".id"],]))
                print rule[".id"]
        except:
            pass

if __name__ == "__main__":
    deleteTarifAndQueue("192.168.88.1", 8728, 'ubnt', 'ubnt', 2, 'M', 2, 'M')
