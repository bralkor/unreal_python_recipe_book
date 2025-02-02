"""
functions used by the Meta Viewer tool in Unreal
"""


from pathlib import Path

import unreal

from recipebook import (
    metadata,
    utils
)


def get_item_data_for_euw():
    """
    get the list of data objects to add to an Unreal List View
    """

    # The template asset path for our item data
    item_template_path = "/PythonRecipeBook/sample_tools/widgets/meta_item_data"

    # use arbitrary icons from the icons python dir
    fp = Path(__file__).parent
    icon_dir = fp.joinpath("icons")
    icons = {
        icon.stem: str(icon.as_posix())
        for icon in icon_dir.iterdir()
    }

    # get all of our managed assets (using the default arg for "is_managed_asset")
    meta_query = {metadata.META_IS_MANAGED_ASSET: True}
    assets = metadata.find_assets_by_metadata(meta_query, class_names=["Blueprint"])
    if not assets:
        return []

    items = []
    for asset in assets:
        # Create a new Python instance of the template asset
        item = utils.new_instance_from_asset(item_template_path)
        name = metadata.get_metadata(asset, metadata.META_ASSET_NAME)

        # feed the desired asset metadata into our item
        item.set_editor_properties({
            "name": name,
            "type": metadata.get_metadata(asset, metadata.META_ASSET_TYPE),
            "group": metadata.get_metadata(asset, metadata.META_ASSET_GROUP),
            "version": metadata.get_metadata(asset, metadata.META_ASSET_VERSION),
            "asset_path": str(asset.package_name),
            "image_path": icons.get(name[-1])
        })
        items.append(item)

    # return the list of ready-to-use item data in our EUW!
    return items


def filter_item_data(items, type_filter, group_filter, name_filter):
    """filter the given list of meta_item_data entries"""

    # nested function to make the list comprehension cleaner
    # only use the filter if it's valid, otherwise skip it (return True)
    def check_filter_match(a, b): return str(a) == str(b) if a else True

    return [
        item
        for item in items
        if check_filter_match(type_filter, item.get_editor_property("type"))
        and check_filter_match(group_filter, item.get_editor_property("group"))
        and name_filter.lower() in str(item.get_editor_property("name")).lower()
    ]
