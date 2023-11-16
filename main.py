
import sounddevice as sd
import time
import sys
import numpy as np
import threading
import collections
import keyboard
from time import sleep
from threading import Lock
from pycaw.pycaw import AudioUtilities
from datetime import datetime, timedelta

class AudioController:
    def __init__(self, process_name: str):
        self.process_name = process_name
        self.volume = self.process_volume()

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

class Bind:
    def __init__(self, audio_controller):
        self.audio_controller = audio_controller
        self.is_manually_muted = False
        self.is_app_running = True
        self.is_input1_disabled = False
        self.is_input2_disabled = False

    # MUTE CONTROLLED APP (TOGGLE)
    def toggle_mute(self):
        if self.is_manually_muted:
            self.audio_controller.set_volume(self.audio_controller.previous_volume)
            self.is_manually_muted = False
        else:
            self.audio_controller.previous_volume = self.audio_controller.process_volume()
            self.audio_controller.set_volume(0)
            self.is_manually_muted = True
        print(f"{self.audio_controller.process_name} mute toggled.")

    def is_muted(self):
        return self.is_manually_muted
    
    # START / STOP APP
    def toggle_app_running(self):
        global streams
        if self.is_app_running:
            for stream in streams:
                stream.stop()
            self.is_app_running = False
            print("App stopped")
        else:
            for stream in streams:
                stream.start()
            self.is_app_running = True

    # DISABLE INPUT 1
    @staticmethod
    def disable_input1(self):
        self.is_input1_disabled = not self.is_input1_disabled
    # DISABLE INPUT 2
    @staticmethod
    def disable_input2(self):
        self.is_input2_disabled = not self.is_input2_disabled

    #HARD
    @staticmethod
    def set_hard_mode():
        cut_off.set_mode("Hard")
    #FADE
    @staticmethod
    def set_fade_mode():
        cut_off.set_mode("Fade")
    #HARD FADE
    @staticmethod
    def set_hard_fade_mode():
        cut_off.set_mode("Hard cut + fade up")
    #FADE HARD
    @staticmethod
    def set_fade_hard_mode():
        cut_off.set_mode("Fade down + hard up")
    #Mute FADE
    @staticmethod
    def set_mute_hard_mode():
        cut_off.set_mode("Mute + fade up")
    #MUTE HARD
    @staticmethod
    def set_mute_fade_mode():
        cut_off.set_mode("Mute + hard up")

    #LIST BINDS
    @staticmethod
    def list_active_binds():
        print("Active binds:")
        for key, function in current_binds.items():
            print(f"{key}: {function.__name__}")

    @staticmethod
    def list_available_binds():
        print("Available binds:")
        for function_name in available_binds:
            print(function_name)

    #ADD BIND
    @staticmethod
    def add_bind(key_combination, function_name):
        global current_binds, available_binds
        if function_name in available_binds:
            function_to_bind = available_binds[function_name]
            current_binds[key_combination] = function_to_bind
            del available_binds[function_name]
            keyboard.add_hotkey(key_combination, function_to_bind)
            print(f"Bind '{key_combination}' added for '{function_name}'.")
        else:
            print(f"Function '{function_name}' not available.")

    #REMOVE BIND
    @staticmethod
    def remove_bind(key_combination):
        global current_binds, available_binds
        # Check if the bind exists in current_binds
        if key_combination in current_binds:
            # Check if the bind was actually added as a hotkey
            if key_combination in keyboard._hotkeys:
                keyboard.remove_hotkey(key_combination)

            function_name = current_binds[key_combination].__name__
            available_binds[function_name] = current_binds[key_combination]
            del current_binds[key_combination]
            print(f"Bind '{key_combination}' removed.")
        else:
            print(f"No bind found for '{key_combination}'.")
 
class CutOff:
    def __init__(self, audio_controller, normal_level, detected_level):
        self.audio_controller = audio_controller
        self.normal_level = normal_level
        self.detected_level = detected_level
        self.mode = "fade"  # Domyślny tryb

    def set_mode(self, mode):
        self.mode = mode
        print(f"CutOff mode set to {mode}")

    def apply_volume(self, input_state):
        new_level = self.normal_level if input_state.is_faded else self.detected_level

        if self.mode == "Fade":
            CutOff.fade_audio(self.audio_controller, new_level, duration=1)
        elif self.mode == "Hard":
            self.audio_controller.set_volume(new_level)
        elif self.mode == "Fade down + hard up":
            if input_state.is_faded:
                self.audio_controller.set_volume(new_level)  # Hard
            else:
                CutOff.fade_audio(self.audio_controller, new_level, duration=1)  # Fade
        elif self.mode == "Hard cut + fade up":
            if input_state.is_faded:
                CutOff.fade_audio(self.audio_controller, new_level, duration=1)  # Fade
            else:
                self.audio_controller.set_volume(new_level)  # Hard
        elif self.mode == "Mute + fade up":
            if input_state.is_faded:
                CutOff.fade_audio(self.audio_controller, new_level, duration=1)  # Fade
                input_state.is_faded = False
            else:
                self.audio_controller.set_volume(0) # Mute
                input_state.is_faded = True
        elif self.mode == "Mute + hard up":
            if input_state.is_faded:
                self.audio_controller.set_volume(new_level)  # Hard
                input_state.is_faded = False
            else:
                self.audio_controller.set_volume(0) # Mute
                input_state.is_faded = True
        input_state.is_faded = not input_state.is_faded

    @staticmethod
    def fade_audio(audio_controller, target_level, duration=1):
        with Lock(): #volume_lock
            current_level = audio_controller.process_volume()
            if current_level != target_level:
                start_time = time.time()
                while True:
                    elapsed = time.time() - start_time
                    if elapsed > duration:
                        break
                    new_level = current_level + (target_level - current_level) * (elapsed / duration)
                    audio_controller.set_volume(new_level)
                    time.sleep(0.01)
                audio_controller.set_volume(target_level)
  
# cutoffModes = [
#     "Hard",
#     "Fade",
#     "Hard cut + fade up",
#     "Fade down + hard up",
#     "Mute + fade up",
#     "Mute + hard up"
# ]

device_indices = []
for i in range(2):
    device_index = int(input(f"Enter the index of input device {i+1}: "))
    device_indices.append(device_index)

# device_index = int(input(f"Enter the index of input device: "))
# device_indices.append(device_index)

threshold1 = 30
threshold_not_reached1 = 5
threshold2 = 30
threshold_not_reached2 = 2
normal_sound_level = 1
detected_sound_level = 0.3


apps = AudioController.list_applications()
app_index = 0
audio_controller = AudioController(apps[app_index])
bind = Bind(audio_controller)
cut_off = CutOff(audio_controller, normal_sound_level, detected_sound_level)

current_binds = {'f1': bind.toggle_mute, 
                 'f2': bind.toggle_app_running, 
                 'f3': bind.disable_input1, 
                 'f4': bind.disable_input2, 
                 '5': bind.set_hard_mode, 
                 '6': bind.set_fade_mode, 
                 '7': bind.set_fade_hard_mode, 
                 '8': bind.set_mute_fade_mode,
                 '9': bind.set_mute_hard_mode 
                 }

available_binds = {}

bind = Bind(audio_controller)


# keyboard.add_hotkey('f1', bind.toggle_mute)
# keyboard.add_hotkey('f2', bind.toggle_app_running)
# keyboard.add_hotkey('f3', bind.disable_input1)
# keyboard.add_hotkey('f4', bind.disable_input2)

# keyboard.add_hotkey('1', Bind.set_hard_mode)
# keyboard.add_hotkey('2', Bind.set_fade_mode)
# keyboard.add_hotkey('3', Bind.set_hard_fade_mode)
# keyboard.add_hotkey('4', Bind.set_fade_hard_mode)
# keyboard.add_hotkey('5', Bind.set_mute_fade_mode)
# keyboard.add_hotkey('6', Bind.set_mute_hard_mode)

use_input2 = len(device_indices) > 1 #Optional input

rms_values = collections.deque(maxlen=10)
max_rms_values = collections.deque(maxlen=1000)

state_lock = Lock()
shared_state = SharedState()
def audio_callback(indata, frames, time_info, status, input_state, other_state, audio_controller):
    # MUTE CONTROLLED APP (TOGGLE)
    if bind.is_muted(): #or not bind.is_app_running: 
        return
    # DISABLE INPUT 1/2
    if (input_state == state_input1 and bind.is_input1_disabled) or \
       (input_state == state_input2 and bind.is_input2_disabled):
        return

    #OPTIONAL INPUT2
    if not use_input2 and input_state == state_input2:
        return

    rms = np.linalg.norm(indata)
    min_rms = 0.1

    with shared_state.lock:
        input_state.max_rms = max(input_state.max_rms, rms)
        mapped_value = (rms - min_rms) / (input_state.max_rms - min_rms) * 100.0 if (input_state.max_rms - min_rms) > 0 else 0
        #print(f"Input RMS: {rms}, Mapped Value: {mapped_value}, Threshold: {input_state.threshold}")  # Dodane logowanie

        if mapped_value >= input_state.threshold:
            if not input_state.is_faded:
                # print(f"Fading audio down for input state with threshold {input_state.threshold}")  # Dodane logowanie
                # fade_audio(audio_controller, input_state.detected_level, duration=1)
                # HARD
                cut_off.apply_volume(input_state)
                input_state.is_faded = True
            input_state.timeout_timestamp = datetime.now()
            shared_state.active_input = input_state
        else:
            if shared_state.active_input == input_state:
                if datetime.now() - input_state.timeout_timestamp >= timedelta(seconds=input_state.threshold_not_reached):
                    if other_state.is_faded:
                        if datetime.now() - other_state.timeout_timestamp >= timedelta(seconds=other_state.threshold_not_reached):
                            # print(f"Fading audio up for input state with threshold {input_state.threshold}")  # Dodane logowanie
                            # fade_audio(audio_controller, input_state.normal_level, duration=1)
                            cut_off.apply_volume(input_state)
                            input_state.is_faded = False
                            other_state.is_faded = False
                            shared_state.active_input = None
                    else:
                        # print(f"Fading audio up for input state with threshold {input_state.threshold}")  # Dodane logowanie
                        # fade_audio(audio_controller, input_state.normal_level, duration=1)
                        cut_off.apply_volume(input_state)
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

#devices = sd.query_devices() ???
for i, device in enumerate(devices):
    if device['hostapi'] == 0 and device['max_input_channels'] > 0:
        print(f"Device {i}: {device['name']}")

# Create input streams for the chosen devices
streams = []
threads = []

for i in range(2 if use_input2 else 1):
    device_name = input_devices[device_indices[i]]['name']
    callback_function = callback_function1 if i == 0 else (callback_function2 if use_input2 else None)
    stream = sd.InputStream(device=device_name, channels=2, callback=callback_function)
    streams.append(stream)
    thread = threading.Thread(target=stream.start)
    threads.append(thread)
    thread.start()


def timeout_handler(threshold_not_reached, audio_controller):
    time.sleep(threshold_not_reached)

if __name__ == "__main__":
    try:
        while True:
            print("\nMenu:")
            print("1. Add a bind")
            print("2. Remove a bind")
            print("3. Exit")
            print("List acvite binds")
            Bind.list_active_binds()
            print("List available binds")
            Bind.list_available_binds()
            choice = input("Enter your choice: ")

            if choice == '1':
                key_combination = input("Enter key combination for the bind: ")
                function_name = input("Enter function name for the bind: ")
                Bind.add_bind(key_combination, function_name)

            elif choice == '2':
                key_combination = input("Enter key combination of the bind to remove: ")
                Bind.remove_bind(key_combination)

            elif choice == '3':
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all()
        for stream in streams:
            stream.stop()

