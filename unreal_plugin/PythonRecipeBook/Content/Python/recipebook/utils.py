"""
This module is meant for miscellaneous utilities that I found useful
"""


import json
from pathlib import Path
import unreal

from recipebook.unreal_systems import EditorAssetLibrary


# module caches to store asset / class information
# this will save us from repeatedly searching for or loading unreal data
asset_class_cache = {}

def new_instance_from_asset(asset):
    """
    Create a new Python instance of the given Asset or string asset path

    This is useful for Editor Utility Widget tools, often times you
    want to use custom Blueprint Assets to store UI item data. This method
    lets you create that BP class in your Content Browser, initialize it
    in Python, set its

    parameters:
        asset: A loaded Content Browser Asset or its string asset_path

    Return:
        a new Python instance of the asset's class
    """
    global asset_class_cache

    # Check if the asset is already cached
    asset_path = asset if isinstance(asset, str) else asset.get_path_name()
    if not asset_class_cache.get(asset_path):

        # Load the asset if an asset path was provided to the function
        if isinstance(asset, str):
            if EditorAssetLibrary.does_asset_exist(asset):
                asset = EditorAssetLibrary.load_asset(asset)
            else:
                unreal.log_error(f"The given asset path does not exist: {asset}")
                return

        # cache the loaded asset's generated class:
        asset_class_cache[asset_path] = asset.generated_class()

    # return a new instance of the asset's class:
    return unreal.new_object(asset_class_cache[asset_path])


def save_user_prefs(prefs_name, prefs_data):
    """save some basic prefs data"""

    # Convert the unreal Map to a json compliant dict
    prefs = {
        str(key): str(value)
        for key, value in prefs_data.items()
    }

    # we'll save this file to the users' tmp dir under 'unreal/unreal_prefs_<pref>.json'
    prefs_file = Path(
        unreal.Paths.project_saved_dir(),
        "pytemp",
        f"unreal_prefs_{prefs_name}.json"
    )

    if not prefs_file.exists():
        prefs_file.parent.mkdir(parents=True, exist_ok=True)

    with prefs_file.open("w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2)


def load_user_prefs(prefs_name) :
    """load some basic prefs data"""

    # use the same path structure as the save and make sure it exists
    prefs_file = Path(
        unreal.Paths.project_saved_dir(),
        "pytemp",
        f"unreal_prefs_{prefs_name}.json"
    )
    if not prefs_file.exists():
        return {}

    # we can return the dict as-is, Unreal will convert it to a Map(str,str) for us
    return json.loads(prefs_file.read_text())