class FileReaderService():
    
    def getFileContent(self, path: str) -> str:
        with open(path, 'r') as file:
            file_content = file.read()
            return file_content