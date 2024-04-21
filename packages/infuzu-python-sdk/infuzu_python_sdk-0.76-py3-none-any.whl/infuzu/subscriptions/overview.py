from datetime import datetime
from requests import Response
from .. import constants
from ..base import BaseInfuzuObject
from ..errors.subscription_overviews import (
    SubscriptionOverviewError,
    SubscriptionOverviewDatetimeParsingError,
    SubscriptionOverviewInvalidDatetimeRangeError
)
from ..http_requests import signed_requests


class SubscriptionOverview(BaseInfuzuObject):
    id: str
    unique_users_subscribed: int
    owner_id: str

    @classmethod
    def retrieve(cls, start_time: datetime, end_time: datetime) -> list['SubscriptionOverview']:
        start_time_str: str = start_time.isoformat()
        end_time_str: str = end_time.isoformat()
        start_time_encoded: str = start_time_str.replace(':', '%3A')
        end_time_encoded: str = end_time_str.replace(':', '%3A')
        url: str = (
            f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTION_OVERVIEW}".replace(
                '<str:start_time>', start_time_encoded
            ).replace('<str:end_time>', end_time_encoded)
        )
        api_response: Response = signed_requests.request(method="GET", url=url)
        if api_response.status_code == 200:
            return [
                cls(
                    id=subscription_id, **subscription_overview
                ) for subscription_id, subscription_overview in api_response.json().items()
            ]
        elif api_response.status_code == 400:
            if api_response.json().get("error") == "datetime_parsing_error":
                raise SubscriptionOverviewDatetimeParsingError(api_response.json()["message"])
            elif api_response.json().get("error") == "invalid_datetime_range":
                raise SubscriptionOverviewInvalidDatetimeRangeError(api_response.json()["message"])
        raise SubscriptionOverviewError(f"Error retrieving subscription overview: {api_response.text}")
