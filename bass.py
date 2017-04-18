from pybass import *

BASS_Init(-1, 44100, 0, 0, 0)
print("BASS initialized...")
BASS_PluginLoad("basswv.dll", 0);

handle = BASS_StreamCreateFile(False, u"sound_files/piano2.wv", 0, 0, BASS_UNICODE)

play_handle(handle, show_tags=False)
if BASS_ErrorGetCode() != BASS_OK:
    print('BASS_ChannelPlay error: %s' % get_error_description(BASS_ErrorGetCode()))
else:
    print("Done playing...")

BASS_Free()
