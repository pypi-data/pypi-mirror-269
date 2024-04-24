# -*- coding: utf-8 -*-
from pprint import pprint
import random
import json
import time
import datetime
import codecs
import os
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, StaleElementReferenceException, NoSuchElementException, \
    JavascriptException, WebDriverException, InvalidSessionIdException
from urllib3.exceptions import MaxRetryError
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
import asyncio
import pyperclip
from app.UserManagement import UserManagement
import tldextract
import base64
sys.path.append(os.path.abspath(os.path.join(__file__, "../")))
import threading

class Scanner:

    random_list = []
    objects_elements_cache = []
    objects_elements_on_iframe_cache = []
    iframes_elements_cache = []
    infractions_cache = []
    infractions_on_iframe_cache = []
    port_api = None
    eventsRecordedList = []
    recorder_elements_order = 1
    state = None
    lock = threading.Lock()  # Crear un bloqueo

    def __init__(self):
        self.driver = None
        self._api = None

    def set_api(self, api):
        """
            :param api:
            :return:
        """
        self._api = api

    def get_url_domain(self, url):
        extracted = tldextract.extract(url)
        domain = extracted.domain
        return domain

    def open_browser(self, browser):
        """
            :return: Activa el webdriver dejandolo disponible en memoria y abre el navegador.
        """
        end = False
        url = "about:blank"
        domain = ''
        asyncio.run(self.event_recorder_handler({"event": "open browser",
                                     "target": browser,
                                     "value": browser,
                                     "frame": None}))
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

        if browser == "Edge":
            options = EdgeOptions()
            service = EdgeService()

        if browser == "Chrome":
            options = ChromeOptions()
            service = ChromeService()
            options.binary_location = './Browsers/chrome-win/chrome.exe'

        options.add_argument("--start-maximized")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--profile-directory=Temporal")
        options.add_argument("--enable-automation")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--verbose")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--disable-cookies")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("user-data-dir=C:\\path\\to\\edge-profile")
        options.add_argument(f"--remote-debugging-port=37209")
        extension_path = os.path.join(os.getcwd(), "app\\extension")
        options.add_argument(f"--load-extension={extension_path}")
        if browser == "Edge":
            self.driver = webdriver.Edge(options=options)
        if browser == "Chrome":
            self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(0)
        try:
            self.driver.get(url)
        except NoSuchWindowException:
            self._api.callback_refresh_message("Se ha cerrado el navegador.")
            end = True
        while end is False:
            time.sleep(1)
            try:
                if self.driver.current_url not in ("data:,", "about:blank", url):
                    url = self.driver.current_url
                    url_domain = self.get_url_domain(url)
                    if domain != url_domain:
                        domain = url_domain
                        asyncio.run(self.event_recorder_handler({"event": "url log",
                                                     "target": url,
                                                     "value": url,
                                                     "frame": None}))
                        self._api.callback_refresh_message(f"Ingresando a {self.driver.current_url}")
            except WebDriverException:
                self._api.callback_refresh_message("Se ha cerrado el navegador.")
                self.driver = None
                end = True

            except NoSuchWindowException:
                self._api.callback_refresh_message("Se ha cerrado el navegador.")
                self.driver = None
                end = True

            except (InvalidSessionIdException, MaxRetryError, AttributeError):
                self.driver = None
                end = True

    def compare_events_and_ignore_key(self, dicc1, dicc2, key_to_ignore):
        """
            Description:
                Compara dos diccionarios ignorando una clave específica.

            :param dicc1:
                El primer diccionario para la comparación.
            :param dicc2:
                El segundo diccionario para la comparación.
            :param key_to_ignore:
                La clave que se debe ignorar durante la comparación.

            :return:
                True si los diccionarios son iguales después de ignorar la clave especificada, False en caso contrario.
            """
        dicc1_copy = dict(dicc1)
        dicc2_copy = dict(dicc2)
        dicc1_copy.pop(key_to_ignore, None)
        dicc2_copy.pop(key_to_ignore, None)
        return dicc1_copy == dicc2_copy

    async def event_recorder_handler(self, event_recorded):
        """
            Description:
                Agrega un evento a la lista de acciones grabadas. siempre y cuando no sea un
                loggueo de usuario ingresando texto en un input, evitando duplicados basándose
                en la comparación del último elemento presente en la lista.

            :param event_recorded:
                Evento capturado.
        """
        if event_recorded['event'] == 'log user input':
            self.event_logger_message(event_recorded)

        elif event_recorded['event'] == 'reset recorder steps':
            self.eventsRecordedList = []
            self.recorder_elements_order = 1
            self._api.add_recorder_list(self.eventsRecordedList)

        elif event_recorded['event'] == 'delete card step':
            self.eventsRecordedList.pop(event_recorded['value'])
            for event_listed in self.eventsRecordedList:
                if event_listed["order"] > event_recorded['value']:
                    event_listed["order"] -= 1
            self.recorder_elements_order -= 1
            self._api.add_recorder_list(self.eventsRecordedList)
            self.event_logger_message(event_recorded)

        else:
            if not self.eventsRecordedList or not self.compare_events_and_ignore_key(self.eventsRecordedList[-1], event_recorded, 'order'):
                #event_recorded['order'] = len(self.eventsRecordedList) + 1 #self.recorder_elements_order
                with self.lock:  # Adquirir el bloqueo antes de modificar la lista
                    if self.driver is not None:
                        event_recorded['screenshot'] = base64.b64encode(self.driver.get_screenshot_as_png()).decode('utf-8')
                    event_recorded['order'] = len(self.eventsRecordedList) + 1  # self.recorder_elements_order
                    self.eventsRecordedList.append(event_recorded)
                    self.event_logger_message(event_recorded)
                    self.recorder_elements_order += 1
                    self._api.add_recorder_list(self.eventsRecordedList)



    def event_logger_message(self, event):
        if event['event'] == 'open browser':
            self._api.callback_refresh_message(f"Se inicio el navegador {event['value']} - Paso número {event['order']}")
        if event['event'] == 'url log':
            self._api.callback_refresh_message(f"Se carga la web {event['value']} - Paso número {event['order']}")
        if event['event'] == 'click':
            self._api.callback_refresh_message(f"Se realizó click - Paso número {event['order']}")
        if event['event'] == 'input':
            self._api.callback_refresh_message(f"Se ha escrito el valor {event['value']}- Paso número {event['order']}")
        if event['event'] == 'send_key':
            self._api.callback_refresh_message(f"Se ha presionado la tecla {event['value']}- Paso número {event['order']}")
        if event['event'] == 'screenshot':
            self._api.callback_refresh_message(f"Se realiza captura de pantalla - Paso número {event['order']}")

    def get_elements_cache(self):
        """
            :return: devuelve el cache de elementos capturados.
        """
        return self.objects_elements_cache

    def injections_scripts(self, scripts: str):
        """
            :param: nombre del archivo de script que se desea inyectar.
            :return: Inyecta archivos js en la memoria del navegador.
        """
        scripts = self.load_js(scripts)
        try:
            self.driver.execute_script(scripts)

        except StaleElementReferenceException:
            self.injections_scripts(scripts)

        except NoSuchElementException:
            pass

        except (NoSuchWindowException, AttributeError):
            self._api.callback_refresh_message("No es posible realizar el escaneo ya que no se encuentra un navegador abierto.")

    @staticmethod
    def normalizer_translation(string):
        string = str(codecs.escape_decode(string.encode("utf-8"))[0].decode("utf-8"))
        return string
    
    def transcribe_infraction(self, list_infractions):
        with open(r"./app/src/InfractionTranslation.json", 'r', encoding="utf-8") as file:
            translations = json.load(file)
        for infraction in list_infractions:
            for translation in translations:
                if infraction["ID"].lower() == translation['key'].lower():
                    infraction["MORE_INFO"] = translation['description']
    async def execute_functions(self):
        """
            :return: Realiza las acciones de scaneo "busqueda de objetos" y "busqueda de errores de accesibilidad.
        """

        asyncio.create_task(self.scan_objects_page())
        asyncio.create_task(self.scan_infractions_page())
 
    async def scan_objects_page(self):
        """
            :return: Ejecuta las funciones de busqueda y captura de elementos web y retorna una lista de objetos que
            contienen la informacion de los elementos y sus localizadores.
        """
        self.objects_elements_cache = []
        if self.driver is None:
            self._api.callback_refresh_message( "No es posible realizar el escaneo ya que no se encuentra un navegador abierto.")
        else:
            try:
                self._api.callback_start_loader("containerObjectLoader", "green")
                self.driver.execute_script("document.dispatchEvent(new Event('runScann'), '*');")
                time.sleep(1)
                self.objects_elements_cache = self.driver.execute_script("return localStorage.getItem('myElementsCache')")
            except WebDriverException:
                self._api.callback_refresh_message("No es posible realizar el escaneo en esta web.")
            if self.objects_elements_cache:
                self.objects_elements_cache = json.loads(self.objects_elements_cache)
                for object_element in self.objects_elements_cache:
                    object_element['NAME'] = self.generate_random_name(object_element["TAGNAME"])
                    object_element['XPATH'] = object_element["XPATH"]
        self._api.add_objects(self.objects_elements_cache)

    async def scan_infractions_page(self):
        """
            :return: Ejecuta las funciones de busqueda y captura de elementos web y retorna una lista de objetos que
            contienen la informacion de los elementos y sus localizadores.
        """
        self.infractions_cache = []
        if self.driver is None:
            self._api.callback_refresh_message( "No es posible realizar el escaneo ya que no se encuentra un navegador abierto.")
        else:
            try:
                self._api.callback_start_loader("containerInfractionLoader", "red")
                self.driver.execute_script("document.dispatchEvent(new Event('runAxe'), '*');")
                time.sleep(1)
                self.infractions_cache = self.driver.execute_script("return localStorage.getItem('MyInfractionsCache')")
            except WebDriverException:
                self._api.callback_refresh_message("No es posible realizar el escaneo en esta web.")
            if self.infractions_cache:
                self.infractions_cache = json.loads(self.infractions_cache)
                self.transcribe_infraction(self.infractions_cache)
                self._api.add_infractions(self.infractions_cache)

    def load_object(self, new_element, frame):
        find_element = False
        new_element['NAME'] = self.generate_random_name(new_element["TAGNAME"])
        new_element['XPATH'] = self.normalizer_xpath(new_element['XPATH'])
        new_element['FRAME'] = self.normalizer_xpath(frame)
        for element in self.objects_elements_cache:
            if element['XPATH'] == new_element['XPATH']:
                new_element['NAME'] = element['NAME']
                find_element = True
                self.objects_elements_cache.remove(element)
                self.objects_elements_cache.insert(0, element)
                break
        if find_element is False:
            self.objects_elements_cache.extend([new_element])
            element = self.objects_elements_cache.pop()
            self.objects_elements_cache.insert(0, element)
        return self.objects_elements_cache

    def update_element(self, name, xpath):
        def search_element(target, name, xpath):
            if target["NAME"] == name:
                target["XPATH"] = xpath
            if "RELATED" in target.items():
                search_element(target["RELATED"])

        for object_element in self.objects_elements_cache:
            search_element(object_element,name, xpath)
        self._api.add_objects(self.objects_elements_cache)

    @staticmethod
    def load_js(file):
        """
            :return: Devuelve variable con funciones js.
        """
        with open(f"app/{file}.js", 'r') as file:
            content = file.read()
        return content

    def save_to_file(self, list_element):
        """
            :return: Guarda los objetos contenidos en cache dentro de un archivo json con formato pybot.
        """
        with open('mi_archivo.json', 'w') as archivo:
            json.dump(self.normalizer_list_to_json(list_element), archivo, ensure_ascii=False, indent=4)
            self._api.callback_refresh_message("Guardando archivo: nombre_archivo.json.")

    def copy_element_object(self, name):
        resultado = list(filter(lambda d: d.get("NAME") == name, self.objects_elements_cache))
        pyperclip.copy(str(self.normalizer_list_to_json(resultado)))

    def normalizer_list_to_json(self, list_element: list):
        """
            :return: Relealiza el armado del archivo json con formato pybot.
        """
        json_data = {}
        for object_element in list_element:
            json_data[object_element['NAME']] = {"GetFieldBy": "Xpath",
                                                "ValueToFind": f"{object_element['XPATH']}",
                                                "Quality": f"{object_element['QUALITY']}"}
        return json_data

    def screenshot_infraction(self, infraction_key):
        """
            :return: Realiza una captura indicando los errores detectados.
        """
        self.highlight_infractions(infraction_key)
        folder_screenshots = UserManagement.get_path("screenshots")
        screenshot_path = f'{folder_screenshots}/PNG_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        self.driver.save_screenshot(screenshot_path)

    def generate_random_name(self, tagname):
        """
            :return: Genera una nombre de objeto random utilizando un id de 10 digitos.
        """
        random_name = tagname
        random_id = random.randint(1000000000, 9999999999)
        while True:
            if random_id in self.random_list:
                random_id = random.randint(1000000000, 9999999999)
            else:
                break
        return random_name + f"_{str(random_id)}"

    def execute_highlight(self, objects_elements, type_locator= "XPATH"):
        """
            :param  objects_elements: Lista de objetos que contienen la informacion de los elementos y sus localizadores.
                    type_locator: Tipo de identificador "XPATH" o "CSS".
            :return: Llama a la funcion 'highlight' inyectada por el webdriver para señalar los objetos en la web.
        """
        errors = []
        self.state = "highlight"
        self.injections_scripts("Highlight")
        self.driver.switch_to.parent_frame()
        count_element = len(objects_elements)
        for object_element in objects_elements:
            if object_element["FRAME"] != "ROOT":
                frame_element = self.driver.find_element(By.XPATH, object_element["FRAME"])
                self.driver.switch_to.frame(frame_element)
                self.injections_scripts("Highlight")
            if type_locator == "XPATH":
                if count_element == 1:
                    control = self.driver.execute_script(f"return highlight('{object_element['XPATH']}', 'XPATH', true);")
                else:
                    control = self.driver.execute_script(f"return highlight('{object_element['XPATH']}', 'XPATH', false);")
            elif type_locator == "CSS":
                for querySelect in object_element['TARGET']:
                    control = self.driver.execute_script(f"return highlight('{querySelect}', 'CSS', false);")
            else:
                self._api.callback_refresh_message("No se reconoce el tipo de localizador utilizado.")
            if control is False:
                errors.append(objects_elements)
            self.driver.switch_to.parent_frame()
        self.state = None
        return errors

    def highlight_infractions(self, infraction_key):
        for infraction in self.infractions_cache:
            if infraction_key == infraction['ID']:
                self.execute_highlight([infraction], "CSS")

    async def inspector_mode(self, activated, recorder_mode = False):
        if self.driver.execute_script("return window.myScanner;") is None:
            await asyncio.create_task(self.scan_objects_page())
        if self.driver.execute_script("return window.myScripts;") is None:
            self.injections_scripts("Utils")
            self.injections_scripts("Inspector")
            self.injections_scripts("Recorder")
        if activated:
            if recorder_mode:
                self.scanner_mode = 'recorder'
                self.driver.execute_script(f"setScannerModeAndLaunch('{self.scanner_mode}')")
            else:
                self.scanner_mode = 'inspector'
                self.driver.execute_script(f"setScannerModeAndLaunch('{self.scanner_mode}')")
        else:
            self.driver.execute_script("activateLocationModeOff()")

        if self.get_iframes_on_page():
            for iframe in self.get_iframes_on_page():
                iframe_element = self.driver.find_element(By.XPATH, iframe["XPATH"])
                self.driver.switch_to.frame(iframe_element)
                if self.driver.execute_script("return window.myScripts;") is None:
                    self.injections_scripts("Utils")
                    self.injections_scripts("Inspector")
                    self.injections_scripts("Recorder")
                    self.driver.execute_script(f"window.myScripts['FRAME'] ='{str(iframe['XPATH'])}';")
                if activated:
                    if recorder_mode:
                        self.scanner_mode = 'recorder'
                        self.driver.execute_script(f"setScannerModeAndLaunch('{self.scanner_mode}')")
                    else: 
                        self.scanner_mode = 'inspector'
                        self.driver.execute_script(f"setScannerModeAndLaunch('{self.scanner_mode}')")
                else:
                    self.driver.execute_script("activateLocationModeOff()")
                self.driver.switch_to.parent_frame()
            self.driver.switch_to.parent_frame()

    def normalizer_xpath(self, xpath):
        """
            :param xpath: Xpath obtenido segun el estandar de javascript.
            :return: Retorna un xpath normalizado.
        """
        xpath = str(xpath).replace("'",'"')
        return xpath

    def get_elemets_clicked_list(self):
        return self.eventsRecordedList

    def capture_screen(self):
        self.driver.execute_script("call_screenshot_event()")

    def delete_step_card(self, step_index):
        self.driver.execute_script(f"call_delete_card_step({step_index})")

    def reorder_cards(self, reorderEventsRecordedList):
        self.eventsRecordedList = reorderEventsRecordedList
    
    def reset_recorder_steps(self):
        self.driver.execute_script("call_reset_recorder_steps()")

    #def execute_monkey_test(self):
        #self.driver.execute_script(f"monkeyTest();")

    def execute_monkey_test(self):
        self.state = "monkeytest"
        self.injections_scripts("Monkey")
        self.driver.switch_to.parent_frame()
        self.driver.execute_script("return monkeyTest();")
        time.sleep(10)
        self.states = None


if __name__=="__main__":
    Scanner().main()