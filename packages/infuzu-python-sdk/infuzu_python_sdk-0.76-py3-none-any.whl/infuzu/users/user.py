import datetime
from pydantic import (Field, EmailStr, PositiveInt)
from pydantic_core import Url
from pydantic_extra_types.phone_numbers import PhoneNumber
from requests import Response
from .. import constants
from ..base import BaseInfuzuObject
from ..errors.base import InfuzuError
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


USER_CACHE: CacheSystem = CacheSystem(default_expiry_time=300)


class User(BaseInfuzuObject):
    user_id: str | None = Field(frozen=True)
    username: str | None = Field(frozen=True)
    email: EmailStr | None = Field(frozen=True)
    email_privacy_settings: str | None = Field(frozen=True)
    email_privacy_settings_display: str | None = Field(frozen=True)
    profile_photo: Url | None = Field(frozen=True)
    profile_photo_privacy_settings: str | None = Field(frozen=True)
    profile_photo_privacy_settings_display: str | None = Field(frozen=True)
    first_name: str | None = Field(frozen=True)
    middle_name: str | None = Field(frozen=True)
    last_name: str | None = Field(frozen=True)
    name_privacy_settings: str | None = Field(frozen=True)
    name_privacy_settings_display: str | None = Field(frozen=True)
    nickname: str | None = Field(frozen=True)
    nickname_privacy_settings: str | None = Field(frozen=True)
    nickname_privacy_settings_display: str | None = Field(frozen=True)
    date_of_birth: datetime.date | None = Field(frozen=True)
    date_of_birth_privacy_settings: str | None = Field(frozen=True)
    date_of_birth_privacy_settings_display: str | None = Field(frozen=True)
    gender: str | None = Field(frozen=True)
    gender_privacy_settings: str | None = Field(frozen=True)
    gender_privacy_settings_display: str | None = Field(frozen=True)
    phone_number: PhoneNumber | None = Field(frozen=True)
    phone_number_privacy_settings: str | None = Field(frozen=True)
    phone_number_privacy_settings_display: str | None = Field(frozen=True)
    record_storage_used: PositiveInt | None = Field(frozen=True)
    total_storage_used: PositiveInt | None = Field(frozen=True)
    cogitobot_storage_used: PositiveInt | None = Field(frozen=True)
    preferred_theme: str | None = Field(frozen=True)
    preferred_theme_display: str | None = Field(frozen=True)
    billing_in_good_status: bool | None = Field(frozen=True)
    signup_source: str | None = Field(frozen=True)
    policy_acceptance_version: datetime.date | None = Field(frozen=True)
    marketing_consent: bool | None = Field(frozen=True)

    @classmethod
    def retrieve(cls, user_id: str, force_new: bool = False) -> 'User':
        def get_user() -> 'User':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.USERS_BASE_URL}{constants.USERS_RETRIEVE_USER_ENDPOINT}"
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise InfuzuError(f"Error retrieving user: {api_response.text}")
        return USER_CACHE.get(
            cache_key_name=f'retrieve-{user_id}', specialized_fetch_function=get_user, force_new=force_new
        )
