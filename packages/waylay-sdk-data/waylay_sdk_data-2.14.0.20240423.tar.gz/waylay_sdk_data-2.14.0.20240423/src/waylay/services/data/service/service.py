"""Data Service."""

from waylay.sdk import ApiClient, WaylayService

from ..api.about_api import AboutApi
from ..api.events_api import EventsApi
from ..api.messages_api import MessagesApi
from ..api.series_api import SeriesApi


class DataService(WaylayService):
    """Data Service Class."""

    name = "data"
    title = "Data Service"

    about: AboutApi
    events: EventsApi
    messages: MessagesApi
    series: SeriesApi

    def __init__(self, api_client: ApiClient):
        """Create the data service."""

        super().__init__(api_client)
        self.about = AboutApi(api_client)
        self.events = EventsApi(api_client)
        self.messages = MessagesApi(api_client)
        self.series = SeriesApi(api_client)
