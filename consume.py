import time
from ActiveMQFactory import ActiveMQFactory
from flask import Flask, jsonify
app = Flask(__name__)


active_mq_factory = ActiveMQFactory(
    host='localhost',
    port=61613,
    username='admin',
    password='admin',
    destination='/queue/test_object'
)

@app.route('/get_messages', methods=['GET'])
def get_messages():
    active_mq_factory.connect()
    time.sleep(1)
    messages = active_mq_factory.get_messages()
    
    active_mq_factory.disconnect()
    print(messages)
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True, port=5000)