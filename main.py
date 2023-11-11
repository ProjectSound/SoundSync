import sounddevice as sd
import time
import sys
import numpy as np
import threading
import collections
from time import sleep
from threading import Lock
from pycaw.pycaw import AudioUtilities
from datetime import datetime, timedelta

class AudioController:
    def __init__(self, process_name: str):
        self.process_name = process_name
        self.volume = self.process_volume()

    def mute(self) -> None:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, "has been muted.")  # debug

    def unmute(self) -> None:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, "has been unmuted.")  # debug

    def process_volume(self) -> float:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print("Volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels: float) -> None:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print("Volume set to", self.volume)  # debug

    @staticmethod
    def list_applications() -> list:
        sessions = AudioUtilities.GetAllSessions()
        apps = []
        for index, session in enumerate(sessions):
            if session.Process:
                print(f"Index {index}: {session.Process.name()}")
                apps.append(session.Process.name())
        return apps

class InputState:
    def __init__(self, threshold, threshold_not_reached, normal_level, detected_level):
        self.threshold = threshold
        self.threshold_not_reached = threshold_not_reached
        self.normal_level = normal_level
        self.detected_level = detected_level
        self.is_faded = False
        self.timeout_timestamp = None
        self.max_rms = 0.1 

class SharedState:
    def __init__(self):
        self.active_input = None
        self.lock = Lock()

# print("Enter index of app")
# app_index = int(input())
# if app_index >= len(apps):
#     print("Invalid index. Please enter a number between 0 and", len(apps)-1)
# else:
#     audio_controller = AudioController(apps[app_index])


apps = AudioController.list_applications()
app_index = 3
audio_controller = AudioController(apps[app_index])
threshold1 = 30
threshold_not_reached1 = 5
threshold2 = 30
threshold_not_reached2 = 2
normal_sound_level = 1
detected_sound_level = 0.3

#normal_sound_level = float(input("Normal sound level: "))
#detected_sound_level = float(input("Turned down to level: "))
# for i in range(2):
#     print(f"Enter the threshold value for input {i+1}:")
#     threshold.append(float(input()))

#     print(f"Enter the threshold not reached duration (in seconds) for input {i+1}:")
#     threshold_not_reached.append(int(input()))

audio_controller = AudioController(apps[app_index])
rms_values = collections.deque(maxlen=10)
max_rms_values = collections.deque(maxlen=1000)

state_lock = Lock()
shared_state = SharedState()
def audio_callback(indata, frames, time_info, status, input_state, other_state, audio_controller):
    rms = np.linalg.norm(indata)
    min_rms = 0.1

    with shared_state.lock:
        input_state.max_rms = max(input_state.max_rms, rms)
        mapped_value = (rms - min_rms) / (input_state.max_rms - min_rms) * 100.0 if (input_state.max_rms - min_rms) > 0 else 0

        print(f"Input RMS: {rms}, Mapped Value: {mapped_value}, Threshold: {input_state.threshold}")  # Dodane logowanie

        if mapped_value >= input_state.threshold:
            if not input_state.is_faded:
                print(f"Fading audio down for input state with threshold {input_state.threshold}")  # Dodane logowanie
                fade_audio(audio_controller, input_state.detected_level, duration=1)
                input_state.is_faded = True
            input_state.timeout_timestamp = datetime.now()
            shared_state.active_input = input_state
        else:
            if shared_state.active_input == input_state:
                if datetime.now() - input_state.timeout_timestamp >= timedelta(seconds=input_state.threshold_not_reached):
                    if other_state.is_faded:
                        if datetime.now() - other_state.timeout_timestamp >= timedelta(seconds=other_state.threshold_not_reached):
                            print(f"Fading audio up for input state with threshold {input_state.threshold}")  # Dodane logowanie
                            fade_audio(audio_controller, input_state.normal_level, duration=1)
                            input_state.is_faded = False
                            other_state.is_faded = False
                            shared_state.active_input = None
                    else:
                        print(f"Fading audio up for input state with threshold {input_state.threshold}")  # Dodane logowanie
                        fade_audio(audio_controller, input_state.normal_level, duration=1)
                        input_state.is_faded = False
                        shared_state.active_input = None

    sd.sleep(1)

state_input1 = InputState(threshold1, threshold_not_reached1, normal_sound_level, detected_sound_level)
state_input2 = InputState(threshold2, threshold_not_reached2, normal_sound_level, detected_sound_level)

# Przypisanie funkcji callback do każdego inputu
callback_function1 = lambda indata, frames, time_info, status: audio_callback(indata, frames, time_info, status, state_input1, state_input2, audio_controller)
callback_function2 = lambda indata, frames, time_info, status: audio_callback(indata, frames, time_info, status, state_input2, state_input1, audio_controller)

devices = sd.query_devices()
input_devices = [device for device in devices if device['max_input_channels'] > 0 and not device['name'].startswith('Loopback')]
device_names = set()

devices = sd.query_devices()
for i, device in enumerate(devices):
    if device['hostapi'] == 0 and device['max_input_channels'] > 0:
        print(f"Device {i}: {device['name']}")

device_indices = []
for i in range(2):
    device_index = int(input(f"Enter the index of input device {i+1}: "))
    device_indices.append(device_index)

# Create input streams for the chosen devices
streams = []
threads = []

for i in range(2):
    device_name = input_devices[device_indices[i]]['name']
    callback_function = callback_function1 if i == 0 else callback_function2
    stream = sd.InputStream(device=device_name, channels=2, callback=callback_function)
    streams.append(stream)
    thread = threading.Thread(target=stream.start)
    threads.append(thread)
    thread.start()

volume_lock = Lock()
def fade_audio(audio_controller, target_level, duration=1):
    with volume_lock:
        current_level = audio_controller.process_volume()
        if current_level != target_level:
            start_time = time.time()
            while True:
                elapsed = time.time() - start_time
                if elapsed > duration:
                    break
                new_level = current_level + (target_level - current_level) * (elapsed / duration)
                audio_controller.set_volume(new_level)
                time.sleep(0.01)  # Krótkie opóźnienie dla płynnego przejścia
            audio_controller.set_volume(target_level)

def timeout_handler(threshold_not_reached, audio_controller):
    time.sleep(threshold_not_reached)

if __name__ == "__main__":
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop both streams when the program ends
        for stream in streams:
            stream.stop()