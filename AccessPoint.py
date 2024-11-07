import network
import time

class AccessPoint:
    """ 
    Class that provides the functionality to start/stop an Access Point
    """

    def __init__(self) -> None:       
        self.__ap: network.WLAN

    def start(self, ap_ssid: str, ap_pwd: str) -> None:
        """
        Start the acces point
        """
        try:
            self.__ap = network.WLAN(network.AP_IF)
            self.__ap.config(essid=ap_ssid, password=ap_pwd)
            self.__ap.active(True)
        except Exception as ex:
            print(f"Failed to start access point with exception: {ex}")

        while not self.__ap.active:
            print("Waiting")
            time.sleep(0.2)
        
        print(f'Access point started with {self.__ap.ifconfig()}!')

    def stop(self) -> None:
        """
        Stops the acces point
        """
        print("Access point stoped!")
        self.__ap.active(False)