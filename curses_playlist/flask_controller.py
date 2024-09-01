import threading
from contextlib import contextmanager
from flask import Flask, jsonify, request
from werkzeug.serving import make_server


app = Flask(__name__)

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

# VLC control commands mapping
COMMANDS = {
    'pause': 'pause\n',
    'stop': 'stop\n',
    'next': 'next\n',
    'previous': 'prev\n'
}

import socket

def run_command(command):
    """
    Execute a VLC control command using Python sockets.
    """
    host = 'localhost'
    port = 44500
    command = command.strip()


    # Convert the command to the VLC remote control command
    if command in COMMANDS:
        vlc_command = COMMANDS[command]
    else:
        print(f"Invalid command, aborting remote control: {command}, available: {COMMANDS.keys()}")
        return

    # Create a socket connection to VLC's remote control interface
    try:
        with socket.create_connection((host, port)) as sock:
            sock.sendall(vlc_command.encode('utf-8'))
            print(f"Executed command: {command}")
    except ConnectionRefusedError:
        print("Failed to connect to VLC remote control interface. Make sure VLC is running with '--intf rc --rc-host localhost:12345'.")
    except Exception as e:
        print(f"Error executing command: {e}")

        
@app.route('/control', methods=['POST'])
def control_vlc():
    """
    Control VLC via Flask.
    Expects a JSON payload with a "command" key.
    """
    data = request.json
    command = data.get('command')

    print(f"received cmd request: {command}")

    if command not in COMMANDS:
        return jsonify({"error": "Invalid command"}), 400

    # Execute the corresponding VLC control command
    run_command(COMMANDS[command])
    return jsonify({"message": f"Executed command: {command}"}), 200

def run_flask_server():
    """
    Run the Flask server in a separate thread.
    """
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

@contextmanager
def flask_vlc_context():
    """
    Context manager that runs a Flask server to control VLC while active.
    """
    print("starting Flask server")
    server = ServerThread(app)
    server.start()

    try:
        yield  # Run the context block while Flask server is running
    finally:
        # Cleanup: stop Flask server and VLC
        print("Shutting down Flask server and VLC")
        server.shutdown()