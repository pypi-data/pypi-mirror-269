import logging
import os

import pandas as pd
import polars as pl
from requests import Response, Session

from sportswrangler.generic.wrangler import Wrangler
from sportswrangler.utils.enums import Sport

logger = logging.getLogger(__name__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class DataFeedsWrangler(Wrangler):
    _endpoint = "http://rest.datafeeds.rolling-insights.com"
    sport: Sport = None
    rsc_token: str = os.environ.get("DATA_FEEDS_RSC_TOKEN")
    """
    Token assigned to your account to make calls to DataFeeds
    """

    def request(self, url: str, additional_params=None) -> Response:
        """
        :param url: URL string to send a get query
        :param additional_params: dict of parameters to combine with RSC_token parameter
        """
        if additional_params is None:
            additional_params = {}
        logger.debug(
            "Sending a request to {} with the parameters {} \nNote: RSC token is intentionally left out of log message.".format(
                url, additional_params
            )
        )
        params = {"RSC_token": self.rsc_token, **additional_params}
        response = (
            self.session if isinstance(self.session, Session) else self.new_session()
        ).get(
            url=url,
            params=params,
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to get a response: status code {response.status_code}, response body {response.text}"
            )
        return response

    def base_request(
        self, api_path: str, additional_params=None, sports: list[Sport] = None
    ) -> dict[str, list] | dict[str, pd.DataFrame] | dict[str, pl.LazyFrame]:
        """
        :param sports: list of sports to parse into preferred dataframe
        :param api_path: path that will be appended to http://rest.datafeeds.rolling-insights.com/api/v1
        :param additional_params: dict of parameters to combine with RSC_token parameter
        """
        path = "http://rest.datafeeds.rolling-insights.com/api/v1"
        response = self.request(
            url=path + api_path,
            additional_params=additional_params or {},
        )
        data = response.json()["data"]
        if sports and self.preferred_dataframe:
            for sport in sports:
                data[sport] = (
                    pd.DataFrame(data[sport])
                    if self.preferred_dataframe == "pandas"
                    else pl.LazyFrame(data[sport])
                )
        return data

    def get_season_schedule(
        self, date: str = None, sports: list[Sport] = None, team_id: str = None
    ):
        api_path = "/schedule-season"
        additional_params = None
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params = {"team_id": team_id}
        return self.base_request(api_path, additional_params, sports)

    def get_weekly_schedule(
        self, date: str = "now", sports: list[Sport] = None, team_id: str = None
    ):
        api_path = "/schedule-week"
        additional_params = None
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params = {"team_id": team_id}
        return self.base_request(api_path, additional_params, sports)

    def get_daily_schedule(
        self,
        date: str = "now",
        sports: list[Sport] = None,
        team_id: str = None,
        game_id: str = None,
    ):
        api_path = "/schedule"
        additional_params = {}
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id
        if game_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `game_id` parameter."
                )
            additional_params["game_id"] = game_id

        return self.base_request(api_path, additional_params, sports)

    def get_live(
        self,
        date: str = "now",
        sports: list[Sport] = None,
        team_id: str = None,
        game_id: str = None,
    ):
        """

        :param date:  "now" or YYYY-MM-DD
        :param sports:
        :param team_id:
        :param game_id:
        :return:
        """
        api_path = "/live"
        additional_params = {}
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id
        if game_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `game_id` parameter."
                )
            additional_params["game_id"] = game_id

        return self.base_request(api_path, additional_params, sports)

    def get_team_info(
        self,
        sports: list[Sport] = None,
        team_id: str = None,
        from_assets: bool = True,
    ):
        if from_assets:
            data = {}
            for sport in sports:
                loaded = pd.read_csv(
                    os.path.join(__location__, "assets/{}/teams.csv".format(sport))
                )
                if team_id:
                    loaded = loaded[loaded["team_id" == team_id]]
                if self.preferred_dataframe != "pandas":
                    loaded = (
                        loaded.to_dict("records")
                        if not self.preferred_dataframe
                        else pl.LazyFrame(loaded)
                    )
                data[sport] = loaded
            return data
        api_path = "/team-info"
        additional_params = {}
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id
        return self.base_request(api_path, additional_params, sports)

    def get_team_season_stats(
        self,
        date: str = None,
        sports: list[Sport] = None,
        team_id: str = None,
    ):
        api_path = "/team-stats"
        additional_params = {}
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id

        return self.base_request(api_path, additional_params, sports)

    def get_player_info(
        self,
        sports: list[Sport] = None,
        team_id: str = None,
        from_assets: bool = True,
    ):
        if from_assets:
            data = {}
            for sport in sports:
                loaded = pd.read_csv(
                    os.path.join(__location__, "assets/{}/players.csv".format(sport))
                )
                if team_id:
                    loaded = loaded[loaded["team_id" == team_id]]
                if self.preferred_dataframe != "pandas":
                    loaded = (
                        loaded.to_dict("records")
                        if not self.preferred_dataframe
                        else pl.LazyFrame(loaded)
                    )
                data[sport] = loaded
            return data
        api_path = "/player-info"
        additional_params = {}
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id

        return self.base_request(api_path, additional_params, sports)

    def get_player_stats(
        self,
        date: str = None,
        sports: list[Sport] = None,
        team_id: str = None,
        player_id: str = None,
    ):
        api_path = "/player-stats"
        additional_params = {}
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id
        if player_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `player_id` parameter."
                )
            additional_params["player_id"] = player_id

        return self.base_request(api_path, additional_params, sports)

    def get_player_injuries(
        self,
        sports: list[Sport] = None,
        team_id: str = None,
    ):
        api_path = "/injuries"
        additional_params = {}
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id

        return self.base_request(api_path, additional_params, sports)

    def get_team_depth_chart(
        self,
        sports: list[Sport] = None,
        team_id: str = None,
    ):
        api_path = "/depth-charts"
        additional_params = {}
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id

        return self.base_request(api_path, additional_params, sports)
