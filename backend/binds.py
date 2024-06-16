import keyboard

from backend.config import Config
from backend.logger import Logger


class Binds:
    def __init__(self, actions, debug):
        self.config = Config()
        self.logger = Logger()
        self.actions = actions
        self.debug = debug
        self.hotkeys_to_load = self.config.key_actions
        self.registered_hotkeys = {}
        self.loaded_hotkeys = {}

    def add(self, hotkey, action) -> bool:
        try:
            if self.debug:
                print(f"Adding hotkey: {hotkey}")
            keyboard.add_hotkey(hotkey, action)
            self.registered_hotkeys[hotkey] = action
        except Exception as e:
            if self.debug:
                print(f"Error while adding hotkey: {e}")
            self.logger.log("Binds", f"Error while adding hotkey: {e}")
            return False

        return True

    def get(self):
        return self.loaded_hotkeys

    def push(self, hotkey, action):
        if self.debug:
            print(f"Pushing new bind: {hotkey}, {action}")
        self.logger.log("Binds", f"Pushing new bind: {hotkey}, {action}")
        self.hotkeys_to_load[hotkey] = action
        self.config.key_actions[hotkey] = action
        self.load(True)
        self.config.save()

    def remove(self, key_index):
        try:
            for index, value in self.loaded_hotkeys.items():
                if index == key_index:
                    key, search_action = next(iter(value.items()))
                    if self.debug:
                        print(f"Removing hotkey: {key}")
                    self.logger.log("Binds", f"Removing hotkey: {key}")
                    keyboard.remove_hotkey(key)
                    del self.registered_hotkeys[key]
                    del self.loaded_hotkeys[index]
                    del self.config.key_actions[key]
                    self.config.save()
                    break
        except Exception as e:
            if self.debug:
                print(f"Error while removing hotkey: {e}")
            self.logger.log("Binds", f"Error while removing hotkey: {e}")

    def load(self, new=False):
        try:
            for combination, hotkeyAction in self.hotkeys_to_load.items():
                for key, action_info in self.actions.actions.items():
                    name, method = next(iter(action_info.items()))
                    if name == hotkeyAction:
                        result = self.add(combination, method)
                        if result:
                            if self.loaded_hotkeys:
                                last_key, last_value = next(reversed(self.loaded_hotkeys.items()))
                            else:
                                last_key = -1
                            self.loaded_hotkeys[last_key + 1] = {combination: name}
            if not new:
                if self.debug:
                    print(f"Loaded all binds, count: {len(self.loaded_hotkeys)}")
                self.logger.log("Binds", f"Loaded all binds, count: {len(self.loaded_hotkeys)}")
        except Exception as e:
            if not new:
                if self.debug:
                    print(f"Failed to load all binds: {e}")
                self.logger.log("Binds", f"Failed to load all binds: {e}")
            else:
                if self.debug:
                    print(f"Failed to load bind: {e}")
                self.logger.log("Binds", f"Failed to load bind: {e}")
        self.hotkeys_to_load = {}

    def clear(self):
        try:
            for hotkey in self.registered_hotkeys.keys():
                keyboard.remove_hotkey(hotkey)
            self.registered_hotkeys = {}
            self.loaded_hotkeys = {}
            self.config.key_actions = {}
            self.config.save()
            if self.debug:
                print("Cleared all hotkeys")
            self.logger.log("Binds", "Cleared all hotkeys")
        except Exception as e:
            if self.debug:
                print(f"Error while clearing all hotkeys: {e}")
            self.logger.log("Binds", f"Error while clearing all hotkeys: {e}")
