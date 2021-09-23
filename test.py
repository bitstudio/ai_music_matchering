import matchering as mg
import pickle
from scipy.io import wavfile

target_wav = "D:/bitstudio/ai_music/MusicProducer/4_track.wav"
ref_wav = "D:/bitstudio/ai_music/MusicProducer/wav_ref.wav"

output_original_method = "D:/bitstudio/ai_music/MusicProducer/4_track_match_original.wav"
output_our_method = "D:/bitstudio/ai_music/MusicProducer/4_track_match_our_method.wav"

parameters = mg.get_ref_parameters(ref_wav)

print(type(parameters))

for e in parameters:
    if len(e.shape) == 0:
        print(e)
    else:
        print(e.shape)

with open("test.pickle","wb") as f:
    pickle.dump(parameters, f)

with open("test.txt","w") as f:
    f.write(",".join([str(e.tolist()) for e in parameters]))


# test original
print("testing original")
mg.process(
    target=target_wav,
    reference=ref_wav,
    results=[
        mg.pcm16(output_original_method),
    ],
)

# test our method
print("testing out method")
mg.process(
    target=target_wav,
    reference=parameters,
    results=[
        mg.pcm16(output_our_method),
    ],
)

# testing equality

original_sr, original_wav_dat = wavfile.read(output_original_method)
our_sr, our_wav_data = wavfile.read(output_our_method)

print("sampling rate equality", original_sr == our_sr)
print("wav data shape equality",original_wav_dat.shape == our_wav_data.shape)
print("wav data equality", (original_wav_dat == our_wav_data).sum()/(our_wav_data.shape[0]*our_wav_data.shape[1]))

# test extracts
mg.extract_ref_wav_parameters_from_root("D:/bitstudio/ai_music/ai_music_backend/music_generator/assets/ref_songs")