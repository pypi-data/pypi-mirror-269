from typing import Literal

from odds.the_odds_api.utils.classes import MLBKeyMapping
from odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport


class TheOddsOddsApiMLBWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.MLB
    player_prop_markets: list[
        Literal[
            "batter_home_runs",
            "batter_hits",
            "batter_total_bases",
            "batter_rbis",
            "batter_runs_scored",
            "batter_hits_runs_rbis",
            "batter_singles",
            "batter_doubles",
            "batter_triples",
            "batter_walks",
            "batter_strikeouts",
            "batter_stolen_bases",
            "pitcher_strikeouts",
            "pitcher_record_a_win",
            "pitcher_hits_allowed",
            "pitcher_walks",
            "pitcher_earned_runs",
            "pitcher_outs",
        ]
    ] = [
        "batter_home_runs",
        "batter_hits",
        "batter_total_bases",
        "batter_rbis",
        "batter_runs_scored",
        "batter_hits_runs_rbis",
        "batter_singles",
        "batter_doubles",
        "batter_triples",
        "batter_walks",
        "batter_strikeouts",
        "batter_stolen_bases",
        "pitcher_strikeouts",
        "pitcher_record_a_win",
        "pitcher_hits_allowed",
        "pitcher_walks",
        "pitcher_earned_runs",
        "pitcher_outs",
    ]
    key_map: MLBKeyMapping = {
        "batter_home_runs": "HR",
        "batter_hits": "H",
        "batter_total_bases": "TB",
        "batter_rbis": "RBI",
        "batter_runs_scored": "R",
        "batter_hits_runs_rbis": "H+R+RBI",
        "batter_singles": "1B",
        "batter_doubles": "2B",
        "batter_triples": "3B",
        "batter_walks": "BB",
        "batter_strikeouts": "K",
        "batter_stolen_bases": "SB",
        "pitcher_strikeouts": "K",
        "pitcher_record_a_win": "W",
        "pitcher_hits_allowed": "H",
        "pitcher_walks": "BB",
        "pitcher_earned_runs": "ERA",
        "pitcher_outs": "O",
    }
