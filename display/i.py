from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Web page rendering
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('screen_share_start')
def handle_screen_share_start():
    socketio.emit('screen_share_start', broadcast=True, include_self=False)

@socketio.on('screen_share_stop')
def handle_screen_share_stop():
    socketio.emit('screen_share_stop', broadcast=True, include_self=False)

if __name__ == '__main__':
    try:
        socketio.run(app, port=5000)
    except Exception as e:
        print(f"An error occurred: {e}")