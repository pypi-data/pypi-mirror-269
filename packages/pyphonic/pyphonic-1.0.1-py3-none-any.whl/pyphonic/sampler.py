from pathlib import Path

import pyphonic
from pyphonic import MidiMessage
import numpy as np
import librosa

sample = np.load(pyphonic.getDataDir() / Path("glockenspiel.pkl"), allow_pickle=True)

def noteToFreq(midi_note):
    a = 440
    return (a / 32) * (2 ** ((midi_note - 9) / 12))

print("Building wavetable")
voices = {}
for note in range(31, 103): # G1 to G7
    print(f"Building wavetable {note}")
    if note == 60:
        ratio = 1 # Center on C3
    else:
        freq = noteToFreq(note)
        ratio = freq / 261.63
    left = librosa.effects.pitch_shift(sample[0], sr=44100, n_steps=(note - 60))
    right = librosa.effects.pitch_shift(sample[1], sr=44100, n_steps=(note - 60))
    joined = np.array([left, right])
    voices[note] = {"wave": joined, "position": 0, "playing": False, "velocity": 0}

def process_npy(midi, audio):

    for msg in midi:
        if msg.note not in voices:
            continue
        if msg.type == "note_on":
            if voices[msg.note]["playing"]:
                voices[msg.note]["position"] = 0
            else:
                voices[msg.note]["playing"] = True
            voices[msg.note]["velocity"] = msg.velocity
        elif msg.type == "note_off":
            voices[msg.note]["position"] = 0
            voices[msg.note]["playing"] = False
            # Could add some tail off instead of dead stop
    
    new_audio = np.zeros((pyphonic.getNumChannels(), pyphonic.getBlockSize()))

    for voice, data in voices.items():
        if not data["playing"]:
            continue
        start_pos = data["position"] % data["wave"].shape[1]
        end_pos = (start_pos + pyphonic.getBlockSize())
        if end_pos >= data["wave"].shape[1]:
            end_pos = data["wave"].shape[1]
            new_audio[:, :end_pos - start_pos] += data["wave"][:, start_pos:end_pos]
            voices[voice]["position"] = 0
            voices[voice]["playing"] = False
        else:
            new_audio += data["wave"][:, start_pos:end_pos] * (data["velocity"] / 127)
            voices[voice]["position"] += pyphonic.getBlockSize()
    
    return midi, new_audio