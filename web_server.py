
import socket

from .services.file_reader_service import FileReaderService
from .services.json_settings_service import JsonSettingsService


class WebServer:
    HTML_HEADER_OK = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    HTML_HEADER_BAD = 'HTTP/1.0 400 Bad Request\r\nContent-type: text/html\r\n\r\n'

    def __init__(self, port: int, data_saved_callback, file_reader_service: FileReaderService, json_settings_service: JsonSettingsService) -> None:
        self.__port = port
        self.__addr = socket.getaddrinfo('0.0.0.0', self.__port)[0][-1]
        self.__data_saved_callback = data_saved_callback
        self.__socket: socket.socket
        self.__call_data_saved_callback = False
        self.__run_server = False

        self.__file_reader_service = file_reader_service
        self.__json_settings_service = json_settings_service


    def start(self) -> None:
        self.__socket = socket.socket()
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind(self.__addr)
        self.__socket.listen(1)
        self.__run_server = True

        print(f"Web server listen to port {self.__port}")

        while self.__run_server:
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
        self.__run_server = False

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

        if self.__call_data_saved_callback and self.__data_saved_callback is not None:
            self.__call_data_saved_callback = False
            self.__data_saved_callback()

    def __send_request(self, client, html_header: str, html_content: str) -> None:
        client.sendall(html_header)
        client.sendall(html_content)

    def __handle_get(self) -> str:
        # Get the main part of the page
        html_content: str = self.__file_reader_service.get_file_content('html/ap_credentials_request.html')

        # Write the SSID in the page if previously set
        ssid, _ = self.__json_settings_service.get_wifi_settings()
        html_content = html_content.replace("SSID_VALUE", ssid)

        settings_template_json = self.__json_settings_service.get_data_template_json()
        other_settings_json = self.__json_settings_service.get_other_settings()

        other_settings_html = ""

        if len(settings_template_json) > 0:
            other_settings_html = other_settings_html + self.__file_reader_service.get_file_content("html/dynamic_html/header.html")
            setting_section = self.__file_reader_service.get_file_content("html/dynamic_html/settings_section.html")
            for setting in settings_template_json:
                other_settings_html = other_settings_html + setting_section.replace("{label}", setting["labelText"]).replace("{setting_id}", setting["fieldName"]).replace("{setting_value}", other_settings_json.get(setting["fieldName"], ""))
        html_content = html_content.replace("REPLACE_ME_WITH_OTHER", other_settings_html)
        return html_content

    def __handle_post(self, request) -> str:
        """Handle the POST request and extract form data."""
        # Find the form data in the request (after the empty line)
        raw_form_data: str = request.split("\r\n\r\n")[1]
        form_data: dict[str, str] = dict(pair.split('=') for pair in raw_form_data.split('&'))

        # Extract values from the form data
        ssid = form_data.get('ssid', 'NA')
        ssid_pwd = form_data.get('ssid_pwd', 'NA')

        # Save the values to a file
        self.__json_settings_service.save_wifi_settings(ssid, ssid_pwd)
        self.__json_settings_service.save_other_settings(form_data)
        self.__call_data_saved_callback = True

        html_content: str = self.__file_reader_service.get_file_content('html/ap_credentials_response_ok.html')
        html_content = html_content.replace("{ssid}", ssid)

        return html_content
