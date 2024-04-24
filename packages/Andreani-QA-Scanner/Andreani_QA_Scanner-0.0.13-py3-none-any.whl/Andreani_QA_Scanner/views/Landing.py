# -*- coding: utf-8 -*-
import sys
import os
import webview
import json
from pprint import pprint
import app.Scanner as Functions
from app.ScreenManagement import Screen as MyScreen
import asyncio
from views.User import UserConfigs, ApiUser
from views.Reporter import Reporter
from app.ScriptToFile import ScriptToFile

#lista de ventanas en ejecución que permite trabajar con ellas de forma independiente
#CURRENT_SCREENS = []

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


class Landing:
    def __init__(self, api: object, debug=False) -> None:
        Landing.debug = debug
        Landing.screen = MyScreen()  # Crea un objeto a partir de la resolucion que este utilizando el usuario.
        Landing.screen.set_size_windows(0.2, 1, min_width=350)  # Configura el tamaño de la aplicación.
        anchor = Landing.screen.get_anchor("right")  # Configura la ubicacion de la aplicación en el escritorio.
        Landing.api = api# Crea los servicios que seran disponibilizados para consultarse desde la vista.
        Landing.api.set_screen(Landing.screen) # Carga el objeto screen sobre la Api.
        Landing.pages = Landing.build_pages() # Crea y gestiona las distintas vistas.
        Landing.window = webview.create_window(f'Pybot Scanner 1.0 ',
                                               html=Landing.pages["HOME"], js_api=Landing.api,
                                               height=Landing.screen.app_height,
                                               width=Landing.screen.app_width,
                                               #min_size=(350, Landing.screen.app_height),
                                               x=anchor, y=0,
                                               resizable=True,
                                               on_top=True) # crea la ventana
        Landing.api.set_window(Landing.window) # Relaciona la ventana con su api
        Landing.api.set_pages(Landing.pages) # Configura la page activa
        Landing.add_jira_window = UserConfigs.get_jira_window(self)
        webview.start(debug=debug)

    def on_closing(self):
        pass

    def on_shown(self, api):
        pass


    def destroy_window(self):
        try:
            webview.windows[1].destroy()
        except:
            print("error")
    @classmethod
    def build_pages(cls):
        """
            :return: Devuelve un diccionario con cada una de las vistas configuradas.
        """
        pages = {'HOME': Landing.get_home()
                 }
        return pages

    @classmethod
    def get_home(cls):
        """
            :return: Devuelve el codigo html, css y js para su despliegue de la vista home en la ventana.
        """
        styles = load_css("./src/style/customazer.css", "customazer.css")
        scripts = f'{load_js("./src/index.js", "index.js")} {load_js("./src/js/updateLanding.js", "updateLanding.js")}'
        home = f"""
                {STYLES_MATERIALIZE}
                {styles}
                {load_html(f"./src/templates/Landing.html", "Landing.html")}
                {SCRIPTS_MATERIALIZE}
                {scripts}
                """
        return home


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
        Api._scanner = Functions.Scanner()
        Api._scanner.set_api(self)

    def call_open_browser(self, browser):
        """
            :return: Inicializa el webdriver configurado bajo la resolucion y el zoom del usuario.
        """
        self.callback_refresh_message(f'Abriendo navegador {browser}')
        Api._scanner.port_api = Landing.api._port_api
        Api._scanner.open_browser(browser)

    def call_scan(self):
        """
            :return: Inyecta el scraper y obtiene los objetos.
        """
        asyncio.run(Api._scanner.execute_functions())

    def call_highlight(self, list_element):
        """
            :return: Ejecuta la funcion de señalar todos los elementos en cache.
        """
        errors = Api._scanner.execute_highlight(Api.normalizer_dict_list(list_element))
        if len(errors) != 0:
            self.callback_refresh_message(f"No se han podido señalar {len(errors)} elementos.")

    def call_copy_element(self,name):
        """
            :return: Ejecuta la funcion que permite copiar un elemento en formato pybot.
        """
        Api._scanner.copy_element_object(name)

    def call_update_element(self,name, xpath):
        """
            :return: actualiza el xpath de un elemento.
        """
        name = Api.normalizer(name)
        Api._scanner.update_element(name, xpath)

    def call_highlight_element(self, element_xpath, name):
        """
            :return: Ejecuta la funcion de señalar un Xpath.
        """
        for object_element in Api._scanner.get_elements_cache():
            if object_element['NAME'] == name:
                tem_object_element = {"NAME": object_element['NAME'],
                                      "XPATH": element_xpath,
                                      "FRAME": object_element['FRAME']}
                errors = Api._scanner.execute_highlight([tem_object_element])
                if len(errors) != 0:
                    self.callback_refresh_message(f"No se han podido señalar el elemento.")
                break

    def call_highlight_infraction(self, infraction_key):
        for infraction in Api._scanner.infractions_cache:
            if infraction_key == infraction['ID']:
                Api._scanner.execute_highlight([infraction], "CSS")

    def call_inspection_elements(self):
        if Api._inspector_activated is None or Api._inspector_activated is False:
            Api._inspector_activated = True
            asyncio.run(Api._scanner.inspector_mode(Api._inspector_activated))

        else:
            Api._inspector_activated = False
            asyncio.run(Api._scanner.inspector_mode(Api._inspector_activated))

    def call_load_object(self, element, xpath):
        cache_objects = Api._scanner.load_object(element, xpath)
        Api.add_objects(self, cache_objects)

    def call_report_infraction(self):
        Reporter()

    def callback_start_loader(self, id_element, color="red"):
        Api._window.evaluate_js(f"startLoader('{id_element}', '{color}');")

    def callback_refresh_message(self, message):
        """
            :param message: string con el mensaje que se requiere mostrar en el footer.
            :return: Actualiza la barra de envetos en el footer.
        """
        Api._window.evaluate_js(f"refreshMessage('{message}')")

    def callback_endLoader(self, loader):
        """
            :param loader: loader que se desea apagar en el front
            :return: apaga el loader en el front
        """
        if loader == "infraction":
            Api._window.evaluate_js(f"endLoader('containerInfractionLoader')")

    def call_open_jira_config_window(self):
        """
            :return: Obtiene el valor de la variable code.
        """
        is_exist = False
        for window in webview.windows:
            if "Pybot Scanner 1.0: User Configs" in window.title:
                window.hide()
                window.show()
                is_exist = True

        if is_exist is False:
            UserConfigs()

    def add_objects(self, cache_objects):
        if cache_objects:
            cache_objects = self.normalizer_json_list(cache_objects)
        cache_objects = json.dumps(cache_objects)
        Api._window.evaluate_js(f"addObjectRow({cache_objects});")

    def add_recorder_list(self, elementsClickedList):
        recorderList = json.dumps(elementsClickedList)
        Api._window.evaluate_js(f"updateRecorderActionList({recorderList});")

    def add_infractions(self, cache_infractions):
        if cache_infractions:
            cache_infractions = self.normalizer_json_list(cache_infractions, "infractions")
        cache_infractions = json.dumps(cache_infractions)
        Api._window.evaluate_js(f"addInfractionRow({cache_infractions});")

    @classmethod
    def normalizer(cls, entity, to="HTML"):
        """
            :return: Normaliza un string de un objeto que utilice los caracteres '<>' para que pueda ser presentado en una vista.
        """
        if to == "HTML":
            entity = entity.replace("&lt;", "<").replace("&gt;", ">")
        else:
            entity = entity.replace("<", "&lt;").replace(">", "&gt;")
        return entity

    @classmethod
    def normalizer_json_list(cls, list_web_objects, type_data="elements"):
        """
            :return: Normaliza un string de un objeto que utilice los caracteres '<>' y '"' para que pueda ser presentado en una vista.
        """
        normalize_list = []
        if type_data == "elements":
            for objectWeb in list_web_objects:
                normalize_list.append({ "FRAME": objectWeb["FRAME"],
                                        "TAGNAME": objectWeb["TAGNAME"],
                                        "QUALITY": objectWeb["QUALITY"],
                                        "XPATH": objectWeb["XPATH"].replace('"', '&quot;'),
                                        "NAME":  objectWeb["NAME"].replace("<", "&lt;").replace(">", "&gt;")})
        if type_data == "infractions":
            for infraction in list_web_objects:
                normalize_list.append({ "DESCRIPTION": infraction["DESCRIPTION"],
                                        "FRAME": infraction["FRAME"],
                                        "ID": infraction["ID"],
                                        "IMPACT": infraction["IMPACT"],
                                        "INFO_URL": infraction["INFO_URL"],
                                        "MORE_INFO": infraction["MORE_INFO"].replace("<", "&lt;").replace(">", "&gt;"),
                                        "TAGS":  infraction["TAGS"],
                                        "TAG_HTML": infraction["TAG_HTML"],
                                        "TARGET": infraction["TARGET"]})
        return normalize_list

    @classmethod
    def normalizer_dict_list(cls, list_web_objects_json):
        """
            :return: Normaliza un string de un objeto que utilice los caracteres '<>' y '"' para que pueda ser presentado en una vista.
        """
        normalize_list = []
        for objectWeb in list_web_objects_json:
            normalize_list.append({ "FRAME": objectWeb["FRAME"],
                                    "TAGNAME": objectWeb["TAGNAME"],
                                    "QUALITY": objectWeb["QUALITY"],
                                    "XPATH": objectWeb["XPATH"].replace('&quot;', '"'),
                                    "NAME":  objectWeb["NAME"].replace("&lt;", "<").replace("&gt;", ">")})
        return normalize_list

    def focus_landing_off(self):
        Api.get_windows_data(self)
        Api._window.hide()
        Api._window.show()
        Api._window.on_top = False

    def get_windows_data(self):
        print(f"Alto: {Landing.window.height}")
        print(f"Ancho: {Landing.window.width}")
        print(f"Punto x: {Api._window.x}")
        print(f"Punto y: {Api._window.y}")

    def focus_landing_on(self):
        Api.get_windows_data(self)
        Api._window.hide()
        Api._window.show()
        Api._window.on_top = True
        Api._window.hide()
        Api._window.show()

    def generate_script(self, file):
        step_by_step = Api._scanner.get_elemets_clicked_list()
        if not step_by_step == []:
            self.callback_refresh_message(ScriptToFile(steps_data=step_by_step).generate_file(file))
        else:
            self.callback_refresh_message("No se han registrado pasos realizados.")

    def call_save_to_file(self, list_element):
        """
            :return: Ejecuta la funcion de guardar los objetos en cache dentro de un archivo json.
        """
        objects_to_file = Api._scanner.normalizer_list_to_json(Api.normalizer_dict_list(list_element))
        if not objects_to_file == {}:
            self.callback_refresh_message(ScriptToFile(objects_data=objects_to_file).generate_object_file())
        else:
            self.callback_refresh_message("No se han registrado objetos capturados.")


    def capture_screen(self):
        Api._scanner.event_recorder_handler({"event": "screenshot",
                                            "target": "screenshot",
                                            "value": "Se realizo una captura de pantalla.",
                                            "frame": None})

    def delete_card_step(self, step_index):
        Api._scanner.delete_step_card(step_index)

    def reorder_card_index(self, reorderEventsRecordedList):
        Api._scanner.reorder_cards(reorderEventsRecordedList)

    def reset_recorder_steps(self):
        asyncio.run(Api._scanner.event_recorder_handler({'event': 'reset recorder steps'}))

    def delete_card_step(self, step_index):
        asyncio.run(Api._scanner.event_recorder_handler({
                                            "event": "delete card step",
                                            "target": "null",
                                            "value": step_index,
                                            "frame": None
                                            }))
    def call_execute_monkey_test(self):
        Api._scanner.execute_monkey_test()

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
    Landing(False)