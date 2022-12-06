# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from pytest_mock import MockFixture

from aswe.api.sport import basketball as basketballApi
from aswe.api.sport import f1 as f1Api
from aswe.api.sport import football as footballApi
from aswe.api.sport import handball as handballApi
from aswe.core.objects import Address, BestMatch, Favorites, Possessions, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.use_cases.sport import SportUseCase


@pytest.fixture(scope="function")
def patch_stt(mocker: MockFixture) -> SpeechToText:
    """Patch `convert_speech` method of `SpeechToText` Class"""
    patched_stt: SpeechToText = mocker.patch.object(SpeechToText, "convert_speech")

    return patched_stt


@pytest.fixture(scope="function")
def patch_tts(mocker: MockFixture) -> TextToSpeech:
    """Patch `convert_text` method of `TextToSpeech` Class"""
    patched_tts: TextToSpeech = mocker.patch.object(TextToSpeech, "convert_text")

    return patched_tts


def test_choose_league(patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the choose_league method of the SportUseCase class

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.tts = MagicMock()  # Use a mock object for the tts property
    leagues = ["Premier League", "Bundesliga", "Serie A", "Ligue 1"]

    # Test the choose_league method
    with patch("builtins.input", return_value="2"):
        result = use_case.choose_league(leagues)
        assert result == "Bundesliga"


def test_choose_team(patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the choose_team method of the SportUseCase class

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.tts = MagicMock()  # Use a mock object for the tts property
    teams = ["Team1", "Team2", "Team3"]

    # Test the choose_team method
    with patch("builtins.input", return_value="3"):
        result = use_case.choose_team(teams)
        assert result == "Team3"


def test_get_matchday_num(patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the get_matchday_num method of the SportUseCase class

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.tts = MagicMock()  # Use a mock object for the tts property

    # Test the choose_team method
    with patch("builtins.input", return_value="3"):
        result = use_case.get_matchday_num(10)
        assert result == 3


def test_football_standings(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of footballStandings in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(use_case="sport", function_key="footballStandings", similarity=1, parsed_text="lorem ipsum")
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(footballApi, "get_league_standings", return_value=["1.Bayern", "2.Frankfurt", "3.Dortmund"])
    mocked_sport_choose_league = mocker.patch.object(SportUseCase, "choose_league", return_value="Bundesliga")

    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    mocked_sport_choose_league.assert_called_once_with(["Premier League", "Bundesliga", "Serie A", "Ligue 1"])
    spy_tts_convert_text.assert_called_with("3.Dortmund")

    mocker.patch.object(footballApi, "get_league_standings", return_value=None)
    with pytest.raises(Exception, match="Could not get standings"):
        use_case.trigger_assistant(best_match)


def test_football_matchday_matches(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of footballMatchdayMatches in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(
        use_case="sport", function_key="footballMatchdayMatches", similarity=1, parsed_text="lorem ipsum"
    )
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(footballApi, "get_matchday_matches", return_value=["Team A vs. Team B", "Team C vs. Team D"])
    mocked_sport_choose_league = mocker.patch.object(SportUseCase, "choose_league", return_value="Bundesliga")
    mocked_sport_choose_matchday = mocker.patch.object(SportUseCase, "get_matchday_num", return_value=3)

    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    mocked_sport_choose_league.assert_called_with(["Premier League", "Bundesliga", "Serie A", "Ligue 1"])
    mocked_sport_choose_matchday.assert_called_once()
    spy_tts_convert_text.assert_called_with("Team C vs. Team D")

    mocker.patch.object(footballApi, "get_matchday_matches", return_value=None)
    with pytest.raises(Exception, match="Could not get matches"):
        use_case.trigger_assistant(best_match)


def test_football_ongoing_matches(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of footballOngoingMatches in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(
        use_case="sport", function_key="footballOngoingMatches", similarity=1, parsed_text="lorem ipsum"
    )
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(footballApi, "get_ongoing_matches", return_value=["Team A vs. Team B", "Team C vs. Team D"])
    mocked_sport_choose_league = mocker.patch.object(SportUseCase, "choose_league", return_value="Bundesliga")

    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    mocked_sport_choose_league.assert_called_with(["Premier League", "Bundesliga", "Serie A", "Ligue 1", "World Cup"])
    # spy_tts_convert_text.assert_called_with("Team A vs. Team B")
    assert spy_tts_convert_text.call_args_list[0][0][0] == "Team A vs. Team B"
    assert spy_tts_convert_text.call_args_list[1][0][0] == "Team C vs. Team D"

    mocker.patch.object(footballApi, "get_ongoing_matches", return_value=None)
    with pytest.raises(Exception, match="Could not get matches"):
        use_case.trigger_assistant(best_match)


def test_football_matches_today(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of footballMatchesToday in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(
        use_case="sport", function_key="footballMatchesToday", similarity=1, parsed_text="lorem ipsum"
    )
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(footballApi, "get_matches_today", return_value=["Team A vs. Team B", "Team C vs. Team D"])
    mocked_sport_choose_league = mocker.patch.object(SportUseCase, "choose_league", return_value="Bundesliga")

    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    mocked_sport_choose_league.assert_called_with(["Premier League", "Bundesliga", "Serie A", "Ligue 1", "World Cup"])
    # spy_tts_convert_text.assert_called_with("Team A vs. Team B")
    assert spy_tts_convert_text.call_args_list[0][0][0] == "Team A vs. Team B"
    assert spy_tts_convert_text.call_args_list[1][0][0] == "Team C vs. Team D"

    mocker.patch.object(footballApi, "get_matches_today", return_value=None)
    with pytest.raises(Exception, match="Could not get matches"):
        use_case.trigger_assistant(best_match)


def test_football_upcoming_matches(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of footballUpcomingMatches in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(
        use_case="sport", function_key="footballUpcomingMatches", similarity=1, parsed_text="lorem ipsum"
    )
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(
        footballApi, "get_upcoming_team_matches", return_value=["Team A vs. Team B", "Team C vs. Team D"]
    )
    mocked_sport_choose_league = mocker.patch.object(SportUseCase, "choose_league", return_value="Bundesliga")
    mocker.patch.object(footballApi, "get_teams", return_value=["Team A vs. Team B", "Team C vs. Team D"])
    mocker.patch.object(SportUseCase, "choose_team", return_value="Bayern")
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    mocked_sport_choose_league.assert_called_with(["Premier League", "Bundesliga", "Serie A", "Ligue 1", "World Cup"])
    # spy_tts_convert_text.assert_called_with("Team A vs. Team B")
    assert spy_tts_convert_text.call_args_list[0][0][0] == "Team A vs. Team B"
    assert spy_tts_convert_text.call_args_list[1][0][0] == "Team C vs. Team D"

    mocker.patch.object(footballApi, "get_upcoming_team_matches", return_value=None)
    with pytest.raises(Exception, match="Could not get matches"):
        use_case.trigger_assistant(best_match)
    mocker.patch.object(footballApi, "get_teams", return_value=None)
    with pytest.raises(Exception, match="Could not get teams"):
        use_case.trigger_assistant(best_match)


def test_basketball_standings(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of basketballStandings in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(
        use_case="sport", function_key="basketballStandings", similarity=1, parsed_text="lorem ipsum"
    )
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(
        basketballApi,
        "get_nba_standings",
        return_value=[
            ["LA Lakers", "Boston Celtics", "Miami Heat"],
            ["Golden State Warriors", "Houston Rockets", "Denver Nuggets"],
        ],
    )
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    # spy_tts_convert_text.assert_called_with("Team A vs. Team B")
    assert spy_tts_convert_text.call_args_list[1][0][0] == "LA Lakers"
    assert spy_tts_convert_text.call_args_list[5][0][0] == "Golden State Warriors"

    mocker.patch.object(basketballApi, "get_nba_standings", return_value=None)
    with pytest.raises(Exception, match="Could not get NBA standings"):
        use_case.trigger_assistant(best_match)


def test_basketball_game_today(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of basketballTeamGameToday in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(
        use_case="sport", function_key="basketballTeamGameToday", similarity=1, parsed_text="lorem ipsum"
    )
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(
        basketballApi,
        "get_nba_teams",
        return_value=[["LA Lakers", "Boston Celtics", "Miami Heat"]],
    )
    mocker.patch.object(
        basketballApi,
        "get_team_game_today",
        return_value=[["Team A vs. Team B"]],
    )
    mocker.patch.object(SportUseCase, "choose_team", return_value="LA Lakers")
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    # spy_tts_convert_text.assert_called_with("Team A vs. Team B")
    assert spy_tts_convert_text.call_args_list[0][0][0][0] == "Team A vs. Team B"

    mocker.patch.object(basketballApi, "get_team_game_today", return_value=None)
    with pytest.raises(Exception, match="Could not get basketball game"):
        use_case.trigger_assistant(best_match)

    mocker.patch.object(basketballApi, "get_team_game_today", return_value=[])
    use_case.trigger_assistant(best_match)
    spy_tts_convert_text.assert_called_with("The LA Lakers have no games today.")

    mocker.patch.object(basketballApi, "get_nba_teams", return_value=None)
    with pytest.raises(Exception, match="Could not get NBA teams"):
        use_case.trigger_assistant(best_match)


def test_handball_standings(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of handballStandings in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(use_case="sport", function_key="handballStandings", similarity=1, parsed_text="lorem ipsum")
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    mocked_sport_choose_league = mocker.patch.object(SportUseCase, "choose_league", return_value="Bundesliga")
    # * Patch Event Api
    mocker.patch.object(
        handballApi,
        "get_league_table",
        return_value=[["1. Fuchse Berlin 5", "2. Rhein Neckar Loewen 3"]],
    )
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    mocked_sport_choose_league.assert_called_once_with(["Bundesliga", "Starligue", "Liga ASOBAL"])
    assert spy_tts_convert_text.call_args_list[0][0][0][0] == "1. Fuchse Berlin 5"
    assert spy_tts_convert_text.call_args_list[0][0][0][1] == "2. Rhein Neckar Loewen 3"

    mocker.patch.object(handballApi, "get_league_table", return_value=None)
    with pytest.raises(Exception, match="Could not get handball standings"):
        use_case.trigger_assistant(best_match)


def test_handball_game_today(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of handballTeamGameToday in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(
        use_case="sport", function_key="handballTeamGameToday", similarity=1, parsed_text="lorem ipsum"
    )
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    mocked_sport_choose_league = mocker.patch.object(SportUseCase, "choose_league", return_value="Bundesliga")
    # * Patch Event Api
    mocker.patch.object(
        handballApi,
        "get_league_teams",
        return_value=[["Fuchse Berlin", "Rhein Neckar Loewen", "Tus N-Lübbecke"]],
    )
    mocker.patch.object(
        handballApi,
        "get_team_game_today",
        return_value=[["Fuchse Berlin vs. Rhein Neckar Loewen"]],
    )
    mocker.patch.object(SportUseCase, "choose_team", return_value="Fuchse Berlin")
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)
    use_case.trigger_assistant(best_match)

    mocked_sport_choose_league.assert_called_with(["Bundesliga", "Starligue", "Liga ASOBAL"])
    # spy_tts_convert_text.assert_called_with("Team A vs. Team B")
    assert spy_tts_convert_text.call_args_list[0][0][0][0] == "Fuchse Berlin vs. Rhein Neckar Loewen"

    mocker.patch.object(handballApi, "get_team_game_today", return_value=None)
    with pytest.raises(Exception, match="Could not get handball game"):
        use_case.trigger_assistant(best_match)

    mocker.patch.object(handballApi, "get_team_game_today", return_value=[])
    use_case.trigger_assistant(best_match)
    spy_tts_convert_text.assert_called_with("The Fuchse Berlin have no games today.")

    mocker.patch.object(handballApi, "get_league_teams", return_value=None)
    with pytest.raises(Exception, match="Could not get handball teams"):
        use_case.trigger_assistant(best_match)


def test_f1_round_results(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of f1ResultsByRound in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(use_case="sport", function_key="f1ResultsByRound", similarity=1, parsed_text="lorem ipsum")
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(
        f1Api,
        "get_results_by_round",
        return_value=[["1. Hamilton", "2. Vettel", "3. Bottas", "4. Verstappen"]],
    )
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)

    with patch("builtins.input", return_value="2"):
        use_case.trigger_assistant(best_match)
        assert spy_tts_convert_text.call_args_list[1][0][0][0] == "1. Hamilton"
        assert spy_tts_convert_text.call_args_list[1][0][0][3] == "4. Verstappen"

        mocker.patch.object(f1Api, "get_results_by_round", return_value=None)
        with pytest.raises(Exception, match="Could not get results"):
            use_case.trigger_assistant(best_match)


def test_f1_last_round_results(mocker: MockFixture, patch_stt: SpeechToText, patch_tts: TextToSpeech) -> None:
    """Test the case of f1LastRoundResult in the sport use case

    Parameters
    ----------
    mocker : MockFixture
        General MockFixture Class
    patch_stt : SpeechToText
        Patched class to instantiate use_case class
    patch_tts : TextToSpeech
        Patched class to instantiate use_case class
    """
    best_match = BestMatch(use_case="sport", function_key="f1LastRoundResult", similarity=1, parsed_text="lorem ipsum")
    # Set up the test case
    user = User(
        name="TestUser",
        age=10,
        address=Address(street="Pfaffenwaldring 45", city="Stuttgart", zip_code=70569, country="DE", vvs_id=""),
        possessions=Possessions(bike=True, car=False),
        favorites=Favorites(
            stocks=[],
            league="",
            team="",
            news_keywords=[""],
            wakeup_time=datetime.now(),
        ),
    )

    # * Patch Event Api
    mocker.patch.object(
        f1Api,
        "get_results_last_round",
        return_value=[["1. Verstappen", "2. Vettel", "3. Bottas", "4. Hamilton"]],
    )
    spy_tts_convert_text = mocker.spy(patch_tts, "convert_text")
    use_case = SportUseCase(patch_stt, patch_tts, "TestBuddy", user)

    use_case.trigger_assistant(best_match)
    assert spy_tts_convert_text.call_args_list[1][0][0][0] == "1. Verstappen"
    assert spy_tts_convert_text.call_args_list[1][0][0][3] == "4. Hamilton"

    mocker.patch.object(f1Api, "get_results_last_round", return_value=None)
    with pytest.raises(Exception, match="Could not get results"):
        use_case.trigger_assistant(best_match)
