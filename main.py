import sounddevice as sd
import time
import sys
import numpy as np
import threading
import collections
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
    
apps = AudioController.list_applications()
print("Enter index of app")
app_index = int(input())
if app_index >= len(apps):
    print("Invalid index. Please enter a number between 0 and", len(apps)-1)
else:
    audio_controller = AudioController(apps[app_index])

threshold = []
threshold_not_reached = []

for i in range(2):
    print(f"Enter the threshold value for input {i+1}:")
    threshold.append(float(input()))

    print(f"Enter the threshold not reached duration (in seconds) for input {i+1}:")
    threshold_not_reached.append(int(input()))

max_rms = 0.1
timeout_threads = [None] * len(threshold)
audio_controller = AudioController(apps[app_index])
max_amplitude = 2**24 - 1  # Dla dźwięku o rozdzielczości 16 bitów

rms_values = collections.deque(maxlen=10)
max_rms_values = collections.deque(maxlen=1000)

#create_audio_callback
def create_audio_callback(threshold, threshold_not_reached):
    timeout_threads = [None] * len(threshold)
    timeout_timestamps = [None] * len(threshold)
    max_rms = 0.1

    def audio_callback(indata, frames: int, time: float, status: sd.CallbackFlags) -> None:
        nonlocal timeout_threads
        nonlocal timeout_timestamps
        nonlocal max_rms
            # global threshold
            # global timeout_thread
            # global timeout_timestamp

        rms = np.linalg.norm(indata)
        min_rms = 0.1
        max_rms = max(max_rms, rms)
        if (max_rms - min_rms) > 0:
            mapped_value = (rms - min_rms) / (max_rms - min_rms) * 100.0
            mapped_value = min(max(mapped_value, 0), 100)
        else:
            mapped_value = 0

        for i in range(len(threshold)):
            if mapped_value >= threshold[i] and timeout_threads[i] is not None:
                timeout_timestamps[i] = datetime.now()

            if mapped_value >= threshold[i] and timeout_threads[i] is None:
                print(f"Próg głośności dla input {i+1} osiągnięty, rozpoczynam wątek timeouta")
                fade_audio(1.0, 0.05, 1)
                timeout_threads[i] = threading.Thread(target=timeout_handler, args=(i,))
                timeout_threads[i].start()

            elif mapped_value < threshold[i] and timeout_threads[i] is not None:
                if timeout_timestamps[i] is not None:
                    time_elapsed = datetime.now() - timeout_timestamps[i]
                    if time_elapsed >= timedelta(seconds=threshold_not_reached[i]):
                        print(f"Poziom głośności dla input {i+1} poniżej progu przez {threshold_not_reached[i]} sekund, kończę wątek timeouta")
                        timeout_threads[i].join()
                        print("Zwiększam poziom")
                        fade_audio(0.05, 1.0, 1)
                        timeout_threads[i] = None
        sd.sleep(1)

    return audio_callback        

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
    stream = sd.InputStream(device=device_name, channels=2, callback=create_audio_callback(threshold=[threshold[i]], threshold_not_reached=[threshold_not_reached[i]]))
    streams.append(stream)

    # Start the input streams in separate threads
    thread = threading.Thread(target=stream.start)
    threads.append(thread)
    thread.start()

def fade_audio(start: float, end: float, duration: int = 2) -> None:
    """
    Parameters:

    start(float): The initial volume level.
    end(float): The final volume level.
    duration(int): The time over which to change the volume, in sec. Default - 2 sec
    """    
    start_time = time.time()  # Zapisz czas rozpoczęcia pętli

    start = int(start * 100)
    end = int(end * 100)

    if start < end:
        step = 5
    elif start > end:
        step = -5
    else:
        return

    for value in range(start, end + step, step):
        audio_controller.set_volume(float(value / 100))

        elapsed_time = time.time() - start_time  # Oblicz czas, który minął od rozpoczęcia pętli

        if end == value:
            time_to_sleep = 0
        else:
            time_to_sleep = (duration - elapsed_time) / (abs(end - value))  # Oblicz czas oczekiwania na kolejną iterację
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

def timeout_handler(i) -> None:
    time.sleep(threshold_not_reached[i])  # Oczekuj threshold dla input1 oraz input2 sekund

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