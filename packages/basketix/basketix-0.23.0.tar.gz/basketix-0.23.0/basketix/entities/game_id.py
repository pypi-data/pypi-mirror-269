from .basketix_season import BasketixSeason


class GameId:

    def __init__(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return self._value

    def __eq__(self, other):
        return self._value == other._value

    @property
    def league(self) -> int:
        return int(self._value[0:2])

    @property
    def league_enum(self) -> str:
        if self.league == 0:
            return "NBA"

        raise ValueError(f"Unknown league {self.league}")

    @property
    def stage(self) -> int:
        return int(self._value[2])

    @property
    def stage_enum(self) -> str:
        if self.stage == 2:
            return "REGULAR"
        if self.stage == 3:
            return "ALL_STAR"
        if self.stage == 4:
            return "PLAYOFF"

        raise ValueError(f"Unknown stage {self.stage}")

    @property
    def is_playoff(self) -> int:
        return self.stage == 4

    @property
    def season(self) -> int:
        return int(self._value[3:5])

    @property
    def season_basketix(self) -> BasketixSeason:
        first_year_of_the_season = int(f"20{self.season}") - 1
        return BasketixSeason(f"{first_year_of_the_season}-{self.season}")

    @property
    def index(self) -> int:
        return int(self._value[5:])
