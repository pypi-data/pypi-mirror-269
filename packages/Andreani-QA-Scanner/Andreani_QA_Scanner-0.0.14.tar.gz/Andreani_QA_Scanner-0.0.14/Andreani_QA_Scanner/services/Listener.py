from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio

class Listener:

    def __init__(self, port=8080, api=None):
        self.app = Flask(__name__)
        self.port = port
        self.api = api
        self.route_config()
        CORS(self.app)
        self.run()

    def route_config(self):
        """
        Description: configura todas las rutas y endpoints para la comunicación local entre los navegadores y la app.
        """
        @self.app.route('/api/events', methods=['POST'])
        def post_event():
            """
            Description: configura el endpoint http://Localhost:{self.port} para el logeo de los eventos.
            return: response a la api.
            """
            data = request.get_json()
            event = data['event']
            target = data['target']
            value = data['value']
            frame = data['frame']
            result = f"Evento: {event} en objeto: {target} con valor {value} dentro del frame {frame}."
            self.send_event(data)
            return jsonify({'resultado': result})

    def send_event(self, data):
        asyncio.run(self.api._scanner.event_recorder_handler(data))

    def run(self):
        """
        :return: Inicializa los servicios api rest que utiliza la consola del webdriver para comunicarse con la app.
        """
        self.app.run(port=30505)


if __name__ == '__main__':
    Listener().run()


