from app import create_app
import ssl
from flask_socketio import SocketIO
from app.controllers.msg_events import register_socketio_events
# from gevent import pywsgi

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")
register_socketio_events(socketio)

if __name__ == '__main__':
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # ssl_pem = './ssl/api.within-circle.techvip.site.pem'
    # ssl_key = './ssl/api.within-circle.techvip.site.key'
    # context.load_cert_chain(ssl_pem, ssl_key)
    # app.run(port=1029, ssl_context=context)
    # app.run(port=1029)
    socketio.run(app, port=1029)
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # server.serve_forever()
