"""
Metadata is a powerful tool when managing assets in Unreal. Instead of searching/recursing
through folders we can search and filter for assets by their metadata values.

This module includes examples to make use of and extend the functionality of metadata

PRE-REQUISITE:
    Metadata names must be declared first in the Asset Registry for your given Unreal Project
    You can add / manage your metadata names in the Game Project's Settings -> Asset Registry -> Metadata

    Plugins can also deliver metadata in the `Config/Default<plugin_name>.ini` file
"""

import sys
import unreal
from .unreal_systems import (
    asset_registry_helper,
    asset_registry,
    EditorAssetLibrary
)


# Arbitrary metadata example: let's pretend we're tracking assets!
# NOTE:
#     these constants should be 1:1 with what's declared in your Project's Asset Registry
#     Any metadata names only declared in Python are not discoverable by the Asset Registry
META_IS_MANAGED_ASSET = "managed_asset"  # all assets we create via Python will have this tag
META_ASSET_TYPE       = "asset_type"     # maybe it's a 'character' or an 'environment' asset
META_ASSET_GROUP      = "asset_group"    # we can use this to collect multiple assets under the same group
META_ASSET_NAME       = "asset_name"     # the official name of our asset
META_ASSET_AUTHOR     = "asset_author"   # who's the creator of this asset?
META_ASSET_VERSION    = "asset_version"  # what version number is this asset currently set to?


# Unreal stores metadata as strings
# this dict maps metadata names we want to be non-strings
# we can use this to get metadata as their expected type (such as an int or bool)
METADATA_TYPE_MAP = {
    META_IS_MANAGED_ASSET: bool,
    META_ASSET_VERSION: int
}


def set_metadata(asset, key, value):
    """
    Setting Metadata is done on a loaded unreal.Object reference

    parameters:
        asset: the asset to save the metadata to
        key:   the metadata key name
        value: the metadata value
    """
    EditorAssetLibrary.set_metadata_tag(asset, key, str(value))


def get_metadata(asset, key, default=None):
    """
    Getting Metadata can be done on a loaded unreal.Object reference OR unreal.AssetData

    using METADATA_TYPE_MAP we can automatically convert
    our metadata into their intended types (if not string)

    parameters:
        asset: the asset to get the metadata from
        key:   the metadata key name
        default: the default value to assume if the metadata is not set

    Return:
        the metadata value in its expected type (if mapped in METADATA_TYPE_MAP)
    """
    # Get the metadata value from the loaded asset or an AssetData instance
    if isinstance(asset, unreal.AssetData):
        value = asset.get_tag_value(key)
    else:
        value = EditorAssetLibrary.get_metadata_tag(asset, key)

    if value and value.lower != "none":
        # Get this metadata key's expected value type:
        value_type = METADATA_TYPE_MAP.get(key, str)

        if value_type == bool:
            # bools are a special case as bool(str) only checks for length
            return value.lower() == "true"
        else:
            # most value types may be directly converted
            return value_type(value)

    return default


def find_assets_by_metadata(metadata=None, class_names=None):
    """
    Find assets in our project's Content Browser
    based on a given dict of metadata key:value pairs

    parameters:
        metadata:    a dict of metadata key:value pairs to search by
        class_names: a list of class names to filter by

    Return:
        a list of AssetData items that match the given metadata / class names
    """
    if metadata is None:
        metadata = {META_IS_MANAGED_ASSET: True}

    if class_names is None:
        class_names = ["object"]

    # create a basic Asset Registry filter:
    base_filter = unreal.ARFilter(
        class_names=class_names,
        recursive_classes=True
    )

    # get the initial search results using the base filter:
    results = asset_registry.get_assets(base_filter) or []

    # filter the results to only those matching the given metadata key:value pairs
    for key, value in metadata.items():
        # Convert the key:value pair and create a metadata based filter:
        query = unreal.TagAndValue(key, str(value))
        meta_filter = asset_registry_helper.set_filter_tags_and_values(base_filter, [query])

        # reduce the results to only those matching the given metadata
        results = asset_registry.run_assets_through_filter(results, meta_filter) or []
        if not results:
            break

    # return the results as a sorted Python list
    return [i for i in sorted(results, key=lambda x: x.package_name)]



def metadata_startup():
    """
    Register the metadata names to the Asset Registry during Editor startup

    Using this method ensures the Metadata components of any tools we build will work properly.
    While it is possible to declare these in the plugin's INI file this method has been
    more reliable in my experience when making tools. It also allows us to set the metadata
    from the same code
    """
    # the metadata keys to register to the Asset Registry
    metadata_keys = [
        META_IS_MANAGED_ASSET,
        META_ASSET_TYPE,
        META_ASSET_GROUP,
        META_ASSET_NAME,
        META_ASSET_AUTHOR,
        META_ASSET_VERSION
    ]

    # this custom c++ function exposes the ability to add metadata keys directly to the Asset Registry
    unreal.PythonUtilsLibrary.register_metadata_tags(metadata_keys)
