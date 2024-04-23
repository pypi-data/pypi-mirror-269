from typing import Literal

from odds.the_odds_api.utils.classes import NBAKeyMapping
from odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport


class TheOddsOddsApiNBAWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.NBA
    _player_prop_markets: list[
        Literal[
            "player_points",
            "player_rebounds",
            "player_assists",
            "player_threes",
            "player_blocks",
            "player_steals",
            "player_turnovers",
            "player_blocks_steals",
            "player_points_rebounds_assists",
            "player_points_rebounds",
            "player_points_assists",
            "player_rebounds_assists",
            "player_first_basket",
            "player_double_double",
            "player_triple_double",
        ]
    ] = [
        "player_points",
        "player_rebounds",
        "player_assists",
        "player_threes",
        "player_blocks",
        "player_steals",
        "player_turnovers",
        "player_blocks_steals",
        "player_points_rebounds_assists",
        "player_points_rebounds",
        "player_points_assists",
        "player_rebounds_assists",
        "player_first_basket",
        "player_double_double",
        "player_triple_double",
    ]
    _player_prop_key_mapping: NBAKeyMapping = {
        "player_points": "PTS",
        "player_rebounds": "TRB",
        "player_assists": "AST",
        "player_threes": "3P",
        "player_blocks": "BLK",
        "player_steals": "STL",
        "player_turnovers": "TOV",
        "player_blocks_steals": "BLK_STL",
        "player_points_rebounds_assists": "PTS_TRB_AST",
        "player_points_rebounds": "PTS_TRB",
        "player_points_assists": "PTS_AST",
        "player_rebounds_assists": "TRB_AST",
        "player_first_basket": "FB",
        "player_double_double": "DD",
        "player_triple_double": "TD",
    }
