# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Optional

from contrast.reporting.teamserver_responses.sampling import Sampling
from contrast.utils.decorators import cached_property


class ServerSettings:
    """
    This class is responsible for safely parsing V1 TeamServer Server Settings from a response to a usable format.
    The format can be found here: https://github.com/Contrast-Security-Inc/contrast-agent-api-spec. At the time of the
    creation of this class, the specific schema is ServerSettings in agent-endpoints.yml.
    """

    def __init__(self, server_settings_json: Optional[dict] = None):
        self.server_settings_json = server_settings_json or {}

    @cached_property
    def log_file(self) -> Optional[str]:
        return self.server_settings_json.get("logger", {}).get("path", None)

    @cached_property
    def log_level(self) -> Optional[str]:
        return self.server_settings_json.get("logger", {}).get("level", None)

    @cached_property
    def assess_enabled(self) -> bool:
        return self.server_settings_json.get("assess", {}).get("enable", False)

    @cached_property
    def protect_enabled(self) -> bool:
        return self.server_settings_json.get("protect", {}).get("enable", False)

    @cached_property
    def sampling(self) -> Optional[Sampling]:
        return Sampling(
            self.server_settings_json.get("assess", {}).get("sampling", None), False
        )
