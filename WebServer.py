
from Services.JsonSettingsService import JsonSettingsService
from Services.FileReaderService import FileReaderService
import socket

class WebServer():
    HTML_HEADER_OK = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    HTML_HEADER_BAD ='HTTP/1.0 400 Bad Request\r\nContent-type: text/html\r\n\r\n'

    def __init__(self, port: int, dataSavedCallack, fileReaderService: FileReaderService, jsonSettingsService: JsonSettingsService) -> None:
        self.__port = port
        self.__addr = socket.getaddrinfo('0.0.0.0', self.__port)[0][-1]
        self.__dataSavedCallack = dataSavedCallack
        self.__socket: socket.socket
        self.__callDataSavedCallack = False
        self.__runServer = False

        self.__fileReaderService = fileReaderService
        self.__jsonSettingsService = jsonSettingsService

        
    def start(self) -> None:
        self.__socket = socket.socket()
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind(self.__addr)
        self.__socket.listen(1)
        self.__runServer = True

        print(f"Web server listen to port {self.__port}")
        
        while self.__runServer:
            try:
                client, addr = self.__socket.accept()
                print(f'Client: {client}')
                print(f'Addr: {addr}')
                print('----------------------------------------------')
                
                self.__handle_client(client)
            except OSError as err:
                client.close()
                print(f"Connection close due error {err}")
    
    def stop(self) -> None:
        print("Web server closed!")
        self.__socket.close()
        self.__runServer = False

    def __handle_client(self, client):
        """Serve the Wifi Credentials form or handle the form submission."""
        try:
            # Read the incoming request
            request: str = client.recv(1024).decode('utf-8')
            
            # Determine if it's a GET or POST request and handle accordingly
            #             
            if request.startswith('GET'):    
                html_content = self.__handle_get()
                self.__send_request(client, self.HTML_HEADER_OK, html_content)

            if request.startswith('POST'):
                html_content: str = self.__handle_post(request)
                self.__send_request(client, self.HTML_HEADER_OK, html_content)
            
        except OSError as err:
            self.__send_request(client, self.HTML_HEADER_BAD, '<h1>400 - Bad Request</h1>')
        finally:
            client.close()
        
        if self.__callDataSavedCallack and None != self.__dataSavedCallack:
            self.__callDataSavedCallack = False
            self.__dataSavedCallack()

    def __send_request(self, client, html_header: str, html_content: str) -> None:
        client.sendall(html_header)
        client.sendall(html_content)

    def __handle_get(self) -> str:
        # Get the main part of the page
        html_content: str = self.__fileReaderService.getFileContent('Html/APCredentialsRequest.html')
        
        # Write the SSID in the page if previously set
        ssid, _ = self.__jsonSettingsService.getWifiSettings()
        html_content = html_content.replace("SSID_VALUE", ssid)

        settingsTemplateJson = self.__jsonSettingsService.getDataTemplateJson()
        otherSettingsJson = self.__jsonSettingsService.getOtherSettings()

        otherSettingsHtml = ""

        if len(settingsTemplateJson) > 0:
            otherSettingsHtml = otherSettingsHtml + self.__fileReaderService.getFileContent("Html/DynamicHTML/Header.html")
            settingSection = self.__fileReaderService.getFileContent("Html/DynamicHTML/SettingsSection.html")
            for setting in settingsTemplateJson:
                otherSettingsHtml = otherSettingsHtml + settingSection.replace("{label}", setting["labelText"]).replace("{setting_id}", setting["fieldName"]).replace("{setting_value}", otherSettingsJson.get(setting["fieldName"], ""))
        html_content = html_content.replace("REPLACE_ME_WITH_OTHER", otherSettingsHtml)
        return html_content

    def __handle_post(self, request) -> str:
        """Handle the POST request and extract form data."""
        # Find the form data in the request (after the empty line)
        rawFormData: str = request.split("\r\n\r\n")[1]
        formData: dict[str, str] = dict(pair.split('=') for pair in rawFormData.split('&'))
        
        # Extract values from the form data
        ssid = formData.get('ssid', 'NA')
        ssid_pwd = formData.get('ssid_pwd', 'NA')
        
        # Save the values to a file
        self.__jsonSettingsService.saveWifiSettings(ssid, ssid_pwd)
        self.__jsonSettingsService.saveOtherSettings(formData)
        self.__callDataSavedCallack = True

        html_content: str = self.__fileReaderService.getFileContent('Html/APCredentialsResponseOK.html')
        html_content = html_content.replace("{ssid}", ssid)
        
        return html_content
