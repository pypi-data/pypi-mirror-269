from typing import Any
from deprecated import deprecated
from pydantic import (Field, PositiveInt)
from pydantic_core import Url
from requests import Response
from ... import constants
from ...base import BaseInfuzuObject
from ...errors.base import InfuzuError
from ...http_requests import signed_requests
from ...utils.enums.api_calls import HttpMethod
from ..errors import NoContentError


class Assignment(BaseInfuzuObject):
    rule_id: str | None = Field(frozen=True)
    url: Url | None = Field(frozen=True)
    private_key_b64: str | None = Field(frozen=True)
    http_method: HttpMethod | None = Field(frozen=True, default=HttpMethod.GET)
    headers: dict[str, Any] | None = Field(frozen=True, default=None)
    body: dict[str, Any] | None = Field(frozen=True, default=None)
    max_retries: PositiveInt | None = Field(frozen=True, default=0)
    timeout: PositiveInt | None = Field(frozen=True, default=30)

    @classmethod
    @deprecated(version='0.77', reason="Use standard pydantic options instead")
    def from_dict(cls, assignment_dict: dict[str, any]) -> 'Assignment':
        rule_id: str = assignment_dict.get("rule_id")
        url: str = assignment_dict.get("url")
        private_key_b64: str = assignment_dict.get("private_key_b64")
        http_method: str = assignment_dict.get("http_method")
        headers: dict[str, any] | None = assignment_dict.get("headers")
        body: dict[str, any] | None = assignment_dict.get("body")
        max_retries: int = assignment_dict.get("max_retries")
        timeout: int = assignment_dict.get("timeout")

        http_method: HttpMethod = HttpMethod(http_method)

        return cls(
            rule_id=rule_id,
            url=url,
            private_key_b64=private_key_b64,
            http_method=http_method,
            headers=headers,
            body=body,
            max_retries=max_retries,
            timeout=timeout
        )

    @deprecated(version='0.77', reason="Use standard pydantic options instead")
    def to_dict(self) -> dict[str, any]:
        return {
            "rule_id": self.rule_id,
            "url": self.url,
            "http_method": self.http_method,
            "headers": self.headers,
            "body": self.body,
            "max_retries": self.max_retries,
            "timeout": self.timeout
        }

    @classmethod
    def retrieve(cls):
        response: Response = signed_requests.get(
            url=f"{constants.CLOCKWISE_BASE_URL}{constants.CLOCKWISE_RETRIEVE_ASSIGNMENT_ENDPOINT}"
        )
        if response.status_code == 200:
            return Assignment(**response.json())
        elif response.status_code == 204:
            raise NoContentError()
        raise InfuzuError(
            f"Status Code: {response.status_code}, Content: {response.content}"
        )


@deprecated(version='0.77', reason="Use Assignment.retrieve() instead")
def get_assignment() -> Assignment:
    return Assignment.retrieve()
