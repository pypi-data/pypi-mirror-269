"""NBA player injury module"""

from enum import Enum


class InjuryType(str, Enum):
    PROBABLE = "PROBABLE"
    DOUBTFUL = "DOUBTFUL"
    QUESTIONABLE = "QUESTIONABLE"
    OUT_NEXT_GAME = "OUT_NEXT_GAME"
    OUT_LAST_GAME = "OUT_LAST_GAME"
    OUT = "OUT"
    OUT_INDEFINITELY = "OUT_INDEFINITELY"
    OUT_FOR_SEASON = "OUT_FOR_SEASON"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def parse(cls, injury_text) -> "InjuryType":
        """Converts Basket-Reference note into a InjuryType"""
        raw_injury_type, injury_detail = injury_text.split(" - ")

        injury_detail = injury_detail.upper()
        raw_injury_type = raw_injury_type.upper()

        if "OUT FOR SEASON" in raw_injury_type:
            return cls.OUT_FOR_SEASON

        if "PROBABLE" in injury_detail:
            return InjuryType.PROBABLE

        if "QUESTIONABLE" in injury_detail:
            return InjuryType.QUESTIONABLE

        if "DOUBTFUL" in injury_detail:
            return InjuryType.DOUBTFUL

        if "DID NOT PLAY IN" in injury_detail:
            return InjuryType.OUT_LAST_GAME

        if "OUT FOR" in injury_detail:
            return InjuryType.OUT_NEXT_GAME

        if "INDEFINITELY" in injury_detail:
            return InjuryType.OUT_INDEFINITELY

        if "WITHOUT A TIMETABLE TO RETURN" in injury_detail:
            return InjuryType.OUT_INDEFINITELY

        if "NO TIMETABLE TO RETURN" in injury_detail:
            return InjuryType.OUT_INDEFINITELY

        if "OUT" in raw_injury_type:
            return InjuryType.OUT

        return InjuryType.UNKNOWN
