import time
from typing import Union

import midiscripter.base.port_base
import midiscripter.base.shared
from midiscripter.logger import log
from midiscripter.base.msg_base import Msg


class MetronomeIn(midiscripter.base.port_base.Input):
    """The input port that sends messages with set interval."""

    def __init__(self, bpm: Union[float, int], msg_to_send: 'Msg' = Msg('Click')):
        """
            Args:
                bpm: Message sending interval in beats per minute
                msg_to_send: Message that the port will send
        """
        super().__init__(bpm)
        self.__interval_sec = 60 / bpm
        self.msg_to_send = msg_to_send
        self.msg_to_send.source = self

    @property
    def bpm(self) -> float:
        """Message sending interval in beats per minute."""
        return self.__interval_sec * 60

    @bpm.setter
    def bpm(self, bpm: float):
        self.__interval_sec = 60 / bpm

    def _open(self):
        self.is_enabled = True
        midiscripter.base.shared.thread_executor.submit(self.__send_clicks_worker)
        log(f'Started metronome at {self.bpm} bpm')

    def __send_clicks_worker(self):
        while self.is_enabled:
            time.sleep(self.__interval_sec)
            self.msg_to_send.ctime = midiscripter.base.shared.precise_epoch_time()
            self._send_input_msg_to_calls(self.msg_to_send)

    def _close(self):
        self.is_enabled = False
        log(f'Stopped metronome at {self.bpm} bpm')
