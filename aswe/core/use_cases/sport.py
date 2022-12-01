from aswe.api.sport import football
from aswe.core.data import BestMatch
from aswe.utils.abstract import AbstractUseCase


class SportUseCase(AbstractUseCase):
    """ "Use case for sports"""

    def choose_league(self, leagues: list[str]) -> str:
        """Returns the league the users chooses.

        Returns
        -------
        str
            The league the user chooses.
        """
        self.tts.convert_text("Hey, Please tell me the league you are interested in.")
        for i, league in enumerate(leagues):
            print(f"{i + 1}: {league}")
        result = None
        while result is None or (result is not None and result not in range(1, len(leagues) + 1)):  # type: ignore
            try:
                result = int(input("Which league are you interested in?"))
            except ValueError:
                print("Pleae enter a valid league number.")
        return leagues[result - 1]  # type: ignore

    def choose_team(self, teams: list[str]) -> str:
        """Returns the team the users chooses.

        Returns
        -------
        str
            The team the user chooses.
        """
        self.tts.convert_text("Hey, Please tell me the team you are interested in.")
        for i, team in enumerate(teams):
            print(f"{i + 1}: {team}")
        result = None
        while result is None or (result is not None and result not in range(1, len(teams) + 1)):  # type: ignore
            try:
                result = int(input("Which team are you interested in?"))
            except ValueError:
                print("Pleae enter a valid team number.")
        return teams[result - 1]  # type: ignore

    def get_matchday_num(self, max_num: int) -> int:
        """Returns the matchday number the user chooses.

        Parameters
        ----------
        max_num : int
            The maximum number of matchdays.

        Returns
        -------
        int
            The matchday number the user chooses.
        """
        self.tts.convert_text(
            f"Hey, please tell me the matchday you are interested in. It is possible to choose between 1 and {max_num}"
        )
        result = None
        while result is None or (result is not None and result not in range(1, max_num)):  # type: ignore
            try:
                result = int(input("Which matchday are you interested in? "))
            except ValueError:
                print("Pleae enter a valid matchday number.")
        return result  # type: ignore

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for sport

        * TODO: Implement `quotes_key`
        * TODO: Fix typing (remove type ignore)
        * TODO: Implement custom exceptions

        Parameters
        ----------
        best_match : BestMatch
            An object containing the best match for the user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        match best_match.function_key:
            case "footballStandings":
                leagues = ["Premier League", "Bundesliga", "Serie A", "Ligue 1"]
                league = self.choose_league(leagues)
                self.tts.convert_text(f"The current standings of the {league} are:")
                standings = football.get_league_standings(league)
                if standings is None:
                    raise Exception("Could not get standings")
                for team in standings:
                    self.tts.convert_text(team)
            case "footballMatchdayMatches":
                leagues = ["Premier League", "Bundesliga", "Serie A", "Ligue 1"]
                league = self.choose_league(leagues)
                matchday = self.get_matchday_num(36)
                matches = football.get_matchday_matches(league, matchday)
                if matches is None:
                    raise Exception("Could not get matches")
                for match in matches:
                    self.tts.convert_text(match)
            case "footballOngoingMatches":
                leagues = ["Premier League", "Bundesliga", "Serie A", "Ligue 1", "World Cup"]
                league = self.choose_league(leagues)
                matches = football.get_ongoing_matches(league)
                if matches is None:
                    raise Exception("Could not get matches")
                for match in matches:
                    self.tts.convert_text(match)
            case "footballUpcomingMatches":
                leagues = ["Premier League", "Bundesliga", "Serie A", "Ligue 1", "World Cup"]
                league = self.choose_league(leagues)
                teams = football.get_teams(league)
                if teams is None:
                    raise Exception("Could not get teams")
                team = self.choose_team(teams)
                matches = football.get_upcoming_team_matches(league, team)
                if matches == []:
                    self.tts.convert_text(f"There are no upcoming matches for {team} in the {league}.")
                if matches is None:
                    raise Exception("Could not get matches")
                for match in matches:
                    self.tts.convert_text(match)
            case "footballCurrentMatch":
                leagues = ["Premier League", "Bundesliga", "Serie A", "Ligue 1", "World Cup"]
                league = self.choose_league(leagues)
                teams = football.get_teams(league)
                if teams is None:
                    raise Exception("Could not get teams")
                team = self.choose_team(teams)
                if team is None or league:
                    raise Exception("Could not get team")
                cur_match = football.get_current_team_match(league, team)
                if cur_match is None:
                    raise Exception("Could not get current match")
                self.tts.convert_text(cur_match[0])
            case _:
                raise NotImplementedError
