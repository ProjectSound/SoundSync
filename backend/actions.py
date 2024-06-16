from backend.global_state_manager import GlobalStateManager
from backend.logger import Logger


class Actions:
    def __init__(self, core, audio_controller, cutoff, input_manager, debug):
        self.core = core
        self.audio_controller = audio_controller
        self.cutoff = cutoff
        self.input_manager = input_manager
        self.debug = debug
        self.state_manager = GlobalStateManager()
        self.logger = Logger()
        self.is_manually_muted = False
        self.is_input1_disabled = False
        self.is_input2_disabled = False
        self.actions = {
            0: {"MUTE CONTROLLED APP": self.mute_controlled_app},
            1: {"START / STOP APP": self.toggle_app_running},
            2: {"DISABLE INPUT 1": self.disable_first_input},
            3: {"DISABLE INPUT 2": self.disable_second_input},
            4: {"CUTOFF MODE HARD": self.set_hard_mode},
            5: {"CUTOFF MODE FADE": self.set_fade_mode},
            6: {"MUTE / UNMUTE": self.set_mute_unmute},
            7: {"HARD CUT + FADE UP": self.set_hard_fade_mode},
            8: {"FADE DOWN + HARD UP": self.set_fade_hard_mode},
            9: {"MUTE + FADE UP": self.set_mute_fade_mode},
            10: {"MUTE + HARD UP": self.set_mute_hard_mode}
        }

    def get_actions(self):
        return self.actions

    def mute_controlled_app(self):
        if self.is_manually_muted:
            self.audio_controller.unmute()
        else:
            self.audio_controller.mute()
        self.is_manually_muted = not self.is_manually_muted

    def is_muted(self):
        return self.is_manually_muted

    def toggle_app_running(self):
        try:
            if self.state_manager.running:
                self.state_manager.running = False
            else:
                self.state_manager.running = True
        except Exception as e:
            print(e)

    def disable_first_input(self):
        primary_input_id = self.input_manager.get_primary()
        secondary_input_id = self.input_manager.get_secondary()
        if primary_input_id is None:
            return

        if not self.state_manager.running:
            return

        self.is_input1_disabled = not self.input_manager.is_enabled(primary_input_id)

        if self.is_input1_disabled:
            self.input_manager.start(primary_input_id)
            self.input_manager.set_enabled(primary_input_id, True)
        else:
            self.input_manager.stop(primary_input_id)
            self.input_manager.set_enabled(primary_input_id, False)

            if ((secondary_input_id is None and
                 self.input_manager.inputs[self.input_manager.get_primary()].threshold_exceeded) or
                    (secondary_input_id is not None and
                     (not self.input_manager.inputs[self.input_manager.get_secondary()].threshold_exceeded and
                      self.input_manager.inputs[self.input_manager.get_primary()].threshold_exceeded))):
                self.input_manager.inputs[self.input_manager.get_primary()].threshold_exceeded = False
                self.cutoff.run()
                if self.debug:
                    print("Threshold changed due to primary input being disabled")
                self.logger.log("Actions", "Threshold changed due to primary input being disabled")

    def disable_second_input(self):
        secondary_input_id = self.input_manager.get_secondary()
        if secondary_input_id is None:
            return

        if not self.state_manager.running:
            return

        self.is_input2_disabled = not self.input_manager.is_enabled(secondary_input_id)

        if self.is_input2_disabled:
            self.input_manager.start(secondary_input_id)
            self.input_manager.set_enabled(secondary_input_id, True)
        else:
            self.input_manager.stop(secondary_input_id)
            self.input_manager.set_enabled(secondary_input_id, False)

            if (not self.input_manager.inputs[self.input_manager.get_primary()].threshold_exceeded and
                    self.input_manager.inputs[self.input_manager.get_secondary()].threshold_exceeded):
                self.input_manager.inputs[self.input_manager.get_secondary()].threshold_exceeded = False
                self.cutoff.run()
                if self.debug:
                    print("Threshold changed due to secondary input being disabled")
                self.logger.log("Actions", "Threshold changed due to secondary input being disabled")

    def set_hard_mode(self):
        self.cutoff.apply(0)

    def set_fade_mode(self):
        self.cutoff.apply(1)

    def set_mute_unmute(self):
        self.cutoff.apply(2)

    def set_hard_fade_mode(self):
        self.cutoff.apply(3)

    def set_fade_hard_mode(self):
        self.cutoff.apply(4)

    def set_mute_hard_mode(self):
        self.cutoff.apply(5)

    def set_mute_fade_mode(self):
        self.cutoff.apply(6)
