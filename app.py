# ✅ Always do this FIRST
import eventlet
eventlet.monkey_patch()

# Now import everything else
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_room')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('user_joined', {'user': data['user']}, room=room)

@socketio.on('text_change')
def handle_text_change(data):
    room = data['room']
    emit('text_update', {'text': data['text']}, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
