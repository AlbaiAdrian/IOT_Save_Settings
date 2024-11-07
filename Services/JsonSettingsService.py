import json

class JsonSettingsService:

    __TEMPLATE_JSON = "JsonData/DataEntryTemplate.json"
    __WIFI_SETTINGS_JSON = "JsonData/WifiSettingsData.json"
    __AP_SETTINGS_JSON = "JsonData/APSettingsData.json"
    __OTHER_SETTINGS_JSON = "JsonData/OtherSettings.json"

    def __init__(self) -> None:
        pass
        
    def saveWifiSettings(self, ssid: str, ssid_pwd: str ) -> None:
        with open(self.__WIFI_SETTINGS_JSON, 'w') as file:
            json.dump({'ssid': ssid, 'ssid_pwd': ssid_pwd} , file)

    def getWifiSettings(self):
        jsonData = self.__readJson(self.__WIFI_SETTINGS_JSON)
        return jsonData["ssid"], jsonData["ssid_pwd"]
    
    def getAPSettings(self):
        jsonData = self.__readJson(self.__AP_SETTINGS_JSON)
        return jsonData["ap_ssid"], jsonData["ap_pwd"]
    
    def getDataTemplateJson(self):
        data = self.__readJson(self.__TEMPLATE_JSON)
        return [ setting for setting in data if setting["fieldName"] != "" and  setting["fieldName"] != "labelText" ]

    def getOtherSettings(self):
        return self.__readJson(self.__OTHER_SETTINGS_JSON)

    def saveOtherSettings(self, settings: dict[str, str]) -> None:
        otherSettings: dict[str, str] = {}
        dataTemplateJson = self.getDataTemplateJson()
        for tmpltSetting in dataTemplateJson:
            keyName = tmpltSetting["fieldName"]
            otherSettings[keyName] = settings[keyName]
        with open(self.__OTHER_SETTINGS_JSON, 'w') as file:
             json.dump(otherSettings, file)

    def __readJson(self, path):
        with open(path, 'r') as file:
            return json.load(file)