import sys
import datetime
import uuid

import numpy as np
from pycaw.pycaw import AudioUtilities
import sounddevice as sd

from backend.config import Config
from backend.logger import Logger


class SoundManager:
    def __init__(self, process_name):
        self.config = Config()
        self.process_name = process_name
        self.last_process_name = self.process_name
        self.volume = self.process_volume()
        self.threshold_reached = False
        self.run = None

    def set_cutoff_run(self, run):
        self.run = run

    def set_threshold_reached(self, threshold):
        self.threshold_reached = threshold

    def update_process(self):
        self.last_process_name = self.process_name
        if (self.config.selectedApp != self.last_process_name) and self.threshold_reached:
            self.run()
            self.process_name = self.config.selectedApp
            self.run()
        else:
            self.process_name = self.config.selectedApp

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                # print(self.process_name, "has been muted.")  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                # print(self.process_name, "has been unmuted.")  # debug

    def process_volume(self) -> float:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # print("Volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels: float) -> None:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                # print("Volume set to", self.volume)  # debug


class InputDeviceManager:
    def __init__(self):
        devices = sd.query_devices()
        input_devices = [device for device in devices if device['hostapi'] == 0 and device['max_input_channels'] > 0]

        self.full_name_inputs = []
        for device in devices:
            for input_device in input_devices:
                if input_device['name'] in device['name'] and device['hostapi'] == 1:
                    input_device['name'] = device['name']
                    self.full_name_inputs.append(input_device)
                    break

    def get_input_devices(self):
        return self.full_name_inputs


class AudioSessionManager:
    def __init__(self):
        self.config = Config()
        self.selectedAppKey = None
        self.apps = {}
        self.lastApps = None

    def list_applications(self) -> dict:
        sessions = AudioUtilities.GetAllSessions()

        self.apps = {}

        for index, session in enumerate(sessions):
            if session.Process:
                app_name = session.Process.name().replace(".exe", "")
                if app_name not in self.apps.values():
                    app_id = str(uuid.uuid4())
                    self.apps[app_id] = app_name
                    if str(app_name + ".exe") == self.config.selectedApp:
                        self.selectedAppKey = app_id

        if self.lastApps is None:
            self.lastApps = self.apps

        if sorted(self.apps.values()) != sorted(self.lastApps.values()):
            for app_id, app_name in self.lastApps.items():
                if app_name not in self.apps.values():
                    del self.lastApps[app_id]
                    break

            for app_id, app_name in self.apps.items():
                if app_name not in self.lastApps.values():
                    self.lastApps[app_id] = app_name

        return self.lastApps


class InputManager:
    def __init__(self, cutoff, debug):
        self.inputs = {}
        self.cutoff = cutoff
        self.debug = debug
        self.config = Config()
        self.primary_input = None
        self.secondary_input = None
        self.logger = Logger()

    def create(self, device, threshold, threshold_not_reached, is_primary):
        callback_handler = CallbackHandler()
        input_id = str(uuid.uuid4())
        callback_function = lambda indata, frames, time, status: \
            callback_handler.handle_callback(indata, frames, time, status, self.inputs, input_id, self.cutoff, self.debug)
        input = Input(device, threshold, threshold_not_reached, callback_function)
        self.inputs[input_id] = input
        if is_primary:
            self.primary_input = input_id
        else:
            self.secondary_input = input_id
        self.logger.log("InputManager", f"Created input {input_id}")
        if self.debug:
            print(f"Created input {input_id}")

    def start(self, input_id):
        if input_id in self.inputs.keys():
            self.inputs[input_id].start()

    def start_all(self):
        for input in self.inputs.values():
            input.start()

    def stop(self, input_id):
        if input_id in self.inputs.keys():
            self.inputs[input_id].stop()

    def stop_all(self):
        for input in self.inputs.values():
            input.stop()

    def remove(self, input_id):
        if input_id in self.inputs.keys():
            self.inputs[input_id].stop()
            del self.inputs[input_id]
            if self.debug:
                print(f"Destroyed input {input_id}")
            self.logger.log("InputManager", f"Destroyed input {input_id}")
            if input_id == self.primary_input:
                self.primary_input = None

            if input_id == self.secondary_input:
                self.secondary_input = None

    def get_primary(self):
        if self.primary_input is not None:
            return self.primary_input

    def get_secondary(self):
        if self.secondary_input is not None:
            return self.secondary_input

    def set_enabled(self, input_id, status):
        if input_id in self.inputs.keys():
            self.inputs[input_id].is_enabled = status

    def is_active(self, input_id):
        if input_id in self.inputs.keys():
            return self.inputs[input_id].is_active

    def is_enabled(self, input_id):
        if input_id in self.inputs.keys():
            return self.inputs[input_id].is_enabled

    def change_device(self, input_id):
        if input_id in self.inputs.keys():
            if self.debug:
                print(f"Changed device for input {input_id}")
            self.logger.log("InputManager", f"Changed device for input {input_id}")
            if input_id == self.primary_input:
                self.inputs[input_id].change_device(self.config.selectedInput1)
            elif input_id == self.secondary_input:
                self.inputs[input_id].change_device(self.config.selectedInput2)

    def swap_inputs(self):
        temp_input_device = self.inputs[self.primary_input].device
        self.inputs[self.primary_input].change_device(self.inputs[self.secondary_input].device)
        self.config.selectedInput1 = self.config.selectedInput2
        self.inputs[self.secondary_input].change_device(temp_input_device)
        self.config.selectedInput2 = temp_input_device
        if self.debug:
            print(f"Swapped devices")
        self.logger.log("InputManager", f"Swapped devices")
        self.config.save()

    def update(self):
        self.inputs[self.primary_input].threshold = self.config.threshold1
        self.inputs[self.primary_input].threshold_not_reached = self.config.threshold_not_reached1
        if self.secondary_input is not None:
            self.inputs[self.secondary_input].threshold = self.config.threshold2
            self.inputs[self.secondary_input].threshold_not_reached = self.config.threshold_not_reached2
        if self.debug:
            print(f"Inputs updated")
        self.logger.log("InputManager", f"Inputs updated")


class CallbackHandler:
    @staticmethod
    def handle_callback(indata, frames, time, status, inputs, input_id, cutoff, debug):
        if status:
            print(status, file=sys.stderr)

        amplitude = np.max(indata)

        if amplitude == 3.0517578125e-05:
            amplitude = 0

        if amplitude * 100 >= inputs[input_id].threshold:
            if not inputs[input_id].threshold_exceeded:
                inputs[input_id].threshold_exceeded = True
                inputs[input_id].start_time = datetime.datetime.now()
                if debug:
                    print(f"Threshold reached for stream {input_id}: {inputs[input_id].threshold_not_reached}")
                cutoff.set_threshold_reached(True)
                one_reached = False
                for key, stream_state in inputs.items():
                    if stream_state.threshold_exceeded and key != input_id:
                        one_reached = True
                        break

                if not one_reached:
                    cutoff.run()
            else:
                inputs[input_id].start_time = datetime.datetime.now()
            return

        if inputs[input_id].threshold_exceeded:
            current_time = datetime.datetime.now()
            elapsed_time = (current_time - inputs[input_id].start_time).total_seconds()
            remaining_time = inputs[input_id].threshold_not_reached - elapsed_time
            if remaining_time <= 0:
                inputs[input_id].threshold_exceeded = False
                if debug:
                    print(f"Threshold not reached for stream {input_id}")

                all_not_reached = True
                for stream_state in inputs.values():
                    if stream_state.threshold_exceeded:
                        all_not_reached = False
                        break

                if all_not_reached:
                    if debug:
                        print("All thresholds not reached!")
                    cutoff.set_threshold_reached(False)
                    cutoff.run()


class Input:
    def __init__(self, device, threshold, threshold_not_reached, callback_function):
        self.device = device
        self.threshold = threshold
        self.threshold_not_reached = threshold_not_reached
        self.is_enabled = True
        self.is_active = False
        self.callback_function = callback_function

        self.stream = None
        self.create_stream()

        self.threshold_exceeded = None
        self.start_time = None
        self.remaining_time = None

    def create_stream(self):
        if self.stream is None:
            # HIGHER LATENCY DONT CAUSE PROBLEMS WITH INPUT OVERFLOW
            self.stream = sd.InputStream(device=self.device, latency=10, callback=self.callback_function)

    def remove_stream(self):
        if self.stream is not None:
            self.stop()
            self.stream = None

    def change_device(self, device):
        if device is not None:
            self.remove_stream()
            self.device = device
            self.is_active = True
            self.create_stream()
            if self.is_enabled:
                self.start()

    def start(self):
        if self.stream:
            self.stream.start()
            self.is_active = True

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.is_active = False
