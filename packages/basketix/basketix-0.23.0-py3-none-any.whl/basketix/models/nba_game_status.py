"""NBA game status"""

from enum import Enum


class NbaGameStatus(str, Enum):
    UNPLAYED = 'unplayed'
    UNSTARTED = 'unstarted'
    INPROGRESS = 'inProgress'
    FINISHED = 'finished'

    @classmethod
    def match(cls, status_number: int) -> 'NbaGameStatus':
        if status_number == 0: return cls.UNPLAYED
        if status_number == 1: return cls.UNSTARTED
        if status_number == 2: return cls.INPROGRESS
        if status_number == 3: return cls.FINISHED
        return cls.UNSTARTED

    @classmethod
    def is_started(cls, status: "NbaGameStatus") -> bool:
        return status in (cls.FINISHED, cls.INPROGRESS)

    @classmethod
    def is_finished(cls, status: "NbaGameStatus") -> bool:
        return status in (cls.FINISHED, cls.UNPLAYED)

NbaGameStatusType = NbaGameStatus
