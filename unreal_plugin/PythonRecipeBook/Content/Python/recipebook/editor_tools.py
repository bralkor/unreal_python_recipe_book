"""
This Module covers examples of managing Editor Utility Widgets (Editor Tools)
"""

from recipebook.unreal_systems import (
    EditorAssetLibrary,
    EditorUtilitySubsystem
)

import unreal


def launch_editor_utility_widget(asset_path: str):
    """Launch the given utility widget from its asset path"""

    # ensure a valid asset path was provided
    if not isinstance(asset_path, str):
        unreal.log_error(f"The given input is not an asset path: {asset_path}")
        return

    if not EditorAssetLibrary.does_asset_exist(asset_path):
        unreal.log_error(f"The given asset path does not exist: {asset_path}")
        return

    # open the EUW
    asset = EditorAssetLibrary.load_asset(asset_path)
    EditorUtilitySubsystem.spawn_and_register_tab(asset)
