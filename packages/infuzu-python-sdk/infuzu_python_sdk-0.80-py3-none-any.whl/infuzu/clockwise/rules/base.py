from dataclasses import dataclass
from datetime import (timedelta, datetime, timezone)
from pydantic import Field
from ...base import BaseInfuzuObject
from ...utils.enums.api_calls import HttpMethod


def _now_utc() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class Rule(BaseInfuzuObject):
    name: str | None = Field(frozen=True)
    url: str | None = Field(frozen=True)
    rule_id: str | None = Field(frozen=True, default=None)
    interval: timedelta | None = Field(frozen=True, default=timedelta(days=1))
    start_datetime: datetime | None = Field(frozen=True, default=_now_utc)
    end_datetime: datetime | None = Field(frozen=True, default=None)
    max_executions: int | None = Field(frozen=True, default=None)
    http_method: HttpMethod | None = Field(frozen=True, default=HttpMethod.GET)
    headers: dict | None = Field(frozen=True, default=None)
    body: dict | None = Field(frozen=True, default=None)
    max_retries: int | None = Field(frozen=True, default=0)
    timeout: int | None = Field(frozen=True, default=30)
    static: bool | None = Field(frozen=True, default=False)

    def to_create_rule_dict(self) -> dict[str, any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "interval": self.interval.total_seconds(),
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat() if isinstance(self.end_datetime, datetime) else None,
            "max_executions": self.max_executions,
            "url": self.url,
            "http_method": self.http_method.name,
            "headers": self.headers,
            "body": self.body,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "static": self.static
        }


# TODO move this over to the pydantic type
@dataclass
class CreatedRule:
    id: str
    key_pair_id: str
    public_key: str
