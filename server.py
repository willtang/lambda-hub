from flask import Flask
import atexit
from pybass import *

app = Flask(__name__)

def init():
    BASS_Init(-1, 44100, 0, 0, 0)
    print("BASS initialized...")

def cleanup():
    try:
        BASS_Free()
    except Exception:
        pass

    print("\nBASS freed...")


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/version")
def version():
    return "LambdaHubServer v0.1"

@app.route("/play/<path:soundfile>")
def play(soundfile):
    print('Opening sound file: %s' % soundfile)
    print('String type: %s' % type(soundfile))
    soundfile = soundfile.encode('ascii','ignore')
    print('String type: %s' % type(soundfile))
    handle = BASS_StreamCreateFile(False, soundfile, 0, 0, 0)
    play_handle(handle, show_tags=False)
    result = ''
    if BASS_ErrorGetCode() != BASS_OK:
        result ='BASS_ChannelPlay error: %s' % get_error_description(BASS_ErrorGetCode())
    else:
        result = "Done playing..."

    return result


if __name__ == "__main__":
    init()
    atexit.register(cleanup)
    app.run()
