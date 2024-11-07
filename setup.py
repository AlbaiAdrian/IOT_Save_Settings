from Services.JsonSettingsService  import JsonSettingsService
from AccessPoint import AccessPoint
from Services.FileReaderService import FileReaderService
from WebServer import WebServer
from Wifi import  Wifi


def credentialsSavedCallack() -> None:
    webServer.stop()
    ap.stop()
    ssid, ssid_pwd = jsonSettingsService.getWifiSettings()
    if not wifiConnecter.connectToWifi(ssid, ssid_pwd):
        wifiConnecter.disconnectFromWifi()
        print("Wifi not connected!")
        ap_ssid, ap_pwd = jsonSettingsService.getAPSettings()
        ap.start(ap_ssid, ap_pwd)
        webServer.start()
        return
    print("Wifi connected!")


fileReaderService = FileReaderService()
jsonSettingsService = JsonSettingsService()

ap_ssid, ap_pwd = jsonSettingsService.getAPSettings()

ap = AccessPoint()

webServer = WebServer(port=80, dataSavedCallack=credentialsSavedCallack, fileReaderService=fileReaderService, jsonSettingsService=jsonSettingsService)

wifiConnecter = Wifi()

ap.start(ap_ssid, ap_pwd)
webServer.start()
print("Nu ajunge aici")