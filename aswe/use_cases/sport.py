from aswe.api.sport import basketball, f1, football, handball
from aswe.core.objects import BestMatch
from aswe.utils.abstract import AbstractUseCase
from aswe.utils.error import ApiLimitReached


class SportUseCase(AbstractUseCase):
    """Use case for sports"""

    def check_proactivity(self) -> None:
        """Check if there is a proactivity to be triggered

        * TODO: Why is it necessary to check if valid_teams is None twice?
        """
        valid_teams = football.get_teams(self.user.favorites.league)
        if valid_teams is None:
            self.tts.convert_text("Sorry, I could not find any teams for the league you specified.")
        if valid_teams is not None and self.user.favorites.team not in valid_teams:
            self.tts.convert_text(
                f"{self.user.favorites.team} could not be found"
                f"in {self.user.favorites.league}. Pleaser choose a team which plays in the legue which was specified."
            )
        match = football.get_current_team_match(self.user.favorites.league, self.user.favorites.team)
        if match is None:
            return
        self.tts.convert_text(match[0])

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
            case "footballMatchesToday":
                leagues = ["Premier League", "Bundesliga", "Serie A", "Ligue 1", "World Cup"]
                league = self.choose_league(leagues)
                matches = football.get_matches_today(league)
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
                teams = [x for x in teams if not x.isnumeric()]  # type: ignore
                team = self.choose_team(teams)
                matches = football.get_upcoming_team_matches(league, team)
                if matches == []:
                    self.tts.convert_text(f"There are no upcoming matches for {team} in the {league}.")
                if matches is None:
                    raise Exception("Could not get matches")
                for match in matches:
                    self.tts.convert_text(match)
            case "basketballStandings":
                try:
                    nba_standings = basketball.get_nba_standings()
                    if nba_standings is None:
                        raise Exception("Could not get NBA standings")
                    self.tts.convert_text("The current standings of the NBA Western Conference are:")
                    for team in nba_standings[0]:
                        self.tts.convert_text(team)
                    self.tts.convert_text("The current standings of the NBA Eastern Conference are:")
                    for team in nba_standings[1]:
                        self.tts.convert_text(team)
                except ApiLimitReached:
                    self.tts.convert_text("Sorry, the API limit for the NBA API has been reached.")
            case "basketballTeamGameToday":
                try:
                    teams = basketball.get_nba_teams()
                    if teams is None:
                        raise Exception("Could not get NBA teams")
                    team = self.choose_team(teams)
                    game = basketball.get_team_game_today(team)
                    if game is None:
                        raise Exception("Could not get basketball game")
                    try:
                        self.tts.convert_text(game[0])
                    except IndexError:
                        self.tts.convert_text(f"The {team} have no games today.")
                except ApiLimitReached:
                    self.tts.convert_text("Sorry, the API limit for the NBA API has been reached.")
            case "handballStandings":
                try:
                    leagues = ["Bundesliga", "Starligue", "Liga ASOBAL"]
                    league = self.choose_league(leagues)
                    handball_standings = handball.get_league_table(league)
                    if handball_standings is None:
                        raise Exception("Could not get handball standings")
                    for team in handball_standings:
                        self.tts.convert_text(team)
                except ApiLimitReached:
                    self.tts.convert_text("Sorry, the API limit for the handball API has been reached.")
            case "handballTeamGameToday":
                try:
                    leagues = ["Bundesliga", "Starligue", "Liga ASOBAL"]
                    league = self.choose_league(leagues)
                    teams = handball.get_league_teams(league)
                    if teams is None:
                        raise Exception("Could not get handball teams")
                    team = self.choose_team(teams)
                    handball_game = handball.get_team_game_today(team)
                    if handball_game is None:
                        raise Exception("Could not get handball game")
                    try:
                        self.tts.convert_text(handball_game[0])
                    except IndexError:
                        self.tts.convert_text(f"The {team} have no games today.")
                except ApiLimitReached:
                    self.tts.convert_text("Sorry, the API limit for the handball API has been reached.")
            case "f1ResultsByRound":
                self.tts.convert_text("Please enter the round of the past formula 1 season you are interested in.")
                race_num = input("Which round are you interested in? ")
                while not race_num.isdigit() or int(race_num) < 1 or int(race_num) > 22:  # type: ignore
                    self.tts.convert_text("Please enter a valid round number. Must be between 1 and 22.")
                    race_num = input("Which round are you interested in? ")
                results = f1.get_results_by_round(2022, race_num)  # type: ignore
                if results is None:
                    raise Exception("Could not get results")
                for driver in results:
                    self.tts.convert_text(driver)
            case "f1LastRoundResult":
                results = f1.get_results_last_round()
                if results is None:
                    raise Exception("Could not get results")
                self.tts.convert_text("The results of the last round of the 2022 formula 1 season are:")
                for driver in results:
                    self.tts.convert_text(driver)

            case _:
                raise NotImplementedError
