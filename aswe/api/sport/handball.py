import os
from datetime import date

from aswe.utils.error import ApiLimitReached
from aswe.utils.request import http_request, validate_api

_HEADERS = {"x-rapidapi-key": os.getenv("SPORTS_API_KEY"), "x-rapidapi-host": "v1.handball.api-sports.io"}


def get_league_id(league_name: str) -> int | None:
    """Get league id from league name

    Parameters
    ----------
    league_name : str
        Name of the league

    Returns
    -------
    int | None
        Return the id of the league
    """
    request = http_request("https://v1.handball.api-sports.io/leagues", headers=_HEADERS)
    if request is None:
        return None
    if validate_api(request):
        raise ApiLimitReached("You have reached the handball API request limit for the day")
    data = request.json()
    for league in data["response"]:
        if league["name"] == league_name:
            return int(league["id"])
    return None


def get_league_teams(league_name: str) -> list[str] | None:
    """Get the league teams of a league

    Parameters
    ----------
    league_name : str
        Name of the league for which the teams are returned

    Returns
    -------
    list[str] | None
        Return a list of strings with the teams in the league
    """
    league_id = get_league_id(league_name)
    if league_id is None:
        return None
    request = http_request(
        f"https://v1.handball.api-sports.io/standings?league={league_id}&season=2022", headers=_HEADERS
    )
    if request is None:
        return None
    if validate_api(request):
        raise ApiLimitReached("You have reached the handball API request limit for the day")
    standings = request.json()
    table = []
    for position in standings["response"][0]:
        table.append(position["team"]["name"])
    return table


def get_league_table(league_name: str = "Bundesliga") -> list[str] | None:
    """Get the league table of a league

    Parameters
    ----------
    league_name : str, optional
        Name of the league for which a table is returned. _By default `Bundesliga`._

    Returns
    -------
    list[str] | None
        Return a list of strings with the league table
    """
    league_id = get_league_id(league_name)
    if league_id is None:
        return None
    request = http_request(
        f"https://v1.handball.api-sports.io/standings?league={league_id}&season=2022", headers=_HEADERS
    )
    if request is None:
        return None
    if validate_api(request):
        raise ApiLimitReached("You have reached the handball API request limit for the day")
    standings = request.json()
    table = []
    for position in standings["response"][0]:
        table.append(f'{position["position"]}. {position["team"]["name"]} {position["points"]} points')
    return table


def get_team_id(team_name: str) -> int | None:
    """Get team id from team name

    Parameters
    ----------
    team_name : str
        Name of the team for which the id is to be returned

    Returns
    -------
    int | None
        Return the id of the team
    """
    team_name = team_name.replace(" ", "%20")
    request = http_request(f"https://v1.handball.api-sports.io/teams?name={team_name}", headers=_HEADERS)
    if request is None:
        return None
    if validate_api(request):
        raise ApiLimitReached("You have reached the handball API request limit for the day")
    data = request.json()

    if data["response"] == []:
        return None

    return int(data["response"][0]["id"])


def get_team_game_today(team_name: str, league_name: str = "Bundesliga") -> list[str] | None:
    """Get the game of a team today

    Parameters
    ----------
    team_name : str
        Name of the team for which the game is to be returned
    league_name : str, optional
        Name of the league in which the game is to be played. _By default `Bundesliga`._

    Returns
    -------
    list[str] | None
        Return a list of a string with the game
    """
    league_id = get_league_id(league_name)
    if league_id is None:
        return None
    today = date.today()
    team_name = team_name.replace(" ", "%20")
    team_id = get_team_id(team_name)
    if team_id is None:
        return None
    request = http_request(
        f"https://v1.handball.api-sports.io/games?date={today}&timezone=Europe/Berlin\
            &league={league_id}&season=2022&team={team_id}",
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
            f"{game['teams']['home']['name']} {game['scores']['home']} - "
            f"{game['scores']['away']} {game['teams']['away']['name']}"
        )
    return games
