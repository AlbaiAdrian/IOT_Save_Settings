import json

_MODULE_PATH = __file__.replace("\\", "/")
_PACKAGE_PATH = _MODULE_PATH.rsplit("/", 2)[0]


class JsonSettingsService:

    __TEMPLATE_JSON = _PACKAGE_PATH + "/json_data/data_entry_template.json"
    __WIFI_SETTINGS_JSON = _PACKAGE_PATH + "/json_data/wifi_settings_data.json"
    __AP_SETTINGS_JSON = _PACKAGE_PATH + "/json_data/ap_settings_data.json"
    __OTHER_SETTINGS_JSON = _PACKAGE_PATH + "/json_data/other_settings.json"

    def __init__(self) -> None:
        pass

    def save_wifi_settings(self, ssid: str, ssid_pwd: str) -> None:
        with open(self.__WIFI_SETTINGS_JSON, 'w') as file:
            json.dump({'ssid': ssid, 'ssid_pwd': ssid_pwd}, file)

    def get_wifi_settings(self):
        json_data = self.__read_json(self.__WIFI_SETTINGS_JSON)
        return json_data["ssid"], json_data["ssid_pwd"]

    def get_ap_settings(self):
        json_data = self.__read_json(self.__AP_SETTINGS_JSON)
        return json_data["ap_ssid"], json_data["ap_pwd"]

    def get_data_template_json(self):
        data = self.__read_json(self.__TEMPLATE_JSON)
        return [setting for setting in data if setting["fieldName"] not in ("", "labelText")]

    def get_other_settings(self):
        return self.__read_json(self.__OTHER_SETTINGS_JSON)

    def save_other_settings(self, settings: dict[str, str]) -> None:
        other_settings: dict[str, str] = {}
        data_template_json = self.get_data_template_json()
        for template_setting in data_template_json:
            key_name = template_setting["fieldName"]
            other_settings[key_name] = settings[key_name]
        with open(self.__OTHER_SETTINGS_JSON, 'w') as file:
            json.dump(other_settings, file)

    def __read_json(self, path):
        with open(path, 'r') as file:
            return json.load(file)
