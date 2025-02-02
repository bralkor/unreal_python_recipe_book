"""
This module provides examples for handling Unreal Engine versions and discovering Python API changes
"""

from functools import total_ordering

import unreal


@total_ordering
class EngineVersion:
    """
    Utility class to compare Unreal Versions

    Provide the engine version formatted as "5" , "5.0" , "5.0.0"
    or leave empty to use the current Unreal Editor session's version
    """

    def __init__(self, version: str = ""):
        version = str(version)

        # Get the current UE session's version if not provided
        if not version:
            version_info = str(unreal.SystemLibrary.get_engine_version())
            version = version_info.split("-", 1)[0]

        # Collect the version IDs
        version_ids = version.split(".")
        if not len(version_ids) or not all([i.isdigit() for i in version_ids]):
            raise ValueError(
                f"EngineVersion was provided '{version}' - must be in the format of '5' , '5.0' , or '5.0.0'"
            )

        # Store the version data
        version_ids = [int(i) for i in version_ids]
        version_ids.extend([0, 0])
        self.major, self.minor, self.patch = version_ids[0:3]

    @property
    def value(self) -> int:
        """The numeric value of the engine version (used for comparison)"""
        return self.major * 1000000 + self.minor * 1000 + self.patch

    @property
    def version(self) -> str:
        """The string value of the engine version (human-readable)"""
        version_string = f"{self.major}.{self.minor}"
        if self.patch:
            version_string += f".{self.patch}"
        return version_string

    # The @total_ordering decorator will use __lt__ and __eq__ to make
    # the rest of our comparison functions
    def __lt__(self, other: 'EngineVersion') -> bool:
        if isinstance(other, str) or isinstance(other, float):
            other = EngineVersion(other)
        if not isinstance(other, EngineVersion):
            raise ValueError(f"{other} must be of type EngineVersion!")
        return self.value < other.value

    def __eq__(self, other) -> bool:
        if isinstance(other, str) or isinstance(other, float):
            other = EngineVersion(other)
        if not isinstance(other, EngineVersion):
            raise ValueError(f"{other} must be of type EngineVersion!")
        return self.value == other.value

    # repr to provide a cleaner debug printout ~ ex: EngineVersion("5.3.0")
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\"{self.version}\")"
