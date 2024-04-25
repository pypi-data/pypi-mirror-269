# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Optional

from contrast.reporting.teamserver_responses.sampling import Sampling
from contrast.utils.decorators import cached_property


class NGServerSettings:
    def __init__(self, features: Optional[dict] = None):
        self.features = features or {}

    @cached_property
    def log_file(self) -> str:
        return self.features.get("features", {}).get("logFile", "")

    @cached_property
    def log_level(self) -> str:
        return self.features.get("features", {}).get("logLevel", "")

    @cached_property
    def assess_enabled(self) -> bool:
        return (
            self.features.get("features", {})
            .get("assessment", {})
            .get("enabled", False)
        )

    @cached_property
    def protect_enabled(self) -> bool:
        return self.features.get("features", {}).get("defend", {}).get("enabled", False)

    @cached_property
    def sampling(self) -> Sampling:
        return Sampling(
            self.features.get("features", {})
            .get("assessment", {})
            .get("sampling", None),
            True,
        )
