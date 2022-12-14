import os
from datetime import date

from aswe.utils.error import ApiLimitReached
from aswe.utils.request import http_request, validate_api

_HEADERS = {"x-rapidapi-key": os.getenv("SPORTS_API_KEY"), "x-rapidapi-host": "v1.basketball.api-sports.io"}


def get_nba_standings() -> list[list[str]] | None:
    """Get the current standings of the NBA

    Returns
    -------
    list[list[str]] | None
        List of the standings of both eastern and western conference
    """
    request = http_request("https://v1.basketball.api-sports.io/standings?league=12&season=2022-2023", headers=_HEADERS)
    if request is None:
        return None
    if validate_api(request):
        raise ApiLimitReached("You have reached the handball API request limit for the day")
    data = request.json()
    wc_standings = []
    ec_standings = []
    conferences = []
    for team in data["response"][0]:
        if team["group"]["name"] == "Eastern Conference" or team["group"]["name"] == "Western Conference":
            if team["group"]["name"] not in conferences:
                conferences.append(team["group"]["name"])
            if team["group"]["name"] == "Eastern Conference":
                ec_standings.append(
                    f"{team['position']}. {team['team']['name']} {team['games']['win']['total']} wins {team['games']['lose']['total']} losses"
                )
            if team["group"]["name"] == "Western Conference":
                wc_standings.append(
                    f"{team['position']}. {team['team']['name']} {team['games']['win']['total']} wins {team['games']['lose']['total']} losses"
                )
    return [wc_standings, ec_standings]


def get_nba_teams() -> list[str] | None:
    """Get all NBA teams

    Returns
    -------
    list[str] | None
        List of all NBA teams
    """
    request = http_request("https://v1.basketball.api-sports.io/standings?league=12&season=2022-2023", headers=_HEADERS)
    if request is None:
        return None
    if validate_api(request):
        raise ApiLimitReached("You have reached the handball API request limit for the day")
    data = request.json()
    teams = []
    for team in data["response"][0]:
        teams.append(team["team"]["name"])
    return teams


def get_team_id(team_name: str) -> int | None:
    """Get the id of a team

    Parameters
    ----------
    team_name : str
        Name of the team for which an id is to be returned

    Returns
    -------
    int | None
        _description_
    """
    team_name = team_name.replace(" ", "%20")
    request = http_request(f"https://v1.basketball.api-sports.io/teams?name={team_name}", headers=_HEADERS)
    if request is None:
        return None
    if validate_api(request):
        raise ApiLimitReached("You have reached the handball API request limit for the day")
    data = request.json()

    if data["response"] == []:
        return None

    return int(data["response"][0]["id"])


def get_team_game_today(team_name: str) -> list[str] | None:
    """Get the game of a team today

    Parameters
    ----------
    team_name : str
        Name of the team for which a game is to be returned

    Returns
    -------
    list[str] | None
        Return list with the game of the team on the current day
    """
    today = date.today()
    team_name = team_name.replace(" ", "%20")
    team_id = get_team_id(team_name)
    if team_id is None:
        return None
    request = http_request(
        f"https://v1.basketball.api-sports.io/games?date={today}&\
            timezone=Europe/Berlin&league=12&season=2022-2023&team={team_id}",
        headers=_HEADERS,
    )
    if request is None:
        return None
    if validate_api(request):
        raise ApiLimitReached("You have reached the handball API request limit for the day")
    data = request.json()

    if data["response"] == []:
        return []

    games = []
    for game in data["response"]:
        games.append(
            f"{game['teams']['home']['name']} {game['scores']['home']['total']} - \
{game['scores']['away']['total']} {game['teams']['away']['name']}"
        )
    return games
