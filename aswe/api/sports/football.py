import os

from aswe.utils.request import http_request

API_key = os.getenv("SOCCER_API_key")
headers = {"X-Auth-Token": API_key}


def convert_league_name(name: str) -> str | None:
    """_summary_

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
        return "Cl"
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
    """_summary_

    Parameters
    ----------
    league : str
        Name of the league

    Returns
    -------
    list[str] | None
        Return list of the standings
    """
    valid = {"WC", "CL", "BL1", "DED", "BSA", "PD", "FL1", "ELC", "PPL", "EC", "SA", "PL"}
    standings = []
    if league not in valid:
        return None
    request = http_request(f"https://api.football-data.org/v4/competitions/{league}/standings", headers=headers)
    if request is None:
        return None
    results = request.json()
    for team in results["standings"][0]["table"]:
        standings.append(str(team["position"]) + ". " + team["team"]["name"] + " - " + str(team["points"]) + " points")
    return standings


def get_matchday_matches(league: str, matchday: int) -> list[str] | None:
    """_summary_

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
    valid = {"WC", "CL", "BL1", "DED", "BSA", "PD", "FL1", "ELC", "PPL", "EC", "SA", "PL"}
    matches = []
    if league not in valid:
        return None
    request = http_request(
        f"https://api.football-data.org/v4/competitions/{league}/matches?matchday={matchday}", headers=headers
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
                + " : "
                + str(match["score"]["fullTime"]["away"])
                + " "
                + match["awayTeam"]["name"]
            )
    return matches


def get_ongoing_matches(league: str = "") -> list[str] | None:
    """_summary_

    Parameters
    ----------
    league : str, optional
        Name of the league, by default ""

    Returns
    -------
    list[str] | None
        List of the ongoing matches in the specified league
    """
    valid = {"WC", "CL", "BL1", "DED", "BSA", "PD", "FL1", "ELC", "PPL", "EC", "SA", "PL", ""}
    matches = []
    if league not in valid:
        return None
    request = http_request("https://api.football-data.org/v4/matches?status=IN_PLAY", headers=headers)
    if request is None:
        return None
    results = request.json()
    for match in results["matches"]:
        if match["competition"]["code"] == league or league == "":
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
    if matches is []:
        matches = ["No matches are currently being played."]
    return matches


def get_matches_today(league: str = "") -> list[str] | None:
    """_summary_

    Parameters
    ----------
    league : str, optional
        Name of the league, by default ""

    Returns
    -------
    list[str] | None
        List of the matches on the current day in the specified league
    """
    valid = {"WC", "CL", "BL1", "DED", "BSA", "PD", "FL1", "ELC", "PPL", "EC", "SA", "PL", ""}
    matches = []
    if league not in valid:
        return None
    request = http_request("https://api.football-data.org/v4/matches?status=SCHEDULED", headers=headers)
    if request is None:
        return None
    results = request.json()
    for match in results["matches"]:
        if match["competition"]["code"] == league or league == "":
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
    """_summary_

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
    request = http_request(f"https://api.football-data.org/v4/competitions/{league}/teams", headers=headers)
    if request is None:
        return None
    team_list = request.json()
    for team in team_list["teams"]:
        if team["name"] == team_name or team["shortName"] == team_name:
            team_id = team["id"]
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
    """_summary_

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
    request = http_request(f"https://api.football-data.org/v4/competitions/{league}/teams", headers=headers)
    if request is None:
        return None
    team_list = request.json()
    for team in team_list["teams"]:
        if team["name"] == team_name or team["shortName"] == team_name:
            team_id = team["id"]
    request = http_request(
        f"https://api.football-data.org/v4/teams/{team_id}/matches?status=IN_PLAY", headers=headers
    )
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
