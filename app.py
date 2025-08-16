from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import serial, time, threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Arduino serial port (adjust COMx or /dev/ttyUSB0)
ser = serial.Serial('COM3', 115200)  

def read_serial():
    while True:
        try:
            data = ser.readline().decode().strip()
            if data.isdigit():
                socketio.emit('eeg_data', {'value': int(data)})
        except:
            pass
        time.sleep(0.02)  # ~50Hz

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=read_serial, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
