from Services.JsonSettingsService import JsonSettingsService
import network
import time

class Wifi:
    """
    Class that provides the functionality to connect/disconect to/from a Wifi
    """
    def __init__(self) -> None:
        self.__wlan: network.WLAN

    def connectToWifi(self, ssid: str, ssid_pwd: str) -> bool:
        self.__wlan = network.WLAN(network.STA_IF)
        self.__wlan.active(True)
        self.__wlan.connect(ssid, ssid_pwd)
        
        for _ in range(25):
            if self.__wlan.isconnected():
                return True
            print('Connecting ....')
            time.sleep(1)
        
        self.__wlan.active(False)
        return False        
        
    def disconnectFromWifi(self) -> None:
        if self.__wlan.isconnected():
            self.__wlan.disconnect()
        self.__wlan.active(False)
        