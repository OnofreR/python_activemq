import time
import json
import stomp

class MyListener(stomp.ConnectionListener):
     def on_error(self, message):
        print(f'Received an error: {message}')
        
     def on_message(self, message):
        print(f'Received a message: {message}')
        
     def on_connected(self, headers):
        print('Connected to ActiveMQ')
        
     def on_disconnected(self, headers):
        print('Disconnected from ActiveMQ')

def send_messages(obj, destination='/queue/test_object'):
    conn = stomp.Connection([('localhost', 61613)])
    conn.set_listener('', MyListener())
    conn.connect('admin', 'admin', wait=True)
    headers = {'content-type': 'application/json'}

    for i in range(3):
         message = json.dumps(obj)
         conn.send(
                body=message,
                destination=destination,
                headers=headers
            )
         print(f'Sent: {message}')
         time.sleep(1)

    conn.disconnect()

if __name__ == "__main__":
    obj = {'name': 'John Doe', 'age': 30, 'city': 'New York'}
    send_messages(obj=obj)
