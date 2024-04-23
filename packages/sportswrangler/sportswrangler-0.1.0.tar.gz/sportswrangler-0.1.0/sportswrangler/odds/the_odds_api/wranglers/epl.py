from datetime import datetime

from odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport


class TheOddsOddsApiEPLWrangler(TheOddsApiWrangler):
    """Player props are currently not available from this odds' provider. Calling functions which would typically
    return player prop odds will raise a ``NotImplementedError``"""

    sport: Sport = Sport.EPL

    def get_all_event_odds(
        self,
        event_id: str = None,
        standardize: bool = True,
        starting_after: datetime = None,
    ):
        """
        Gets all odds available for an event using ``get_player_prop_odds`` & ``get_additional_markets_event_odds``

        - If ``event_id`` is provided, only odds for that event are returned
        - If ``starting_after`` is provided, odds for applicable events are returned
        NOTE: ``event_id`` takes precedence over ``starting_after``
        :param event_id: event id to get odds for
        :param standardize: if this is False, the results per event will not be sent to ``standardize_odds``
        :param starting_after: datetime that will be passed to ``get_events``
        """
        events = (
            [event_id] if event_id else self.get_events(starting_after=starting_after)
        )
        dfs = [
            (
                self.standardize_odds(
                    self.get_additional_markets_event_odds(event_id=event)
                )
                if standardize
                else self.get_additional_markets_event_odds(event_id=event)
            )
            for event in events
        ]
        return self.merge_dfs(dfs)

    def get_player_prop_odds(self, event_id: str):
        raise NotImplementedError(
            "This league currently does not support player prop odds."
        )

    def get_all_player_prop_odds(
        self, standardize: bool = True, starting_after: datetime = None
    ):
        raise NotImplementedError(
            "This league currently does not support player prop odds."
        )
