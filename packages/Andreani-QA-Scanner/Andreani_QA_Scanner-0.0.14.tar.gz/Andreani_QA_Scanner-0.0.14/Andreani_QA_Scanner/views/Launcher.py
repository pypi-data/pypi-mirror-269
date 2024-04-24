# -*- coding: utf-8 -*-
import sys
import os
import time

import webview
from app.ScreenManagement import Screen as MyScreen
from app.Downloader import Downloader as MyDownloader

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
            data_css = data_css.replace("$zoomValue$", str(MyScreen.get_scale()))
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


class Launcher:
    def __init__(self, debug=False) -> None:
        Launcher.is_validator = None
        Launcher.debug = debug
        Launcher.screen = MyScreen()  # Crea un objeto a partir de la resolucion que este utilizando el usuario.
        Launcher.api = Api()
        anchor = Launcher.screen.get_anchor("center", dimensions=(400, 300))  # Configura la ubicacion de la aplicación en el escritorio.
        Launcher.pages = Launcher.build_pages() # Crea y gestiona las distintas vistas.
        Launcher.window = webview.create_window(f'Pybot Scanner 1.0 ',
                                                html=Launcher.pages["LAUNCHER"], js_api=Launcher.api,
                                                height=300,
                                                width=400,
                                                x=anchor[0], y=anchor[1],
                                                resizable=True,
                                                frameless=True,
                                                transparent=True,
                                                easy_drag=False,
                                                on_top=True) # crea la ventana
        Launcher.api.set_window(Launcher.window)  # Relaciona la ventana con su api
        Launcher.window.events.shown += lambda self=self: Launcher.on_shown(self)
        webview.start(debug=debug)

    def on_shown(self):
        Launcher.is_validator = MyDownloader(api=Launcher.api).main()
        if Launcher.is_validator is False:
            Launcher.api.callback_refresh_message("Ah ocurrido un error.")
            time.sleep(3)
        Launcher.window.destroy()

    def __repr__(self):
        return str(Launcher.is_validator)

    @classmethod
    def build_pages(cls):
        """
            :return: Devuelve un diccionario con cada una de las vistas configuradas.
        """
        pages = {'LAUNCHER': Launcher.get_launcher()
                 }
        return pages

    @classmethod
    def get_launcher(cls):
        """
            :return: Devuelve el codigo html, css y js para su despliegue de la vista home en la ventana.
        """
        styles = load_css("./src/style/customazer.css", "customazer.css")
        scripts = f'{load_js("./src/index.js", "index.js")} {load_js("./src/js/updateLauncher.js", "updateLauncher.js")}'
        launcher = f"""
                    {STYLES_MATERIALIZE}
                    {styles}
                    {load_html(f"./src/templates/Launcher.html", "Launcher.html")}
                    {SCRIPTS_MATERIALIZE}
                    {scripts}
                    """
        return launcher

class Api:
    code = 1  # status 2: exit

    def __init__(self):
        """
            Constructor de la clase Api que maneja funciona de interfaz entre la vista y las funciones.
        """
        Api.element_cache = None
        Api._inspector_activated = None
        Api._port_api = None
        Api._window = None
        Api._pages = None
        Api._screen = None

    def callback_start_loader(self, id_element, color="red"):
        Api._window.evaluate_js(f"startLoader('{id_element}', '{color}');")

    def callback_refresh_message(self, message):
        """
            :param message: string con el mensaje que se requiere mostrar en el footer.
            :return: Actualiza la barra de envetos en el footer.
        """
        Api._window.evaluate_js(f"refreshMessage('{message}')")

    def set_window(self, window):
        """
            :return: Configura una variable de la api para que obtener todas las funciones de una ventana especifica.
        """
        Api._window = window

    def set_screen(self, screen):
        """
            :return: Configura una variable de la api para obtener el objeto screen y ajustar el tamaño del contenido.
        """
        Api._screen = screen

    def set_pages(self, pages):
        """
            :return: Carga la variable pages con el diccionario que almacena todas las vistas.
        """
        Api._pages = pages

    def get_code(self):
        """
            :return: Obtiene el valor de la variable code.
        """
        return Api.code


if __name__ == '__main__':
    Launcher(False)