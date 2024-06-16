import threading
import time

from backend.audio_core import SoundManager
from backend.config import Config
from backend.logger import Logger


class CutOff:
    def __init__(self, sound_manager, debug):
        self.config = Config()
        self.sound_manager = sound_manager
        self.debug = debug
        self.normal_level = self.config.normal_sound_level / 100
        self.reduced_level = self.config.reduced_sound_level / 100
        self.duration = self.config.fade_duration
        self.is_muted = False
        self.is_faded = False
        self.is_running = False
        self.selected_mode_index = None
        self.logger = Logger()
        self.volume_lock = False
        self.previous_process = self.sound_manager.process_name
        self.should_cutoff_run = False

    def set(self, index):
        self.selected_mode_index = index

    def apply(self, index):
        self.set(index)
        self.config.selectedCutoff = index
        self.config.save()

        message = ""

        if self.selected_mode_index == 0:
            message = "Changed to hard"
        elif self.selected_mode_index == 1:
            message = "Changed to fade"
        elif self.selected_mode_index == 2:
            message = "Changed to mute / unmute"
        elif self.selected_mode_index == 3:
            message = "Changed to hard down / fade up"
        elif self.selected_mode_index == 4:
            message = "Changed to fade down / hard up"
        elif self.selected_mode_index == 5:
            message = "Changed to mute / fade up"
        elif self.selected_mode_index == 6:
            message = "Changed to mute / hard up"
        else:
            message = "Selected incorrect index"
            raise Exception('Incorrect index')

        if self.debug:
            print(message)
        self.logger.log("Cutoff", message)

    def run(self):
        if self.selected_mode_index is None:
            if self.debug:
                print("No mode selected")
            self.logger.log("Cutoff", "No mode selected")
            raise Exception('Cutoff index not selected')

        self.duration = self.config.fade_duration
        self.normal_level = self.config.normal_sound_level / 100
        self.reduced_level = self.config.reduced_sound_level / 100

        if self.selected_mode_index == 0:
            self.hard()
        elif self.selected_mode_index == 1:
            self.fade()
        elif self.selected_mode_index == 2:
            self.mute_unmute()
        elif self.selected_mode_index == 3:
            self.hard_cut_fade_up()
        elif self.selected_mode_index == 4:
            self.fade_down_hard_up()
        elif self.selected_mode_index == 5:
            self.mute_fade_up()
        elif self.selected_mode_index == 6:
            self.mute_hard_up()
        else:
            if self.debug:
                print("Tried to run incorrect cutoff")
            self.logger.log("Cutoff", "Tried to run incorrect cutoff")
            raise Exception('Incorrect index')

    def set_threshold_reached(self, threshold):
        self.sound_manager.set_threshold_reached(threshold)

    def hard(self):
        if self.is_faded:
            self.sound_manager.set_volume(self.normal_level)
        else:
            self.sound_manager.set_volume(self.reduced_level)
        self.is_faded = not self.is_faded

    def fade(self):
        if self.volume_lock:
            self.should_cutoff_run = True
            return

        if self.is_faded:
            self.fade_audio(self.normal_level)
        else:
            self.fade_audio(self.reduced_level)
        self.is_faded = not self.is_faded

    def mute_unmute(self):
        if self.is_muted:
            self.sound_manager.unmute()
        else:
            self.sound_manager.mute()
        self.is_muted = not self.is_muted

    def hard_cut_fade_up(self):
        if self.is_faded:
            self.fade_audio(self.normal_level)
        else:
            self.sound_manager.set_volume(self.reduced_level)
        self.is_faded = not self.is_faded

    def fade_down_hard_up(self):
        if self.is_faded:
            self.sound_manager.set_volume(self.normal_level)
        else:
            self.fade_audio(self.reduced_level)
        self.is_faded = not self.is_faded

    def mute_fade_up(self):
        if not self.is_muted:
            self.sound_manager.set_volume(0)
            self.sound_manager.mute()
        else:
            self.sound_manager.unmute()
            self.fade_audio(self.normal_level)
        self.is_muted = not self.is_muted

    def mute_hard_up(self):
        if not self.is_muted:
            self.sound_manager.set_volume(0)
            self.sound_manager.mute()
        else:
            self.sound_manager.unmute()
            self.sound_manager.set_volume(self.normal_level)
        self.is_muted = not self.is_muted

    def fade_audio(self, target_level):
        if not self.volume_lock or self.previous_process != self.sound_manager.process_name:
            sound_manager = SoundManager(self.sound_manager.process_name)
            fade_thread = FadeThread(sound_manager, target_level, self.duration, self)
            fade_thread.start()

        if self.previous_process == self.sound_manager.process_name:
            self.volume_lock = True
        else:
            self.previous_process = self.sound_manager.process_name

    def check_if_cutoff_should_run(self):
        if self.should_cutoff_run:
            self.fade()
            self.should_cutoff_run = False


class FadeThread(threading.Thread):
    def __init__(self, sound_manager, target_level, duration, cutoff_instance):
        super().__init__()
        self.sound_manager = sound_manager
        self.target_level = target_level
        self.duration = duration
        self.cutoff_instance = cutoff_instance

    def run(self):
        current_level = self.sound_manager.process_volume()
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            if elapsed > self.duration:
                break
            new_level = current_level + (self.target_level - current_level) * (elapsed / self.duration)
            self.sound_manager.set_volume(new_level)
            time.sleep(0.01)
        self.sound_manager.set_volume(self.target_level)
        self.cutoff_instance.volume_lock = False
        self.cutoff_instance.check_if_cutoff_should_run()
