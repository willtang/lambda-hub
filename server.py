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


@app.route("/", methods=['GET'])
@app.route("/version", methods=['GET'])
def version():
    return "LambdaHubServer v0.1"

@app.route("/play/<path:soundfile>", methods=['GET'])
def play(soundfile):
    print('Opening sound file: %s' % soundfile)
    # print('String type: %s' % type(soundfile))
    soundfile = soundfile.encode('ascii', 'ignore')
    # print('String type converted: %s' % type(soundfile))
    handle = BASS_StreamCreateFile(False, soundfile, 0, 0, BASS_STREAM_AUTOFREE)
    # play_handle(handle, show_tags=False)

    channel_info = BASS_CHANNELINFO()
    if not BASS_ChannelGetInfo(handle, channel_info):
        return 'BASS_ChannelGetInfo error: %s' % get_error_description(BASS_ErrorGetCode())

    channel_length = BASS_ChannelGetLength(handle, BASS_POS_BYTE)
    channel_position = BASS_ChannelGetPosition(handle, BASS_POS_BYTE)

    if not BASS_ChannelPlay(handle, False):
        return 'BASS_ChannelPlay error: %s' % get_error_description(BASS_ErrorGetCode())

    return 'Playing...'


if __name__ == "__main__":
    init()
    atexit.register(cleanup)
    app.run()
