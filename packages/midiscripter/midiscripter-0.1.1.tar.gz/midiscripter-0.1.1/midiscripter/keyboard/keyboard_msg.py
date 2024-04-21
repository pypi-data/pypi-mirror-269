import pynput.keyboard

from typing import TYPE_CHECKING, Union, Iterable

import midiscripter.base.msg_base

if TYPE_CHECKING:
    from midiscripter.keyboard.keyboard_port import KeyIn


MODIFIER_KEYS = {pynput.keyboard.Key.alt, pynput.keyboard.Key.cmd, pynput.keyboard.Key.ctrl,
                 pynput.keyboard.Key.shift}


MODIFIER_KEYS_VARIATIONS = {pynput.keyboard.Key.alt_gr: pynput.keyboard.Key.alt,
                            pynput.keyboard.Key.alt_l: pynput.keyboard.Key.alt,
                            pynput.keyboard.Key.cmd_l: pynput.keyboard.Key.cmd,
                            pynput.keyboard.Key.cmd_r: pynput.keyboard.Key.cmd,
                            pynput.keyboard.Key.ctrl_l: pynput.keyboard.Key.ctrl,
                            pynput.keyboard.Key.ctrl_r: pynput.keyboard.Key.ctrl,
                            pynput.keyboard.Key.shift_l: pynput.keyboard.Key.shift,
                            pynput.keyboard.Key.shift_r: pynput.keyboard.Key.shift}


class KeyEventType(midiscripter.base.msg_base.AttrEnum):
    KEY_PRESS = 'KEY_PRESS'
    KEY_RELEASE = 'KEY_RELEASE'
    KEY_TAP = 'KEY_TAP'
    

class KeyMsg(midiscripter.base.msg_base.Msg):
    """TODO"""
    
    __match_args__ = ('type', 'description')
      
    keycodes: list[pynput.keyboard.Key]
    

    def __init__(self, type: KeyEventType, 
                 description_or_keycodes: Union[str, Iterable[pynput.keyboard.Key]],
                 *, source: 'KeyIn' = None):
        """
        Args:
            TODO
            source (KeyIn): The [`KeyIn`][midiscripter.KeyIn] instance that generated the message
        """
        super().__init__(type, source)
        self.__description_cache = ''
        self.__cached_keycodes = None
        
        if isinstance(description_or_keycodes, str):
            self.description = description_or_keycodes
        elif isinstance(description_or_keycodes, Iterable):
            self.keycodes = list(description_or_keycodes)
        
    @property
    def description(self) -> str:
        if self.__cached_keycodes != self.keycodes:            
            modifiers = []
            non_mod_keys = []
            for keycode in self.keycodes:
                keycode = MODIFIER_KEYS_VARIATIONS.get(keycode, keycode)
                if keycode in MODIFIER_KEYS:
                    modifiers.append(str(keycode))
                else:
                    non_mod_keys.append(str(keycode))
                    
            modifiers.sort()
            non_mod_keys.sort()
            key_strings = modifiers + non_mod_keys
            
            keys_descr = (key_str.rpartition(".")[-1].replace("'", '') for key_str in key_strings)
            combined_descr = '+'.join(keys_descr)
            
            self.__cached_keycodes = self.keycodes
            self.__description_cache = combined_descr
            
        return self.__description_cache

    @description.setter
    def description(self, key_desc: str):
        self.keycodes = []
        for key in key_desc.split('+'):
            if len(key) == 1:
                key = pynput.keyboard.KeyCode.from_char(key)
            else:
                key = getattr(pynput.keyboard.Key, key)
            self.keycodes.append(key)
    
    
    def matches(self, type=None, description=None):
        return super().matches(type, description)
