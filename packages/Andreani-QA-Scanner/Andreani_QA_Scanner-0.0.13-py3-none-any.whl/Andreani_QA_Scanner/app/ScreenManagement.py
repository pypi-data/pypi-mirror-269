import ctypes
from screeninfo import get_monitors

class Screen():

    def __init__(self):
        self.width = self.get_screen()[0]
        self.height = self.get_screen()[1]
        self.app_width = 0
        self.app_height = 0

    def get_screen(self):
        """
            :return: Obtiene el tamaño de la resolucion usada por el usuario.
        """
        main_screen = get_monitors()[0]
        width = main_screen.width
        height = main_screen.height
        zoom = Screen.detect_scale_factor() / 100
        height = (height / zoom) - (Screen.get_windows_bar_height() / zoom)
        return width, height

    @staticmethod
    def get_windows_bar_height():
        """
            :return: Obtiene el tamaño de la barra de windows usada por el usuario.
        """
        user32 = ctypes.windll.user32
        rect = ctypes.wintypes.RECT()
        hwnd = user32.FindWindowW("Shell_TrayWnd", None)
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        height = rect.bottom - rect.top
        return height

    @staticmethod
    def detect_scale_factor():
        """
            :return: Obtiene el valor del zoom configurado en el sistema del usuario.
        """
        zoom = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        return zoom
    @staticmethod
    def get_scale():
        scale = 1 - (Screen.detect_scale_factor() - 100) / 100
        return scale

    def set_size_windows(self, factor_x=1, factor_y=1, min_width=None, min_height=None):
        """
            :return: Configura los valores de alto y ancho de la aplicacion en funcion de la resolucion del usuario.
        """
        self.app_width = int(self.width * factor_x)
        self.app_height = int(self.height * factor_y)
        if self.app_width < min_width:
            self.app_width=min_width
    def get_anchor(self, position="center", point=None, dimensions=()):
        """
            :return: Obtiene el valor del punto de anclaje de la aplicacion.
        """
        zoom = Screen.detect_scale_factor()/100
        if position == "center":
            if dimensions != ():
                return (int((self.width - dimensions[0] * zoom) / 2),
                        int((self.height - dimensions[1] )/2))
            return float(self.width - self.app_width * zoom)/2
        if position == "left":
            return 0
        if position == "right":
            return int(self.width - self.app_width * zoom)

