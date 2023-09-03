import os


class FileManager():
    """ Класс для работы с файлами в системе """

    def create_folder(self, path: str):

        if not os.path.exists(path):
            os.mkdir(path)

    def delete_folder(self, path: str):

        if os.path.exists(path):
            os.rmdir(path)

    def start(self, path: str):

        self.create_folder(path)
        self.delete_folder(path)
