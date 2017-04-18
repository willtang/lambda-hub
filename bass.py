from pybass import *
import time
from os import path

BASS_Init(-1, 44100, 0, 0, 0)
print("BASS initialized...")

if platform.system() == 'Windows':
    if not BASS_PluginLoad(path.abspath('./basswv.dll'), 0):
        print('WV Plugin Error: %s' % get_error_description(BASS_ErrorGetCode()))
elif platform.system().lower() == 'darwin':
    if not BASS_PluginLoad(path.abspath('./libbassflac.dylib'), 0):
        print('FLAC Plugin Error: %s' % get_error_description(BASS_ErrorGetCode()))
    if not BASS_PluginLoad(path.abspath('./libbasswv.dylib'), 0):
        print('WV Plugin Error: %s' % get_error_description(BASS_ErrorGetCode()))
    if not BASS_PluginLoad(path.abspath('./libbassdsd.dylib'), 0):
        print('DSD Plugin Error: %s' % get_error_description(BASS_ErrorGetCode()))
else:
    if not BASS_PluginLoad(path.abspath('./libbasswv.so'), 0):
        print('WV Plugin Error: %s' % get_error_description(BASS_ErrorGetCode()))

handle = BASS_StreamCreateFile(False, "sound_files/piano2.wv", 0, 0, 0)
# print('Handle: %d' % handle)
if not handle:
    print('BASS_StreamCreateFile error: %s' % get_error_description(BASS_ErrorGetCode()))

print("Playing...")
# play_handle(handle, show_tags=False)
# if BASS_ErrorGetCode() != BASS_OK:
if not BASS_ChannelPlay(handle, False):
    print('BASS_ChannelPlay error: %s' % get_error_description(BASS_ErrorGetCode()))
else:
    channel_length = BASS_ChannelGetLength(handle, BASS_POS_BYTE)
    channel_position = BASS_ChannelGetPosition(handle, BASS_POS_BYTE)
    while channel_position < channel_length:
        channel_position = BASS_ChannelGetPosition(handle, BASS_POS_BYTE)
        time.sleep(0.25)

    print("Done playing...")

BASS_Free()

print("BASS freed")
