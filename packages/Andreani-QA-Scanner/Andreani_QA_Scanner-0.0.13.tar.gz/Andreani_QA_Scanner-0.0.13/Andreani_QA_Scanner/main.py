import threading
import time
import os
from views.Landing import Landing, Api
from views.Launcher import Launcher
from services.Listener import Listener
import ctypes

class Main:
    def __init__(self):
        port = 30505
        api_landing = Api()
        api_landing._port_api = port
        if str(Launcher()) == "True":
            listener = threading.Thread(target=Listener, args=(port, api_landing,))
            listener.start()
            Landing(api_landing, debug=False)
            thread_id = listener.ident
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print("Error: No se pudo detener el thread.")
            listener.join()

    @staticmethod
    def validar_puerto():
        port = 30505
        cmd = f"netstat -aon | findstr :{port}"
        output = os.popen(cmd)
        output_read = output.read()
        output.close()
        if output_read:
            lines = output_read.split('\n')
            for line in lines:
                if f":{port}" in line:
                    pid = int(line.strip().split()[-1])
                    if pid:
                        print(f"El proceso que está utilizando el puerto {port} es {pid}")
                        os.system(f"taskkill /F /PID {pid}")
                    else:
                        print(f"El puerto {port} está en uso pero no se pudo determinar el proceso asociado.")
                    return
            print(f"No se encontró ningún proceso utilizando el puerto {port}.")
        else:
            print(f"El puerto {port} no está en uso.")


if __name__ == '__main__':
    Main()
