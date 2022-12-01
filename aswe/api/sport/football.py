import os

from dotenv import load_dotenv

from aswe.utils.request import http_request

load_dotenv()

API_key = os.getenv("SOCCER_API_KEY")
headers = {"X-Auth-Token": API_key}


def convert_league_name(name: str) -> str | None:
    """Converts the name of the league to the code used by the API

    Parameters
    ----------
    name : str
        Name of the league

    Returns
    -------
    str | None
        Return id of the league
    """
    valid = {
        "Premier League",
        "English League",
        "Primera Division",
        "Spanish League",
        "Serie A",
        "Italian League",
        "Bundesliga",
        "German League",
        "Ligue 1",
        "French League",
        "FIFA World Cup",
        "World Cup",
        "UEFA Champions League",
        "Champions League",
        "Eredivisie",
        "Dutch League",
        "Campeonato Brasileiro Série A",
        "Brazilian League",
        "Championship",
        "English League 2",
        "Primeira Liga",
        "Portugese League",
        "European Championship",
        "Euro",
    }
    if name not in valid:
        return None
    if name == "Premier League" or name == "English League":
        return "PL"
    elif name == "Primera Division" or name == "Spanish League":
        return "PD"
    elif name == "Serie A" or name == "Italian League":
        return "SA"
    elif name == "Bundesliga" or name == "German League":
        return "BL1"
    elif name == "Ligue 1" or name == "French League":
        return "FL1"
    elif name == "FIFA World Cup" or name == "World Cup":
        return "WC"
    elif name == "UEFA Champions League" or name == "Champions League":
        return "CL"
    elif name == "Eredivisie" or name == "Dutch League":
        return "DED"
    elif name == "Campeonato Brasileiro Série A" or name == "Brazilian League":
        return "BSA"
    elif name == "Championship" or name == "English League 2":
        return "ELC"
    elif name == "Primeira Liga" or name == "Portuguese League":
        return "PPL"
    elif name == "European Championship" or name == "Euro":
        return "EC"
    return None


def get_league_standings(league: str) -> list[str] | None:
    """Get the standings of the league

    Parameters
    ----------
    league : str
        Name of the league

    Returns
    -------
    list[str] | None
        Return list of the standings
    """
    league_id = convert_league_name(league)
    standings = []
    if league_id is None:
        return None
    request = http_request(f"https://api.football-data.org/v4/competitions/{league_id}/standings", headers=headers)
    if request is None:
        return None
    results = request.json()
    for team in results["standings"][0]["table"]:
        standings.append(str(team["position"]) + ". " + team["team"]["name"] + " - " + str(team["points"]) + " points")
    return standings


def get_matchday_matches(league: str, matchday: int) -> list[str] | None:
    """Get the matches of the specified matchday

    Parameters
    ----------
    league : str
        Name of the league
    matchday : int
        Number of the matchday

    Returns
    -------
    list[str] | None
        Return list of the matches on that matchday
    """
    league_id = convert_league_name(league)
    matches = []
    if league_id is None:
        return None
    request = http_request(
        f"https://api.football-data.org/v4/competitions/{league_id}/matches?matchday={matchday}", headers=headers
    )
    if request is None:
        return None
    results = request.json()

    for match in results["matches"]:
        if match["status"] == "SCHEDULED" or match["status"] == "TIMED":
            matches.append(
                "playing on the "
                + match["utcDate"][-12:-10]
                + "."
                + match["utcDate"][-15:-13]
                + "."
                + match["utcDate"][0:4]
                + " at "
                + str(int(match["utcDate"][-9:-7]) + 2)
                + match["utcDate"][-7:-4]
                + ": "
                + match["homeTeam"]["name"]
                + " vs "
                + match["awayTeam"]["name"]
            )
        elif match["status"] == "FINISHED":
            matches.append(
                "played on the "
                + match["utcDate"][-12:-10]
                + "."
                + match["utcDate"][-15:-13]
                + "."
                + match["utcDate"][0:4]
                + " at "
                + str(int(match["utcDate"][-9:-7]) + 1)
                + match["utcDate"][-7:-4]
                + ": "
                + match["homeTeam"]["name"]
                + " "
                + str(match["score"]["fullTime"]["home"])
                + " to "
                + str(match["score"]["fullTime"]["away"])
                + " "
                + match["awayTeam"]["name"]
            )
    return matches


def get_ongoing_matches(league: str = "") -> list[str] | None:
    """Get the ongoing matches in the specified league

    Parameters
    ----------
    league : str, optional
        Name of the league, by default ""

    Returns
    -------
    list[str] | None
        List of the ongoing matches in the specified league
    """
    league_id = convert_league_name(league)
    matches = []
    if league_id is None:
        return None
    request = http_request("https://api.football-data.org/v4/matches?status=IN_PLAY", headers=headers)
    if request is None:
        return None
    results = request.json()
    for match in results["matches"]:
        if match["competition"]["code"] == league_id:
            matches.append(
                match["homeTeam"]["name"]
                + " "
                + str(match["score"]["fullTime"]["home"])
                + " : "
                + str(match["score"]["fullTime"]["away"])
                + " "
                + match["awayTeam"]["name"]
                + " in "
                + match["competition"]["name"]
            )

    if not matches:
        matches = ["No matches are currently being played."]
    return matches


def get_matches_today(league: str = "") -> list[str] | None:
    """Get the matches that are being played today

    Parameters
    ----------
    league : str, optional
        Name of the league, by default ""

    Returns
    -------
    list[str] | None
        List of the matches on the current day in the specified league
    """
    league_id = convert_league_name(league)
    matches = []
    if league_id is None:
        return None
    request = http_request("https://api.football-data.org/v4/matches?status=SCHEDULED", headers=headers)
    if request is None:
        return None
    results = request.json()
    for match in results["matches"]:
        if match["competition"]["code"] == league_id:
            matches.append(
                "playing at "
                + str(int(match["utcDate"][-9:-7]) + 1)
                + match["utcDate"][-7:-4]
                + ": "
                + match["homeTeam"]["name"]
                + " vs "
                + match["awayTeam"]["name"]
                + " in "
                + match["competition"]["name"]
            )
    return matches


def get_upcoming_team_matches(league: str, team_name: str, num_matches: int = 3) -> list[str] | None:
    """Get the upcoming matches of the specified team

    Parameters
    ----------
    league : str
        Name of the league
    team_name : str
        Name of the team from which the matches are requested
    num_matches : int, optional
        Number of matches which will be returned, by default 3

    Returns
    -------
    list[str] | None
       Return list of the upcoming matches of the specified team
    """
    league_id = convert_league_name(league)
    if league_id is None:
        return None
    request = http_request(f"https://api.football-data.org/v4/competitions/{league_id}/teams", headers=headers)
    if request is None:
        return None
    team_list = request.json()
    team_id = ""
    for team in team_list["teams"]:
        if team["name"] == team_name or team["shortName"] == team_name:
            team_id = team["id"]
    if team_id == "":
        return None
    request = http_request(
        f"https://api.football-data.org/v4/teams/{team_id}/matches?status=SCHEDULED", headers=headers
    )
    if request is None:
        return None
    results = request.json()
    matches = []
    for match in results["matches"]:
        matches.append(
            "playing on the "
            + match["utcDate"][-12:-10]
            + "."
            + match["utcDate"][-15:-13]
            + "."
            + match["utcDate"][0:4]
            + " at "
            + str(int(match["utcDate"][-9:-7]) + 2)
            + match["utcDate"][-7:-4]
            + ": "
            + match["homeTeam"]["name"]
            + " vs "
            + match["awayTeam"]["name"]
        )
    return matches[0:num_matches]


def get_current_team_match(league: str, team_name: str) -> list[str] | None:
    """Get the current match of the specified team

    Parameters
    ----------
    league : str
        Name of the league
    team_name : str
        Name of the team from which the match is requested

    Returns
    -------
    list[str] | None
        Return list of the current match of the specified team
    """
    league_id = convert_league_name(league)
    if league_id is None:
        return None
    request = http_request(f"https://api.football-data.org/v4/competitions/{league_id}/teams", headers=headers)
    if request is None:
        return None
    team_list = request.json()
    team_id = ""
    for team in team_list["teams"]:
        if team["name"] == team_name or team["shortName"] == team_name:
            team_id = team["id"]
    if team_id == "":
        return None
    request = http_request(f"https://api.football-data.org/v4/teams/{team_id}/matches?status=IN_PLAY", headers=headers)
    if request is None:
        return None
    results = request.json()
    matches = []
    for match in results["matches"]:
        matches.append(
            match["homeTeam"]["name"]
            + " "
            + str(match["score"]["fullTime"]["home"])
            + " : "
            + str(match["score"]["fullTime"]["away"])
            + " "
            + match["awayTeam"]["name"]
            + " in "
            + match["competition"]["name"]
        )
    return matches


def get_teams(league: str) -> list[str] | None:
    """Get the teams of the specified league

    Parameters
    ----------
    league : str
        Name of the league

    Returns
    -------
    list[str] | None
        Return list of the teams of the specified league
    """
    league_id = convert_league_name(league)
    if league_id is None:
        return None
    request = http_request(f"https://api.football-data.org/v4/competitions/{league_id}/teams", headers=headers)
    if request is None:
        return None
    results = request.json()
    teams = []
    for team in results["teams"]:
        teams.append(team["name"])
    return teams
