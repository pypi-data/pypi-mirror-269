import pynput.keyboard

import midiscripter.base.port_base
import midiscripter.osc.osc_msg
from midiscripter.logger import log
from midiscripter.keyboard.keyboard_msg import KeyMsg, KeyEventType


class KeyIn(midiscripter.base.port_base.Input):
    """Keyboard input port. Produces [`KeyMsg`][midiscripter.KeyMsg] objects."""
    
    _force_uid = 'Keyboard In'

    def __init__(self):
        super().__init__(self._force_uid)
        self.pynput_listener = None
        self.pressed_keys = []
    
    def __on_press(self, key: pynput.keyboard.Key):
        if not self.is_enabled:
            return 
        
        if type(key) is pynput.keyboard.KeyCode:
            key = self.pynput_listener.canonical(key)
            
        if key not in self.pressed_keys:
            self.pressed_keys.append(key)
            
        msg = KeyMsg(KeyEventType.KEY_PRESS, self.pressed_keys.copy(), source=self)
        self._send_input_msg_to_calls(msg)
        
    def __on_release(self, key: pynput.keyboard.Key):    
        if not self.is_enabled:
            return 
        
        if type(key) is pynput.keyboard.KeyCode:
            key = self.pynput_listener.canonical(key)
       
        try:
            pressed_keys_for_msg = self.pressed_keys.copy()
            self.pressed_keys.remove(key)
            
            msg = KeyMsg(KeyEventType.KEY_RELEASE, pressed_keys_for_msg, source=self)
            self._send_input_msg_to_calls(msg)
        except ValueError:
            pass
        
    def _open(self):
        if self.pynput_listener:
            return 
        
        self.pynput_listener = pynput.keyboard.Listener(self.__on_press, self.__on_release)
        self.pynput_listener.start()
        self.pynput_listener.wait()
        self.is_enabled = True
        log(f'Started keyboard input listener')

    def _close(self):
        self.pynput_listener.stop()
        self.is_enabled = False
        log(f'Stopped keyboard input listener')


class KeyOut(midiscripter.base.port_base.Output):
    """Keyboard output port. Sends [`KeyMsg`][midiscripter.KeyMsg] objects."""

    _force_uid = 'Keyboard Output'
    
    def __init__(self):
        super().__init__(self._force_uid)
        self.pynput_controller = pynput.keyboard.Controller()
        
    def send(self, msg: KeyMsg):        
        """Send the keyboard input.

        Args:
            msg: object to send
        """   
        # Log messages sent before actual sending, so receive messages for sent keys 
        # won't be displayed before the message
        with self._check_and_log_sent_message(msg):
            pass
            
        if msg.type is KeyEventType.KEY_PRESS:
            for keycode in msg.keycodes:
                self.pynput_controller.press(keycode)
                
        elif msg.type is KeyEventType.KEY_RELEASE:
            for keycode in msg.keycodes:
                self.pynput_controller.release(keycode)
                
        elif msg.type is KeyEventType.KEY_TAP:
            for keycode in msg.keycodes:
                self.pynput_controller.press(keycode)
            for keycode in reversed(msg.keycodes):
                self.pynput_controller.release(keycode)
    
    def type_in(self, string_to_type: str):
        self.pynput_controller.type(string_to_type)
