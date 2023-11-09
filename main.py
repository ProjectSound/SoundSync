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

max_rms = 0.1
threshold = 5
timeout_thread = None
timeout_timestamp = None
audio_controller = AudioController(apps[app_index])
max_amplitude = 2**24 - 1  # Dla dźwięku o rozdzielczości 16 bitów

rms_values = collections.deque(maxlen=10)
max_rms_values = collections.deque(maxlen=1000)

def audio_callback(indata, frames: int, time: float, status: sd.CallbackFlags) -> None:
    global max_rms
    global threshold
    global timeout_thread
    global timeout_timestamp

    mapped_value = np.linalg.norm(indata)*10

    rms = np.linalg.norm(indata)  # Calculate RMS value
    rms_values.append(rms)  # Add RMS value to deque
    avg_rms = sum(rms_values) / len(rms_values)  # Calculate moving average of RMS values

    min_rms = 0.1  # Minimum RMS value to 0%
    max_rms = max(max_rms, avg_rms)  # Update maximum RMS value

    if (max_rms - min_rms) > 0:
        mapped_value = (avg_rms - min_rms) / (max_rms - min_rms) * 100.0  # Scale value from 0% to 100%
    else:
        mapped_value = 0

    compression_ratio = 2.0
    threshold = 50.0
    if mapped_value > threshold:
        mapped_value = threshold + (mapped_value - threshold) / compression_ratio

    # rms = np.linalg.norm(indata)  # Oblicz wartość RMS sygnału
    # min_rms = 0.1  # Minimalna wartość RMS, która odpowiada 0%
    # max_rms = max(max_rms, rms)  # Zaktualizuj maksymalną wartość RMS
    # if (max_rms - min_rms) > 0:
    #     mapped_value = (rms - min_rms) / (max_rms - min_rms) * 100.0  # Skaluj wartość od 0% do 100%
    # else:
    #     mapped_value = 0

    # print(rms)

    #print(f"Poziom głośności: {mapped_value:.2f}% (Maks RMS: {max_rms:.2f})")

    if mapped_value >= threshold and timeout_thread is not None:
        timeout_timestamp = datetime.now()  # Zapisz czas przekroczenia progu

    if mapped_value >= threshold and timeout_thread is None:
        print("Próg głośności osiągnięty, rozpoczynam wątek timeouta")
        fade_audio(1.0, 0.05, 1)
        # audio_controller.set_volume(0.05)
        timeout_thread = threading.Thread(target=timeout_handler)
        timeout_thread.start()

    elif mapped_value < threshold and timeout_thread is not None:
        if timeout_timestamp is not None:
            time_elapsed = datetime.now() - timeout_timestamp
            if time_elapsed >= timedelta(seconds=5):
                print("Poziom głośności poniżej progu przez 5 sekund, kończę wątek timeouta")
                timeout_thread.join()
                print("Zwiększam poziom")
                fade_audio(0.05, 1.0, 1)
                # audio_controller.set_volume(1.0)
                timeout_thread = None
    
    #print(max(lisa))
    sd.sleep(1)


devices = sd.query_devices()
input_devices = [device for device in devices if device['max_input_channels'] > 0 and not device['name'].startswith('Loopback')]
device_names = set()

#show all with channels
# for device in devices:
#     if device['max_input_channels'] > 0 and not device['name'].startswith('Loopback'):
#         device_name = device['name']
#         if device_name not in device_names:
#             input_devices.append(device)
#             device_names.add(device_name)

# print("Available input devices:")
# for i, device in enumerate(input_devices):
#     print(f"Device {i}: {device['name']} - {device['hostapi']} - {device['max_input_channels']} channels")
#show all without channels

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
for i in range(2):
    device_name = input_devices[device_indices[i]]['name']
    stream = sd.InputStream(device=device_name, channels=2, callback=audio_callback)
    streams.append(stream)

    # Start the input streams in separate threads
threads = []
for i in range(2):
    thread = threading.Thread(target=streams[i].start)
    threads.append(thread)
    threads[i].start()



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


def timeout_handler() -> None:
    time.sleep(5)  # Oczekuj 5 sekund

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