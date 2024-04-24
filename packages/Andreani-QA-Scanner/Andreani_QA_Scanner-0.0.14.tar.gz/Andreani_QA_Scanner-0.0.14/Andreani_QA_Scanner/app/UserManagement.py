#XML tools
import xml.etree.ElementTree as Et
import xml.dom.minidom
import os
from pathlib import Path
import socket
import subprocess

USER_PC = os.getlogin()
PATH_USER_FOLDER = Path(f"C:/Users/{USER_PC}/Pybot/")
PATH_SCREENSHOTS_FOLDER = Path(f"C:/Users/{USER_PC}/Pybot/screenshots")
PATH_CONFIG_FOLDER = Path(f"C:/Users/{USER_PC}/Pybot/config")
PATH_USER_CONFIG_FILE = Path(f"C:/Users/{USER_PC}/Pybot/config/user_data.xml")
HOST_NAME = socket.gethostname()


class UserManagement:

    def main(self):
        print(f"El archivo siempre podrá ser encontrado en: {PATH_USER_CONFIG_FILE}")
        if self.folder_exists() is True:
            #Si el archivo no existe lo creo con una plantilla tomando información base del usuario
            if self.file_exists() is False:
                print("Veo que no tienes tu archivo qa_user_data.xml, dejame crealo!")
                #creación del archivo
                self.create_user_file()
                print(f"El archivo se encuentra listo en la dirección -> {PATH_USER_CONFIG_FILE}")
                return False
            else:
                # Si el formato es el correcto da inicio el proceso de opciones dentro del menú
                if self.file_format_is_xml() is True:
                    print("Todo en condiciones de iniciar")
                    return True
                # Si el formato del archivo no es el correcto, termino el programa.
                else:
                    print("El formato del archivo no es correcto,\n"
                          "corrijalo y vuelva a intentarlo.\n"
                          "El formato esperado es .xml")
                    return False
        else:
            #si la carpeta no existe, la genero  y corro nuevamente el proceso
            os.mkdir(PATH_CONFIG_FOLDER)
            UserManagement.main(self)
    @staticmethod
    def get_path(folder_name: str):
        folder_path = None
        if folder_name.lower() == "root":
            folder_path = PATH_USER_FOLDER
        elif folder_name.lower() == "config":
            folder_path = PATH_CONFIG_FOLDER
        elif folder_name.lower() == "screenshots":
            folder_path = PATH_SCREENSHOTS_FOLDER
        else:
            print("No se encontro la carpeta")
        if UserManagement.folder_exists(folder_path) is False:
            Path(folder_path).mkdir(parents=True, exist_ok=True)
        return folder_path

    @staticmethod
    def folder_exists(folder: Path):
        return folder.exists()
    @staticmethod
    def file_exists(file: Path):
        return file.exists()

    def file_format_is_xml(self):
        file_format = ".xml"
        is_xml = False
        if self.file_path.suffix == file_format:
            is_xml = True
        return is_xml

    @staticmethod
    def get_xml_root():
        tree = Et.parse(PATH_USER_CONFIG_FILE)
        current_root = tree.getroot()
        return current_root, tree

    @staticmethod
    def create_user_file():
        xml_body = f'<?xml version="1.0" encoding="UTF-8" ?> ' \
                   f'<root>' \
                   f'<USER>' \
                   f'<JIRA-ID></JIRA-ID>' \
                   f'<JIRA-SERVER></JIRA-SERVER>' \
                   f'<JIRA-TOKEN></JIRA-TOKEN>' \
                   f'<PC-NAME>{HOST_NAME}</PC-NAME>' \
                   f'<PC-ID>{USER_PC}</PC-ID>' \
                   f'</USER>' \
                   f'</root>'
        # Analiza el contenido XML
        dom = xml.dom.minidom.parseString(xml_body)
        # Obtiene una versión formateada del XML
        xml_formateado = dom.toprettyxml()
        with open(PATH_USER_CONFIG_FILE, 'w') as output_file:
            output_file.write(xml_formateado)
        output_file.close()

    @staticmethod
    def read_xml_file():
        if UserManagement.folder_exists(PATH_CONFIG_FOLDER) is False:
            Path(PATH_CONFIG_FOLDER).mkdir(parents=True, exist_ok=True)
        if UserManagement.file_exists(PATH_USER_CONFIG_FILE) is False:
            UserManagement.create_user_file()
        xml_dict_data = {}
        read_xml_file, project_tree = UserManagement.get_xml_root()
        for element in read_xml_file.findall(f"./USER/"):
            xml_dict_data[element.tag] = element.text
        return xml_dict_data

    def check_and_save(self, jiraId, jiraServer, jiraToken):
        """
            :param jiraId: ID de usuario correspondiente a la plataforma de JIRA.
            :param jiraServer: Nombre o dirección del host al que se va a realizar la conexión.
            :param jiraToken: Token personal del usuario requerido par algunos procesos realizardos en JIRA.
        """
        if UserManagement.folder_exists(PATH_CONFIG_FOLDER) is False:
            Path(PATH_CONFIG_FOLDER).mkdir(parents=True, exist_ok=True)
        if UserManagement.file_exists(PATH_USER_CONFIG_FILE) is False:
            UserManagement.create_user_file()
        UserManagement.search_jid_on_xml_file(jiraId)
        UserManagement.search_jserver_on_xml_file(jiraServer)
        UserManagement.search_jtoken_on_xml_file(jiraToken)

    @staticmethod
    def search_jtoken_on_xml_file(new_jira_token):
        read_xml_file, project_tree = UserManagement.get_xml_root()
        for element in read_xml_file.findall(f"./USER/"):
            if element.tag == "JIRA-TOKEN":
                element.text = new_jira_token
        project_tree.write(PATH_USER_CONFIG_FILE)

    @staticmethod
    def search_jid_on_xml_file(new_jira_id):
        read_xml_file, project_tree = UserManagement.get_xml_root()
        for element in read_xml_file.findall(f"./USER/"):
            if element.tag == "JIRA-ID":
                element.text = new_jira_id
        project_tree.write(PATH_USER_CONFIG_FILE)

    @staticmethod
    def search_jserver_on_xml_file(new_jira_server_host):
        read_xml_file, project_tree = UserManagement.get_xml_root()
        for element in read_xml_file.findall(f"./USER/"):
            if element.tag == "JIRA-SERVER":
                element.text = new_jira_server_host
        project_tree.write(PATH_USER_CONFIG_FILE)

    @staticmethod
    def open_config_folder():
        """
            :return: Abre la carpeta donde se encuentra alojado el archivo que contiene la información del usuario
            para llevar a cabo una conexión.
        """
        subprocess.call(rf"explorer C:\Users\{USER_PC}\Pybot\config")

if __name__ == '__main__':
    instancia = UserManagement()
    instancia.main()