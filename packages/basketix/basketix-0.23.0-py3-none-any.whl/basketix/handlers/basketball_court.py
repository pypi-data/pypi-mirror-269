"""Basketball court handler"""

from ..models import BasketballCourtSettings, BasketixId, SeasonId
from ..tables import BasketixSeasonsTable


class BasketballCourtHandler:

    BLACK = "#000000"
    DEFAULT_COURT_COLOR = "#e6be91"
    DEFAULT_LINE_WIDTH = 3

    def __init__(self, environment: str) -> None:
        self.basketix_seasons_table = BasketixSeasonsTable(environment)


    def get(self, season_id: SeasonId, basketix_id: BasketixId) -> BasketballCourtSettings:
        season = self.basketix_seasons_table.get(season_id)

        if "courtSettings" in season["basketixs"][basketix_id]:
            return season["basketixs"][basketix_id]["courtSettings"]

        return self.default()

    def upsert(self, season_id: SeasonId, basketix_id: BasketixId, court_settings: BasketballCourtSettings) -> BasketballCourtSettings:
        """Update or insert court setting of a user"""
        season = self.basketix_seasons_table.get(season_id)

        court = self.default()
        if "courtSettings" in season["basketixs"][basketix_id]:
            court: BasketballCourtSettings = season["basketixs"][basketix_id]["courtSettings"]

        updated_court: BasketballCourtSettings = {**court, **court_settings} # type: ignore
        season["basketixs"][basketix_id]["courtSettings"] = updated_court
        self.basketix_seasons_table.update([season])

        return updated_court

    def default(self) -> BasketballCourtSettings:
        return {
            "backgroundColor": self.DEFAULT_COURT_COLOR,
            "courtColor": self.DEFAULT_COURT_COLOR,
            "linesColor": self.BLACK,
            "linesWidth": self.DEFAULT_LINE_WIDTH,
            "paintColor": self.DEFAULT_COURT_COLOR,
            "sidePaintColor": self.DEFAULT_COURT_COLOR,
            "threePointsColor": self.DEFAULT_COURT_COLOR,
        }
