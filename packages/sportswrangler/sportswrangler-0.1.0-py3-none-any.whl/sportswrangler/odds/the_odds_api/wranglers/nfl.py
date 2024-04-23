from typing import Literal

from odds.the_odds_api.utils.classes import NFLKeyMapping
from odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport


class TheOddsOddsApiNFLWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.NFL
    player_prop_markets: list[
        Literal[
            "player_pass_tds",
            "player_pass_yds",
            "player_pass_completions",
            "player_pass_attempts",
            "player_pass_interceptions",
            "player_pass_longest_completion",
            "player_rush_yds",
            "player_rush_attempts",
            "player_rush_longest",
            "player_receptions",
            "player_reception_yds",
            "player_reception_longest",
            "player_kicking_points",
            "player_field_goals",
            "player_tackles_assists",
            "player_1st_td",
            "player_last_td",
            "player_anytime_td",
        ]
    ] = [
        "player_pass_tds",
        "player_pass_yds",
        "player_pass_completions",
        "player_pass_attempts",
        "player_pass_interceptions",
        "player_pass_longest_completion",
        "player_rush_yds",
        "player_rush_attempts",
        "player_rush_longest",
        "player_receptions",
        "player_reception_yds",
        "player_reception_longest",
        "player_kicking_points",
        "player_field_goals",
        "player_tackles_assists",
        "player_1st_td",
        "player_last_td",
        "player_anytime_td",
    ]
    key_map: NFLKeyMapping = {
        "player_pass_tds": "TD",
        "player_pass_yds": "YDS",
        "player_pass_completions": "COM",
        "player_pass_attempts": "ATT",
        "player_pass_interceptions": "INT",
        "player_pass_longest_completion": "LNG",
        "player_rush_yds": "YDS",
        "player_rush_attempts": "ATT",
        "player_rush_longest": "LNG",
        "player_receptions": "REC",
        "player_reception_yds": "YDS",
        "player_reception_longest": "LNG",
        "player_kicking_points": "P",
        "player_field_goals": "FG",
        "player_tackles_assists": "TOT",
        "player_1st_td": "FTD",
        "player_last_td": "LTD",
        "player_anytime_td": "ATD",
    }
