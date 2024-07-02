import stomp
import json

class ActiveMQListener(stomp.ConnectionListener):
    def __init__(self):
        self.messages = []

    def on_error(self, message):
        print(f'Received an error: {message}')

    def on_message(self, message):
        print(f'Received a message: {message}')
        try:
            id_, nombre, dni, url = message.body.split('|')
            self.messages.append({
                "ID": id_,
                "NOMBRE": nombre,
                "DNI": dni,
                "URL": url
            })
        except Exception as e:
            print(f"Error processing message: {e}")

class ActiveMQFactory:
    def __init__(self, host, port, username, password, destination):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.destination = destination
        self.listener = ActiveMQListener()
        self.conn = None

    def connect(self):
        self.conn = stomp.Connection([(self.host, self.port)])
        self.conn.set_listener('', self.listener)
        self.conn.connect(self.username, self.password, wait=True)
        self.conn.subscribe(destination=self.destination, id=1, ack='auto')
        print(f'Subscribed to {self.destination}')

    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.clear_messages()
            self.conn.disconnect()

    def get_messages(self):
        return self.listener.messages

    def clear_messages(self):
        self.listener.messages = []
