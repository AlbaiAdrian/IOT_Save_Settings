from access_point import AccessPoint
from services.file_reader_service import FileReaderService
from services.json_settings_service import JsonSettingsService
from web_server import WebServer
from wifi import Wifi


def credentials_saved_callback() -> None:
    web_server.stop()
    ap.stop()
    ssid, ssid_pwd = json_settings_service.get_wifi_settings()
    if not wifi_connector.connect_to_wifi(ssid, ssid_pwd):
        wifi_connector.disconnect_from_wifi()
        print("Wifi not connected!")
        ap_ssid, ap_pwd = json_settings_service.get_ap_settings()
        ap.start(ap_ssid, ap_pwd)
        web_server.start()
        return
    print("Wifi connected!")


file_reader_service = FileReaderService()
json_settings_service = JsonSettingsService()

ap_ssid, ap_pwd = json_settings_service.get_ap_settings()

ap = AccessPoint()

web_server = WebServer(port=80, data_saved_callback=credentials_saved_callback, file_reader_service=file_reader_service, json_settings_service=json_settings_service)

wifi_connector = Wifi()

ap.start(ap_ssid, ap_pwd)
web_server.start()
print("Nu ajunge aici")
