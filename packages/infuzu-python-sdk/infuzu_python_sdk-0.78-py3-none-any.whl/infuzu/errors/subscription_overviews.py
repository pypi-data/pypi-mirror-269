from .base import (InfuzuError, InputFormatError, InputValueError)


class SubscriptionOverviewError(InfuzuError):
    pass


class SubscriptionOverviewDatetimeParsingError(SubscriptionOverviewError, InputFormatError):
    pass


class SubscriptionOverviewInvalidDatetimeRangeError(SubscriptionOverviewError, InputValueError):
    pass
