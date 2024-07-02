from flask import Flask, jsonify, request
import stomp

app = Flask(__name__)

class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print('received an error "%s"' % frame.body)
    def on_message(self, frame):
        print('received a message "%s"' % frame.body)

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', MyListener())
conn.connect('admin', 'admin', wait=True)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()

    expected_from = "incidente@vbbc.com.pe"
    expected_tipo = "MAIL"
    required_keys = ["body", "from", "sendto", "subject", "tipo"]
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing required keys in JSON"}), 400
    if data['from'] != expected_from or data['tipo'] != expected_tipo:
        return jsonify({"error": f"Invalid value for 'from' or 'tipo'. Expected 'from': {expected_from}, 'tipo': {expected_tipo}"}), 400
    conn.send(body=str(data), destination='/queue/test')

    response = {
        "data": data
    }
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(debug=True)
    conn.disconnect()
