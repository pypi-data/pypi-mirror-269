import pathlib
from typing import TYPE_CHECKING, Union

import midiscripter.base.msg_base

if TYPE_CHECKING:
    from midiscripter.file_event.file_event_port import FileEventIn


class FileEventType(midiscripter.base.msg_base.AttrEnum):
    # Names are hardcoded, equal watchdog's event types
    MOVED = 'MOVED'
    DELETED = 'DELETED'
    CREATED = 'CREATED'
    MODIFIED = 'MODIFIED'
    CLOSED = 'CLOSED'
    OPENED = 'OPENED'


class FileEventMsg(midiscripter.base.msg_base.Msg):
    ___match_args__ = ('type', 'path')

    def __init__(self, type: Union[FileEventType, str], path: pathlib.Path,
                 *, source: 'FileEventIn' = None):
        super().__init__(type, source)
        self.type = type
        self.path = path

    def matches(self, type=None, path=None):
        return super().matches(type, path)
