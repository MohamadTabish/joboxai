import sounddevice as sd
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

SOUND_AMPLITUDE = 0
AUDIO_CHEAT = 0

CALLBACKS_PER_SECOND = 38
SUS_FINDING_FREQUENCY = 4
SOUND_AMPLITUDE_THRESHOLD = 20  # Lowered the threshold to make it sensitive to lower volume

FRAMES_COUNT = int(CALLBACKS_PER_SECOND / SUS_FINDING_FREQUENCY)
AMPLITUDE_LIST = list([0] * FRAMES_COUNT)
SUS_COUNT = 0
count = 0

# Create global variable to store audio data
AUDIO_DATA = []

def print_sound(indata, outdata, frames, time, status):
    avg_amp = 0
    global SOUND_AMPLITUDE, SUS_COUNT, count, SOUND_AMPLITUDE_THRESHOLD, AUDIO_CHEAT, AUDIO_DATA
    vnorm = int(np.linalg.norm(indata) * 10)
    AMPLITUDE_LIST.append(vnorm)
    count += 1
    AMPLITUDE_LIST.pop(0)
    if count == FRAMES_COUNT:
        avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT
        SOUND_AMPLITUDE = avg_amp
        AUDIO_DATA.append(indata.copy())  # Store audio data
        if SUS_COUNT >= 1:
            AUDIO_CHEAT = 1
            SUS_COUNT = 0
        if avg_amp > SOUND_AMPLITUDE_THRESHOLD:
            SUS_COUNT += 1
        else:
            SUS_COUNT = 0
            AUDIO_CHEAT = 0
        count = 0

def sound():
    print("Starting audio processing...")
    with sd.Stream(callback=print_sound):
        sd.sleep(-1)

@app.route('/audio_data', methods=['POST'])
def receive_audio_data():
    data = request.get_json()
    audio_data = data['audioData']
    # Store or process audio_data as needed
    return jsonify({'message': 'Audio data received and processed successfully'})

def get_audio_data():
    return AUDIO_DATA

if __name__ == "__main__":
    sound()
