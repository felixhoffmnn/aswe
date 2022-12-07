from datetime import datetime

import pycountry
from loguru import logger

from aswe.api.calendar import get_all_events_today
from aswe.api.finance import (
    get_currency_by_country,
    get_news_info_by_symbol,
    get_stock_price,
    get_stock_price_change,
    get_stock_rating,
    get_ticker_by_symbol,
)
from aswe.api.news import keyword_search, top_headlines_search
from aswe.api.weather.weather import dynamic_range
from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum
from aswe.core.objects import BestMatch
from aswe.utils.abstract import AbstractUseCase
from aswe.utils.error import TooManyRequests


class MorningBriefingUseCase(AbstractUseCase):
    """Use case for the morning briefing"""

    last_stock_prices: dict[str, float] = {}
    currency: tuple[str, str] = ("", "")

    def full_briefing(self) -> None:
        """Provides an overview of the calendar, news, weather and finance for the current day"""
        self.tts.convert_text(
            f"Good morning {self.user.name}! It's time to get up! Here is your morning briefing "
            "providing all the essential information to start into the day."
        )

        self.tts.convert_text("Now about your calendar:")
        self._calendar_overview()

        self.tts.convert_text("Let me give you a quick overview about some important news:")
        self._news_overview()

        self.tts.convert_text("Now let's have a look at the weather forecast:")
        self._weather_overview()

        self.tts.convert_text("And finally, here are some information about your stocks:")
        self._finance_overview()

        self.tts.convert_text("That was everything for today. Have a nice day!")

    def _calendar_overview(self) -> None:
        """Summarizes the calendar events for the current day"""
        events_today = get_all_events_today()
        if events_today is not None and len(events_today) > 0:
            self.tts.convert_text("Today you have the following calendar events:")
            for event in events_today:
                if event.location != "":
                    location_info = f" at {event.location}"
                else:
                    location_info = ""
                if event.full_day:
                    time_info = " all day"
                else:
                    start_time = datetime.strptime(event.start_time, "%Y-%m-%dT%H:%M:%S+01:00").strftime("%H:%M")
                    end_time = datetime.strptime(event.end_time, "%Y-%m-%dT%H:%M:%S+01:00").strftime("%H:%M")
                    time_info = f" from {start_time} to {end_time}"
                self.tts.convert_text(f"{event.title}{location_info}{time_info}")
        else:
            self.tts.convert_text("You do not have any calendar events today.")

    def _news_overview(self) -> None:
        """Reads out the top headlines for the current day including articles related to the user's keywords"""
        try:
            country_top_headlines = top_headlines_search(
                country=pycountry.countries.get(name=self.user.favorites.news_country).alpha_2, max_results=2
            )
        except TooManyRequests:
            self.tts.convert_text("Unfortunately, I could not find any news for you today.")
            return

        if country_top_headlines is not None:
            self.tts.convert_text("These are the top headlines in your country:")
            for headline in country_top_headlines:
                self.tts.convert_text(headline)

        keyword_headlines_list = [
            keyword_search(keyword=keyword, max_results=2) for keyword in self.user.favorites.news_keywords
        ]
        for keyword_headlines in keyword_headlines_list:
            if keyword_headlines is not None:
                self.tts.convert_text("You could also be interested in these headlines:")
                for headline in keyword_headlines:
                    self.tts.convert_text(headline)

        if country_top_headlines is None and all(
            keyword_headlines is None for keyword_headlines in keyword_headlines_list
        ):
            self.tts.convert_text("Unfortunately, I could not find any news for you today.")

    def _weather_overview(self) -> None:
        """Reads out the weather forecast for the current day"""
        weather = dynamic_range(
            location=f"{self.user.address.city},{pycountry.countries.get(name=self.user.address.country).alpha_2}",
            dynamic_period=DynamicPeriodEnum.TODAY,
            elements=[
                ElementsEnum.TEMP,
                ElementsEnum.TEMP_MIN,
                ElementsEnum.TEMP_MAX,
                ElementsEnum.PRECIP_PROB,
                ElementsEnum.FEELSLIKE,
                ElementsEnum.SUNRISE,
                ElementsEnum.SUNSET,
            ],
            include=[IncludeEnum.DAYS],
        )
        if weather is not None:
            weather_today = weather["days"][0]
            sunrise = datetime.strptime(weather_today["sunrise"], "%H:%M:%S").strftime("%H:%M")
            sunset = datetime.strptime(weather_today["sunset"], "%H:%M:%S").strftime("%H:%M")

            self.tts.convert_text(
                f"""Today it will be {weather_today['temp']} degrees Celsius (with a minimum of """
                f"""{weather_today['tempmin']} and a maximum of {weather_today['tempmax']}). This feels """
                f"""like {weather_today['feelslike']} degrees. The probability of precipitation is """
                f"""{weather_today['precipprob']} percent. The sun will rise at {sunrise} and set at {sunset}."""
            )
        else:
            self.tts.convert_text("Unfortunately, I could not find any weather information for you today.")

    def _finance_overview(self) -> None:
        """Reads out the stock prices, changes, ratings for the user's favorite stocks"""
        if self.currency == ("", ""):
            self.currency = get_currency_by_country(self.user.address.country)

        for stock in self.user.favorites.stocks:
            try:
                price = get_stock_price(stock["symbol"], self.currency[1])
                change = get_stock_price_change(stock["symbol"])
                rating = get_stock_rating(stock["symbol"])

                if all(response is None for response in [price, change, rating]):
                    self.tts.convert_text("Unfortunately, I could not find any information for you today.")
                else:
                    self.tts.convert_text(f"About {stock['name']}:")
                    if price is not None:
                        self.last_stock_prices[stock["symbol"]] = price
                        self.tts.convert_text(
                            f"The {stock['name']} stock is currently trading at {price} {self.currency[0]} per share."
                        )
                    if change is not None:
                        self.tts.convert_text(
                            f"""It has changed by {change['24h']} in the last 24 hours ({change['5D']}"""
                            """in the last 5 days)."""
                        )
                    if rating is not None:
                        self.tts.convert_text(f"The latest rating by analysts is {rating}.")
            except TooManyRequests:
                self.tts.convert_text("Unfortunately, I could not find any information about your stocks today.")
                return

    def _news_sentiment_info(self, stock: dict[str, str]) -> None:
        """Reads out the relevant headlines and their sentiment for a given stock"""
        try:
            news_info = get_news_info_by_symbol(stock["symbol"])
        except TooManyRequests:
            self.tts.convert_text("Unfortunately, I could not find any news sentiment information for you today.")
            return

        if news_info is not None:
            for news in news_info:
                symbol_ticker = get_ticker_by_symbol(news["ticker_sentiment"], stock["symbol"])
                self.tts.convert_text(
                    f"""The article '{news['title']}' written by {news['authors'][0]} and published """
                    f"""on {news['source']} implies a {symbol_ticker['ticker_sentiment_label']} sentiment."""
                )
            return
        else:
            self.tts.convert_text("Unfortunately, I could not find any news sentiment information for you today.")

    def check_proactivity(self) -> None:
        """Check if there is a proactivity to be triggered."""

        logger.debug("Evaluate proactivity in morning briefing use case")

        for stock in self.user.favorites.stocks:
            price = get_stock_price(stock["symbol"])
            if price is not None and self.last_stock_prices[stock["symbol"]] is not None:
                change = (price - self.last_stock_prices[stock["symbol"]]) / self.last_stock_prices[stock["symbol"]]
                if abs(change) >= 0.03:
                    self.tts.convert_text(
                        f"""I have breaking news about the {stock['name']} stock for you! The price has changed """
                        f"""significantly, {round(change * 100, 2)} percent since the last time I told you the """
                        f"""price. It is now trading at {round(price, 2)} {self.currency[0]} per share."""
                    )
                    self.last_stock_prices[stock["symbol"]] = price
                    self.tts.convert_text("Do you want to hear more about this?")
                    if self.stt.check_if_yes():
                        self._news_sentiment_info(stock)

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for morning briefing

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
            case "fullBriefing":
                self.full_briefing()
            case "news":
                self._news_overview()
            case "weather":
                self._weather_overview()
            case "calendar":
                self._calendar_overview()
            case "finance":
                self._finance_overview()
            case _:
                raise NotImplementedError
