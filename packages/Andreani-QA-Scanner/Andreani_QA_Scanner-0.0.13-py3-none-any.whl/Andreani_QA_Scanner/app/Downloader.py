import os
import time
import zipfile
import requests


class Downloader:

    def __init__(self,
                 url="https://download-chromium.appspot.com/dl/Win_x64?type=snapshots",
                 save_path="chromium_windows_x64.temp",
                 folder="Browsers",
                 api=None):
        self.chromium_url = url
        self.save_path = save_path
        self.folder = folder
        self.api = api

    def main(self):
        is_validator = False
        if not os.path.exists(self.folder):
            try:
                self.api.callback_refresh_message("Descargando paquetes.")
                self.download_chromium(self.chromium_url, self.save_path)
                self.api.callback_refresh_message("Descomprimiendo carpetas.")
                self.unzip_and_rename(self.save_path, self.folder)
                self.api.callback_refresh_message("Limpiando directorios.")
                self.delete_folder(self.save_path)
                self.api.callback_refresh_message("Iniciando...")
                is_validator = True
            #Se debe agregar el manejo de excepciones.
            finally:
                return is_validator

        else:
            return True

    @staticmethod
    def delete_folder(folder_path):
        os.remove(folder_path)

    @staticmethod
    def download_chromium(url, save_path):
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

    @staticmethod
    def unzip_and_rename(zip_file, destination_folder):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)


if __name__ == '__main__':
    Downloader().main()
