"""
This module provides examples for handling Unreal Engine versions and discovering Python API changes
"""

from functools import total_ordering
import json
from pathlib import Path

import unreal


PYTHON_DATA_DIR = Path(unreal.SystemLibrary.get_platform_user_dir()) / "unreal/engine_python_data/"
PYTHON_DATA_DIR.mkdir(exist_ok=True)


@total_ordering
class EngineVersion:
    """
    Utility class to compare Unreal Versions

    Provide the engine version formatted as "5" , "5.0" , or "5.0.0"
    or leave empty to use the current Unreal Editor session's version
    """

    def __init__(self, version: str = ""):
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
        return self.major*1000000 + self.minor*1000 + self.patch

    @property
    def version(self) -> str:
        """The string value of the engine version (human readable)"""
        return f"{self.major}.{self.minor}.{self.patch}"

    # The @total_ordering decorator will use __lt__ and __eq__ to make
    # the rest of our comparison functions
    def __lt__(self, other: 'EngineVersion') -> bool:
        if not isinstance(other, EngineVersion):
            raise ValueError(f"{other} must be of type EngineVersion!")

        return self.value < other.value

    def __eq__(self, other) -> bool:
        if not isinstance(other, EngineVersion):
            raise ValueError(f"{other} must be of type EngineVersion!")

        return self.value == other.value

    # repr to provide a cleaner debug printout ~ ex: EngineVersion("5.3.0")
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\"{self.version}\")"


def compare_unreal_python_versions(source_version: str, target_version: str = "") -> dict:
    """
    Compare what's changed between two engine versions of Unreal for the Python API
    This will return a dictionary of everything that's been added to the TARGET version

    collect_python_class_data() must be run from each UE version you wish to compare

    parameters:
        source_version: the BEFORE engine version to compare from, formatted as "5" "5.0" or "5.0.0"
        target_version: the AFTER engine version to compare to, formatted as "5" "5.0" or "5.0.0"

    return:
        Dict of new classes and properties only found in the target version
    """
    source = EngineVersion(source_version)
    target = EngineVersion(target_version)

    source_file = PYTHON_DATA_DIR / (source.version.replace(".", "_") + ".json")
    target_file = PYTHON_DATA_DIR / (target.version.replace(".", "_") + ".json")

    # Alert the user if either file is missing
    if not source_file.exists() or not target_file.exists():
        existing_data = f"\n\t".join([
            i.stem.replace("_", ".")
            for i in PYTHON_DATA_DIR.iterdir()
        ])
        raise FileNotFoundError(
            f"One or both Unreal Versions do not have Python Class data on disk."
            f"\nProvided:\n\t{source.version}\n\t{target.version}"
            f"\nAvailable Unreal Versions to compare:"
            f"\n\t{existing_data}"
        )

    # load the json data
    source_data = json.loads(source_file.read_text())
    target_data = json.loads(target_file.read_text())

    # collect all new properties/classes
    new_properties = {}
    for class_name, properties in target_data.items():
        # If the class didn't exist in the older version we can add everything
        if class_name not in source_data:
            new_properties[class_name] = properties
        # Otherwise, check each property to see which (if any) are new
        else:
            added_properties = [p for p in properties if p not in source_data[class_name]]
            if added_properties:
                new_properties[class_name] = added_properties

    return new_properties


def collect_python_class_data():
    """
    Harvest the Unreal Python classes & properties and write them to disk

    This function must be run in a given Unreal version prior to using it in compare_unreal_python_versions()
    """
    current_version = EngineVersion().version.replace(".", "_")

    class_data = {}
    for class_name in sorted(dir(unreal)):
        class_obj = getattr(unreal, class_name)
        properties = [i for i in dir(class_obj) if not i.endswith("__")]
        if properties:
            class_data[class_name] = sorted(properties)

    data_file = PYTHON_DATA_DIR / f"{current_version}.json"
    with data_file.open("w", encoding="utf-8") as f:
        json.dump(class_data, f, indent=2)
