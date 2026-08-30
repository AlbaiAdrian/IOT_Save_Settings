_MODULE_PATH = __file__.replace("\\", "/")
_PACKAGE_PATH = _MODULE_PATH.rsplit("/", 2)[0]

class FileReaderService():
    
    def getFileContent(self, path: str) -> str:
        with open(_PACKAGE_PATH + '/' + path, 'r') as file:
            file_content = file.read()
            return file_content