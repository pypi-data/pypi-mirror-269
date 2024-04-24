# -*- coding: utf-8 -*-
import sys
import os
import webview
from app.ScreenManagement import Screen as MyScreen

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

class Reporter:

    def __init__(self, debug=False) -> None:
        self.window = None
        Reporter.debug = debug
        Reporter.screen = MyScreen()  # Crea un objeto a partir de la resolucion que este utilizando el usuario.
        Reporter.screen.set_size_windows(0.6, 1)  # Configura el tamaño de la aplicación.
        anchor_x = Reporter.screen.get_anchor("center")  # Configura la ubicacion de la aplicación en el escritorio.
        Reporter.api_reporter = ApiReporter() # Crea los servicios que seran disponibilizados para consultarse desde la vista.
        Reporter.api_reporter.set_screen(Reporter.screen) # Carga el objeto screen sobre la Api.
        Reporter.pages = Reporter.build_pages() # Crea y gestiona las distintas vistas.
        Reporter.window = webview.create_window(f'Pybot Scanner 1.0: Report ',
                                                html=Reporter.pages["REPORTER"], js_api=Reporter.api_reporter,
                                                height= Reporter.screen.app_height,
                                                width= Reporter.screen.app_width,
                                                x=anchor_x, y=0,
                                                resizable=True) # crea la ventana
        Reporter.set_jira_window(self, Reporter.window) # setea la variable window para que sea leida desde el Landing
        Reporter.api_reporter.set_window(Reporter.window) # Relaciona la ventana con su api

    def set_jira_window(self, window):
        self.window = window

    def get_jira_window(self):
        return self.windowasdasd

    @classmethod
    def build_pages(cls):
        """
            :return: Devuelve un diccionario con cada una de las vistas configuradas.
        """
        pages = {'REPORTER': Reporter.get_jira_home_page()
                 }
        return pages

    @classmethod
    def get_jira_home_page(cls):
        """
            :return: Devuelve el codigo html, css y js para su despliegue de la vista home en la ventana.
        """
        styles = load_css("src/style/customazer.css", "customazer.css")
        scripts = f'{load_js("./src/index.js", "index.js")}'
        jira_home = f"""
                {STYLES_MATERIALIZE}
                {styles}
                {load_html(f"./src/templates/ReportDefects.html", "ReportDefects.html")}
                {SCRIPTS_MATERIALIZE}
                {scripts}
                """
        if Reporter.debug is True:
            print(jira_home)
        return jira_home

class ApiReporter():
    code = 1  # status 2: exitUserConfigs

    def __init__(self):
        """
            Constructor de la clase Api que maneja funciona de interfaz entre la vista y las funciones.
        """
        ApiReporter.cancel_heavy_stuff_flag = False
        ApiReporter._window = None
        ApiReporter._pages = None
        ApiReporter.element_cache = None
        ApiReporter._screen = None
        #piReporter._user_management = Functions.UserManagement()

    def set_window(self, window):
        """
            :return: Configura una variable de la api para que obtener todas las funciones de una ventana especifica.
        """
        ApiReporter._window = window

    def set_screen(self, screen):
        """
            :return: Configura una variable de la api para obtener el objeto screen y ajustar el tamaño del contenido.
        """
        ApiReporter._screen = screen

    def set_pages(self, pages):
        """
            :return: Carga la variable pages con el diccionario que almacena todas las vistas.
        """
        ApiReporter._pages = pages

    def get_code(self):
        """
            :return: Obtiene el valor de la variable code.
        """
        return ApiReporter.code

    def call_exit_reporter(self):
        """
            :return: Obtiene el valor de la variable code.
        """
        #UserConfigs.destroy_window(self)

if __name__ == '__main__':
    Reporter(False)