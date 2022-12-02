from aswe.utils.request import http_request


def get_results_by_round(year: int, round_num: int) -> list[str] | None:
    """Get f1 results by round

    Parameters
    ----------
    year : int
        Year of the season in which the race took place
    round_num : int
        Number of the race in the season

    Returns
    -------
    list[str] | None
        Returns a list of strings with the results
    """
    url = f"https://ergast.com/api/f1/{year}/{round_num}/results.json"
    request = http_request(url)
    if request is None:
        return None
    response = dict(request.json())

    if response["MRData"]["total"] == "0":
        return None
    result = [
        (
            f"{driver['Driver']['givenName']} {driver['Driver']['familyName']} - "
            f"{driver['Constructor']['name']} - {driver['position']}"
        )
        for driver in response["MRData"]["RaceTable"]["Races"][0]["Results"]
    ]
    return result


def get_results_next_round() -> list[str] | None:
    """Get information about the next round

    Returns
    -------
    list[str] | None
        Returns a list of strings with information about the next round
    """
    url = "https://ergast.com/api/f1/current/next/results.json"
    request = http_request(url)
    if request is None:
        return None
    response = dict(request.json())

    if response["MRData"]["total"] == "0":
        return []

    result = [
        (
            f"{driver['Driver']['givenName']} {driver['Driver']['familyName']} -\""
            f"{driver['Constructor']['name']} - {driver['position']}"
        )
        for driver in response["MRData"]["RaceTable"]["Races"][0]["Results"]
    ]
    return result


def get_results_last_round() -> list[str] | None:
    """Get results of last round

    Returns
    -------
    list[str] | None
        Returns a list of strings with the results of the last round
    """
    url = "https://ergast.com/api/f1/current/last/results.json"
    request = http_request(url)
    if request is None:
        return None
    response = dict(request.json())

    if response["MRData"]["total"] == "0":
        return []

    result = [
        (
            f"{driver['Driver']['givenName']} {driver['Driver']['familyName']} - "
            f"{driver['Constructor']['name']} - {driver['position']}"
        )
        for driver in response["MRData"]["RaceTable"]["Races"][0]["Results"]
    ]
    return result
