from aswe.core.data import BestMatch
from aswe.utils.classes import AbstractUseCase


class MorningBriefingUseCase(AbstractUseCase):
    """ "Use case for the morning briefing"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for morning briefing

        * TODO: Implement `quotes_key`

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
            case "newsSummary":
                raise NotImplementedError
            case _:
                raise NotImplementedError
