# -*- coding: utf-8 -*-
import sys
import os
import webview
import app.Scanner as Functions
from app.ScreenManagement import Screen as MyScreen
from app.UserManagement import UserManagement
from views import Landing


def load_css(path, name=None):
    """
        :param path: ruta del archivo css que sera agregado a la vista.
        :param name: nombre del archivo css.
        :return: String con los estilos.
    """
    try:
        path = normalizer_path_by_pyinstaller(path)
        with open(path, "r") as f:
            data_css = f.read()
            data_css = data_css.replace("$zoomValue$", str(MyScreen.detect_scale_factor()))
        return rf"<STYLE>{data_css}</STYLE>"

    except FileNotFoundError:
        print(f"El archivo de estilos no se encontro en el directorio... {name if name is not None else ''}")
    except IOError:
        print("Ocurrió un error al leer el archivo de estilos.")

def load_js(path, name=None):
    """
        :param path: ruta del archivo js que sera agregado a la vista.
        :param name: nombre del archivo js.
        :return: String con las funciones.
    """
    try:
        path = normalizer_path_by_pyinstaller(path)
        with open(path, "r", encoding="utf-8") as f:
            data_js = f.read()
            return rf"<SCRIPT>{data_js}</SCRIPT>"
    except FileNotFoundError:
        print(f"El archivo de funciones no se encontro en el directorio... {name if name is not None else ''}")
    except IOError:
        print("Ocurrió un error al leer el archivo de funciones.")

def load_html(path, name=None):
    """
        :param path: ruta del archivo html temaplate que sera usado para el armado de la vista.
        :param name: nombre del archivo js.
        :return: String con las funciones.
    """
    try:
        path = normalizer_path_by_pyinstaller(path)
        with open(path, "r", encoding="utf-8") as f:
            data_html = f.read()
            return rf"<HTML>{data_html}</HTML>"
    except FileNotFoundError:
        print(f"No se encontro la plantilla html en el directorio... {name if name is not None else ''}")
    except IOError:
        print("Ocurrió un error al leer la plantilla html.")

def normalizer_path_by_pyinstaller(relative_path):
    """
    :param relative_path: string que contiene los recursos a cargarse en la aplicacion.
    :return: Devuelve una ruta que puede ser reconocida por la libreria pyinstaller.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

STYLES_MATERIALIZE = f'{load_css(r"./src/style/materialize.css")}'
SCRIPTS_MATERIALIZE = f'{load_js(r"./src/js/materialize.js")}'
ICON = normalizer_path_by_pyinstaller(r"./src/icon.png")

class UserConfigs:

    def __init__(self, debug=False) -> None:
        self.window = None
        UserConfigs.debug = debug
        UserConfigs.screen = MyScreen()  # Crea un objeto a partir de la resolucion que este utilizando el usuario.
        UserConfigs.screen.set_size_windows(0.2, 1)  # Configura el tamaño de la aplicación.
        anchor_x = UserConfigs.screen.get_anchor("center")  # Configura la ubicacion de la aplicación en el escritorio.
        UserConfigs.api_user = ApiUser() # Crea los servicios que seran disponibilizados para consultarse desde la vista.
        UserConfigs.api_user.set_screen(UserConfigs.screen) # Carga el objeto screen sobre la Api.
        UserConfigs.pages = UserConfigs.build_pages() # Crea y gestiona las distintas vistas.
        UserConfigs.window = webview.create_window(f'Pybot Scanner 1.0: User Configs',
                                                   html=UserConfigs.pages["JIRA"], js_api=UserConfigs.api_user,
                                                   height=500,
                                                   width=650,
                                                   x=anchor_x, y=200,
                                                   resizable=True) # crea la ventana con on_top la ventana siempre
                                                                   # estará en primer plano
        UserConfigs.set_user_window(self, UserConfigs.window)
        UserConfigs.api_user.set_window(UserConfigs.window) # Relaciona la ventana con su api
        ApiUser.autofill_user_data(self)

        #Landing.CURRENT_SCREENS.append(UserConfigs.window)

    def destroy_window(self):
        #for objeto in UserConfigs.CURRENT_SCREENS:
           #print(objeto)
        Landing.Landing.destroy_window(self)
        print("acá va el destroy")


    def set_user_window(self, window):
        self.window = window

    def get_jira_window(self):
        return self.window
    @classmethod
    def build_pages(cls):
        """
            :return: Devuelve un diccionario con cada una de las vistas configuradas.
        """
        pages = {'JIRA': UserConfigs.get_jira_home_page()
                 }
        return pages

    @classmethod
    def get_jira_home_page(cls):
        """
            :return: Devuelve el codigo html, css y js para su despliegue de la vista home en la ventana.
        """
        styles = load_css("src/style/customazer.css", "customazer.css")
        scripts = load_js("./src/js/updateUser.js", "updateUser.js")
        jira_home = f"""
                {STYLES_MATERIALIZE}
                {styles}
                {load_html(f"./src/templates/JiraUserConfigs.html", "JiraUserConfigs.html")}
                {SCRIPTS_MATERIALIZE}
                {scripts}
                """
        if UserConfigs.debug is True:
            print(jira_home)
        return jira_home

class ApiUser():
    _data_file = None
    code = 1  # status 2: exitUserConfigs

    def __init__(self):
        """
            Constructor de la clase Api que maneja funciona de interfaz entre la vista y las funciones.
        """
        ApiUser.cancel_heavy_stuff_flag = False
        ApiUser._window = None
        ApiUser._pages = None
        ApiUser.element_cache = None
        ApiUser._screen = None
        ApiUser._user_management = UserManagement()
        ApiUser._data_file = ApiUser._user_management.read_xml_file()

    def set_window(self, window):
        """
            :return: Configura una variable de la api para que obtener todas las funciones de una ventana especifica.
        """
        ApiUser._window = window

    def get_window(self):
        """
            :return: Configura una variable de la api para que obtener todas las funciones de una ventana especifica.
        """
        return ApiUser._window

    def set_screen(self, screen):
        """
            :return: Configura una variable de la api para obtener el objeto screen y ajustar el tamaño del contenido.
        """
        ApiUser._screen = screen

    def set_pages(self, pages):
        """
            :return: Carga la variable pages con el diccionario que almacena todas las vistas.
        """
        ApiUser._pages = pages

    def get_code(self):
        """
            :return: Obtiene el valor de la variable code.
        """
        return ApiUser.code

    def call_open_jira_config_window(self):
        """
            Esta función se encarga de la apertura de la nueva ventana utilizada para cargar
            los datos de conexión con Jira.
        """
        #call flag disabled
        UserConfigs.UserConfigs(debug=False)

    def call_check_and_save(self, jiraId, jiraServer, jiraToken):
        """
            :return: Obtiene el valor de la variable code.
        """
        ApiUser._user_management.check_and_save(jiraId, jiraServer, jiraToken)

    def call_exit_jira_configs(self):
        """
            :return: Obtiene el valor de la variable code.
        """
        ApiUser._window.hide()

    def call_open_jira_config_folder(self):
        ApiUser._user_management.open_config_folder()

    #funciones lógicas para los procesos
    def autofill_user_data(self):
        ApiUser._window.evaluate_js(f"autofill({ApiUser._data_file});")



if __name__ == '__main__':
    UserConfigs(False)