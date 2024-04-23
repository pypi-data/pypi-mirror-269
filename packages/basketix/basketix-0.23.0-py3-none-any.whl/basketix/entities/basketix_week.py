"""Week id module"""

from datetime import datetime
from typing import List, Type

from isoweek import Week
from typing_extensions import Self

from ..helpers.date_helper import DateHelper
from .basketix_season import BasketixSeason
from .game_id import GameId


class BasketixWeek:
    """Basketix week class"""

    SEPARATOR = "_"
    WEEK_MODE = {
        "REGULAR": "REGULAR",
        "PO": "PLAYOFF",
    }

    def __init__(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Basketix week: {self._value}"

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other):
        return self.first_day == other.first_day and self.mode == other.mode

    def __gt__(self, other):
        return self.first_day > other.first_day

    def __ge__(self, other):
        return self.first_day >= other.first_day

    def __lt__(self, other):
        return self.first_day < other.first_day

    def __le__(self, other):
        return self.first_day <= other.first_day

    def __call__(self):
        return self.id

    @property
    def id(self) -> str:
        """Returns week id"""

        return self._value

    @property
    def year(self) -> int:
        """Returns week year"""

        return int(self._value.split(self.SEPARATOR)[0])

    @property
    def week_number(self) -> int:
        """Returns week number"""

        return int(self._value.split(self.SEPARATOR)[1])

    @property
    def mode(self) -> str:
        """Returns week mode"""

        splitted = self._value.split(self.SEPARATOR)
        if len(splitted) == 3:
            return self.WEEK_MODE[splitted[2]]

        return self.WEEK_MODE["REGULAR"]

    @property
    def days(self) -> List[str]:
        """Returns all days of a week."""

        return [day.strftime(DateHelper.DATE_ISO_FORMAT) for day in Week(self.year, self.week_number).days()]

    @property
    def first_day(self) -> str:
        """Returns first days of a week as string"""

        return self.days[0]

    @property
    def last_day(self) -> str:
        """Returns last days of a week as string"""

        return self.days[-1]

    @property
    def season(self) -> BasketixSeason:
        """Returns all days of a week."""

        first_day_of_week = self.days[0]

        return BasketixSeason.from_date(first_day_of_week)

    def next(self, delta=1) -> Self:
        """Returns next delta week"""

        date = DateHelper.delta_days(self.first_day, days=7 * delta)

        return self.from_date(date=date)

    def previous(self, delta=1) -> Self:
        """Returns previous delta week"""

        date = DateHelper.delta_days(self.first_day, days=-7 * delta)

        return self.from_date(date=date)

    def to_playoff(self) -> Self:
        new_id = self.id + self.SEPARATOR + "PO"
        return self.__class__(new_id)

    @classmethod
    def from_date(cls: Type["Self"], date: str) -> Self:
        """Parses date and returns Week instance"""

        parse_date = datetime.strptime(date, DateHelper.DATE_ISO_FORMAT)
        year, week_number, _ = parse_date.isocalendar()

        week_id = f"{year}_{week_number:02d}"

        return cls(value=week_id)

    @classmethod
    def from_date_and_game_id(cls: Type["Self"], date: str, game_id: GameId) -> Self:
        """Parses date and returns Week instance"""

        week = cls.from_date(date=date)

        if game_id.is_playoff:
            week = week.to_playoff()

        return week
