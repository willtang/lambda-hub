import sys
from time import sleep
import audiotools
from audiotools.player import Player, PLAYER_STOPPED, PLAYER_PAUSED, PLAYER_PLAYING
import pyaudio


CHUNK = 1024


if len(sys.argv) < 2:
    print("Plays an audio file.\n\nUsage: %s file" % sys.argv[0])
    sys.exit(-1)


audio_file = audiotools.open(sys.argv[1])

print("FORMAT: %s" % audio_file.NAME)
channels = audio_file.channels()
print("CHANNELS: %s" % audio_file.channels())
print("BITS: %d" % audio_file.bits_per_sample())
rates = audio_file.sample_rate()
print("RATES: %d Hz" % audio_file.sample_rate())
print("LENGTH: %d s" % audio_file.seconds_length())

print("LOSSLESS? %s" % audio_file.lossless())
print("METADATA? %s" % audio_file.supports_metadata())
print("TO PCM? %s" % audio_file.supports_to_pcm())
print("SEEK? %s" % audio_file.seekable())

total_frames = audio_file.total_frames()
print("TOTAL FRAME: %d" % total_frames)

reader = audio_file.to_pcm()
# frame_list = reader.read(CHUNK)
# for frame in frame_list:
#     print("Frmae: %d" % frame)


p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=channels,
                rate=rates,
                output=True)

frame_list = reader.read(CHUNK)
data = frame_list.to_bytes(False, True)

print("Playing now...")

while data != '':
    stream.write(data)
    frame_list = reader.read(CHUNK)
    data = frame_list.to_bytes(False, True)

reader.close()

p.terminate()


# audio_output = None
# outputs = audiotools.player.available_outputs()
# for output in outputs:
#     print("OUTPUT: %s" % output.NAME)
#     if "NULL" not in output.NAME:
#         audio_output = output
#         break
#
# print("USING: %s" % audio_output)

# player = Player(audio_output)
# player.open(audio)
# player.set_volume(1)
# player.play()
# print("STATE: %s" % player.state())
# while (player.state() == PLAYER_PLAYING):
#     sleep(0.1)
#     print("STATE: %s" % player.state())
#
# player.close()
