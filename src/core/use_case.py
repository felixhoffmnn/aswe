from loguru import logger


class UseCases:
    def __init__(self):
        logger.debug("UseCases initialized")
        pass

    def _morning_briefing(self):
        # API: News, Weather, Sport, Stocks, Calendar, etc.
        pass

    def _events(self):
        # API: Calendar, Weather, Events, etc.
        pass

    def _transportation(self):
        # API: Weather, Navigation, Calendar etc.
        pass

    def evaluate_input(self, input):
        print(input)


def morning_briefing():
    pass


def events():
    pass


def transportation():
    pass
