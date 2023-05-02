"""
This is a Blueprint Function Library

When initialized it will add function nodes to Unreal that may be used in Blueprint Graphs
Python based BP functions are currently suited towards Editor Utilities, giving more access
to technical artists and developers to create editor tools and macros

Blueprint Function Libraries rely heavily on decorators, this module focuses
on exposing most of the available practical options in individual examples
"""


import json
import os
from pathlib import Path

import unreal

from . import (
    editor_tools,
    metadata,
    utils
)


@unreal.uclass()
class PyDemoBPLibrary(unreal.BlueprintFunctionLibrary):
    """
    Blueprint functions declared in this class will be available in Editor
    """

    # ---------      standard options     --------- #

    @unreal.ufunction(static=True)
    def basic_function_test():
        """Python Blueprint Node -- run Python logic!"""
        print("Running python!")
        pass


    @unreal.ufunction(static=True, params=[str])
    def input_test(user_input = "cool!"):
        """Python Blueprint Node -- print the text input"""
        print(f"Provided input: {user_input}")


    @unreal.ufunction(static=True, ret=str)
    def return_test():
        """Python Blueprint Node -- return a string!
        returns:
            str
        """
        return "cool!"


    @unreal.ufunction(static=True, params=[str, bool, int])
    def multiple_input_test(in_str, in_bool, in_int):
        """Python Blueprint Node -- multiple inputs (string, bool, int)"""
        print(f"{in_str} ({type(in_str)}) | {in_bool} ({type(in_bool)}) | {in_int} ({type(in_int)})")


    @unreal.ufunction(static=True, ret=(int, bool, str))
    def multiple_returns_test():
        """Python Blueprint Node -- Return (str, bool, int)

        NOTE: the 'ret' decorator arg is reversed from the actual python return
        """
        return "Awesome", True, 5


    @unreal.ufunction(static=True, ret=unreal.Array(str), params=[unreal.Array(str)])
    def sort_string_list_test(in_list):
        """
        Python Blueprint Node -- Sort a list of strings,
        useful for managing options in editor tools
        """
        return sorted(in_list)


    @unreal.ufunction(ret= str, pure=True, static=True)
    def pure_function_test() -> str:
        """Python Blueprint Node -- Pure functions have no execution flow pin connectors,
        a pure function is intended for getter functions that do not change the state of assets in Unreal
        """
        return os.environ.get("USER", "unknown user")


    # ---------      metadata options     --------- #

    @unreal.ufunction(static=True, meta=dict(Category="demo | category | sorting"))
    def meta_category_test():
        """Python Blueprint Node -- Category organizes this node in the BP Graph right click menu
        Use | to create sub-groupings to further organize complex libraries or place them with
        existing nodes in the BP Graph menu
        """
        pass


    @unreal.ufunction(static=True, meta=dict(KeyWords="random arbitrary keywords"))
    def meta_keywords_test():
        """Python Blueprint Node -- KeyWords help the discovery of this node in the BP Graph right click menu"""
        pass


    @unreal.ufunction(static=True, meta=dict(CompactNodeTitle="UEPY"))
    def meta_compact_name_test():
        """Python Blueprint Node -- CompactNodeTitle"""
        pass


    @unreal.ufunction(static=True, params=[unreal.Actor], meta=dict(DefaultToSelf="target_object"))
    def meta_default_to_self_test(target_object):
        """Python Blueprint Node -- DefaultToSelf (The BP Class calling this Function)"""
        print(f"target object: {target_object}")
        pass


    @unreal.ufunction(static=True, ret=(int, bool, str), meta=dict(HidePin="returnValue"))
    def multiple_returns_fixed_test():
        """Python Blueprint Node -- Return (str, bool, int)"""
        return "Awesome", True, 5


    # ---------      practical examples     --------- #

    @unreal.ufunction(
        static=True, ret=unreal.Array(unreal.EditorUtilityObject),
        params=[unreal.Array(unreal.EditorUtilityObject)],
        pure=True, meta=dict(Category="demo | EUW | item data", DeterminesOutputType="array_to_match")
    )
    def get_item_data_for_euw(array_to_match=unreal.Array(unreal.EditorUtilityObject)):
        """
        Python Blueprint Node -- Return the EUW Item Data,
        array_to_match is used to manage the return type
        this lets us return custom Blueprint Asset based classes directly
        """

        # The template asset path for our item data
        item_template_path = "/PythonRecipeBook/sample_tools/widgets/meta_item_data"

        # use arbitrary icons from the icons python dir
        fp = Path(__file__).parent
        icon_dir = fp.joinpath("icons")
        icons = {
            icon.stem: str(icon)
            for icon in icon_dir.iterdir()
        }

        # get all of our managed assets (using the default arg for "is_managed_asset")
        assets = metadata.find_assets_by_metadata(class_names=["Blueprint"])
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
                "image_path": icons.get(name[-1])
            })
            items.append(item)

        # return the list of ready-to-use item data in our EUW!
        return items


    @unreal.ufunction(
        static=True, ret=unreal.Array(unreal.EditorUtilityObject),
        params=[unreal.Array(unreal.EditorUtilityObject), str, str, str],
        pure=True, meta=dict(Category="demo | EUW | item data", DeterminesOutputType="items")
    )
    def filter_item_data(items, type_filter, group_filter, name_filter):
        """Python Blueprint Node -- filter the given list of meta_item_data entries"""

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


    @unreal.ufunction(
        static=True, params=[str, unreal.Map(str, str)],
        meta=dict(Category="demo | EUW | prefs")
    )
    def save_user_prefs(prefs_name, prefs_data):
        """Python Blueprint Node -- save some basic prefs data"""

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


    @unreal.ufunction(
        static=True, ret=unreal.Map(str, str), params=[str],
        pure=True, meta=dict(Category="demo | EUW | prefs")
    )
    def load_user_prefs(prefs_name) :
        """Python Blueprint Node -- load some basic prefs data"""

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


    @unreal.ufunction(
        static=True, params=[unreal.EditorUtilityWidget],
        meta=dict(Category="demo | EUW | prefs", DeterminesOutputType="editor_tool", DefaultToSelf="editor_tool")
    )
    def on_editor_tool_close(editor_tool):
        """Python Blueprint Node -- pass a widget's `self` reference to safely handle its Destruct

        Unreal caches any currently open editor tools to a UE user prefs file.
        During Unreal startup Unreal will open any tools listed in the UE user prefs
        before Python has been initialized, before any Python nodes have been generated.

        This function removes the editor tool from the UE user prefs and caches it separately,
        allowing us to properly launch the tool after Python has been initialized
        """

        # Get the asset path and pass it to the editor_tools module
        editor_tool_path = str(editor_tool.get_class().get_outer().get_path_name())
        editor_tools.on_editor_tool_close(editor_tool_path)
