import atexit
import platform
from os import listdir, path, walk

from flask import Flask, abort
from pybass import *

app = Flask(__name__)
handle = None

def init():
    BASS_Init(-1, 44100, 0, 0, 0)
    BASS_PluginLoad("basswv.dll", 0);
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

@app.route("/list/", methods=['GET'])
def listroot():
    # return list('./')
    listdir = './'

    if not path.isdir(listdir):
        abort(404, 'File not found: %s' % soundfile)

    result = "<ul>"
    for (dirpath, dirnames, filenames) in walk(listdir):
        for d in dirnames:
            href = path.join(dirpath, d).replace(u'\\', u'/')
            result += '<li>[<a href="%s">%s</a>]</li>' % (href, d)
        for f in filenames:
            href = '/play/' + path.join(dirpath, f).replace(u'\\', u'/')
            result += '<li><a href="%s">%s</a></li>' % (href, f)
        break
    result += "</ul>"
    return result

@app.route("/list/<path:listdir>", methods=['GET'])
def list(listdir):
    if not path.isdir(listdir):
        abort(404, 'File not found: %s' % soundfile)

    result = "<ul>"
    for (dirpath, dirnames, filenames) in walk(listdir):
        for d in dirnames:
            href = path.join(dirpath, d).replace(u'\\', u'/')
            result += '<li>[<a href="%s">%s</a>]</li>' % (href, d)
        for f in filenames:
            href = '/play/' + path.join(dirpath, f).replace(u'\\', u'/')
            result += '<li><a href="%s">%s</a></li>' % (href, f)
        break
    result += "</ul>"
    return result

@app.route("/play/<path:soundfile>", methods=['GET'])
def play(soundfile):
    if platform.system() == 'Windows':
        soundfile = soundfile.replace(u'/', u'\\')

    if not path.isfile(soundfile):
        abort(404, 'File not found: %s' % soundfile)

    print('Opening sound file: %s' % soundfile)
    handle = BASS_StreamCreateFile(False, soundfile, 0, 0, BASS_UNICODE)
    # play_handle(handle, show_tags=False)

    # channel_info = BASS_CHANNELINFO()
    # if not BASS_ChannelGetInfo(handle, channel_info):
    #     abort(500, 'BASS_ChannelGetInfo error: %s' % get_error_description(BASS_ErrorGetCode()))

    # channel_length = BASS_ChannelGetLength(handle, BASS_POS_BYTE)
    # channel_position = BASS_ChannelGetPosition(handle, BASS_POS_BYTE)

    if not BASS_ChannelPlay(handle, False):
        abort(500, 'BASS_ChannelPlay error: %s' % get_error_description(BASS_ErrorGetCode()))

    return 'Playing...'

@app.route("/pause", methods=['GET'])
def pause():
    if not BASS_Pause():
        abort(500, 'BASS_Pause error: %s' % get_error_description(BASS_ErrorGetCode()))

    return 'Paused'

@app.route("/stop", methods=['GET'])
def stop():
    if not BASS_Stop():
        abort(500, 'BASS_Stop error: %s' % get_error_description(BASS_ErrorGetCode()))

    return 'Stopped'

@app.route("/setvolume/<int:volume>", methods=['GET'])
def set_volume(volume):
    if not BASS_SetVolume(volume / 100.0):
        abort(500, 'BASS_SetVolume error: %s' % get_error_description(BASS_ErrorGetCode()))

    return 'Volume set to %f' % (volume / 100.0)

@app.route("/getvolume", methods=['GET'])
def get_volume():
    volume = BASS_GetVolume()
    if not BASS_ErrorGetCode() == BASS_OK:
        abort(500, 'BASS_GetVolume error: %s' % get_error_description(BASS_ErrorGetCode()))

    return volume

@app.route("/getstatus", methods=['GET'])
def get_status():
    channel_position = BASS_ChannelGetPosition(handle, BASS_POS_BYTE)
    if not BASS_ErrorGetCode() == BASS_OK:
        abort(500, 'BASS_GetVolume error: %s' % get_error_description(BASS_ErrorGetCode()))

    return '{"channel_position": %s}' % channel_position


if __name__ == "__main__":
    init()
    atexit.register(cleanup)
    app.debug = True
    app.run()
    #app.run(threaded=True)
