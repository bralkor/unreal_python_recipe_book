"""
This module is meant for miscellaneous utilities that I found useful
"""


import unreal

from .unreal_systems import EditorAssetLibrary


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
