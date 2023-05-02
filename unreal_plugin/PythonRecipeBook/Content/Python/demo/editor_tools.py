"""
This Module covers examples of managing Editor Utility Widgets (Editor Tools)

An issue in Unreal is that any Editor Tools using Python-based Blueprint Nodes might be opened
before Python has been initialized during Unreal Startup. This module (and the added c++ code)
allows us to ensure Python has been fully initialized before they are opened

How the logic works:
  1) Whenever a managed Editor Tool is closed it will be removed from the official User Prefs
  2) The Editor Tool information will be cached by this module for 2 seconds
  3) After 2 seconds has passed the tool will be removed from the cache
  4) On Editor Close, any Editor Tools currently in the cache at that time will be written to a json file
  5) On Editor Open, this json file will be read to determine which Editor Tools to launch

Effectively, we're telling Unreal to ignore specified Editor Tools and managing them ourselves
during Editor shutdown / startup to ensure Python is fully initialized before they're opened.
"""

import json
from pathlib import Path

from .unreal_systems import (
    EditorAssetLibrary,
    EditorUtilitySubsystem
)

import unreal

# module cache to track recently closed tools
cache_delayed_editor_tool_shutdown = {}


def on_editor_tool_close(tool_path):
    """Manage the shutdown of Editor Tools that use Python-based nodes

    This will remove the tool from the official user prefs (EditorPerProjectUserSettings.ini)
    and cache the tool separately for Unreal shutdown/startup to safely relaunch the tool
    """

    # get the module cache
    global cache_delayed_editor_tool_shutdown

    # ensure the tool wasn't recently closed (skip if so)
    if cache_delayed_editor_tool_shutdown.get(tool_path):
        return

    # remove the editor tool from the official user prefs
    tool = unreal.find_asset(tool_path)
    unreal.PythonUtilsLibrary.clear_editor_tool_from_prefs(tool)

    # create & cache a callback that will track this tool for the next 2 seconds
    # by default the register_slate_post_tick_callback function only passes
    # the delta time to our declared function, by using a lambda
    # we can also have the callback track which blueprint path it's associated with
    cache_delayed_editor_tool_shutdown.setdefault(tool_path, {}).setdefault(
        "callback_id",
        unreal.register_slate_post_tick_callback(
            lambda x: cache_tracker_callback(tool_path, x)
        )
    )
    print(f"[editor_tool] Begin tracking {tool_path}...")


def cache_tracker_callback(tool_path, delay):
    """Callback to track how long a tool should be cached for"""

    # get the module cache
    global cache_delayed_editor_tool_shutdown

    # update the counter tracking how much time has passed since the tool was closed
    counter = cache_delayed_editor_tool_shutdown.setdefault(tool_path, {}).setdefault("time", 0.0)
    counter += delay
    cache_delayed_editor_tool_shutdown[tool_path]["time"] = counter

    # if more than 2 seconds has passed we can remove the tool from the cache
    # unregister the callback and then remove the cache entry
    if counter > 2:
        cid = cache_delayed_editor_tool_shutdown[tool_path].get("callback_id")
        if cid:
            unreal.unregister_slate_post_tick_callback(cid)
        del cache_delayed_editor_tool_shutdown[tool_path]
        print(f"[editor_tool] No longer tracking {tool_path}")


def get_cache_path():
    """
    The file location for the editor tool cache (json file)
    it should resolve to "{project dir}/Saved/pytemp/editor_tool_cache.json"
    """
    return Path(
        unreal.Paths.project_saved_dir(),
        "pytemp",
        "editor_tool_cache.json"
    )

def shutdown():
    """
    Read the cache on shutdown, any editor tools still present will be saved to a json file
    only tracks editor tools which make use of the "on editor tool close" node in their Destruct event
    """

    # get the module cache
    global cache_delayed_editor_tool_shutdown

    # get the list of tools currently in the module cache
    opened_tools = [x for x in cache_delayed_editor_tool_shutdown]

    # we'll save our editor tool cache in <project>/Saved/pytemp/editor_tool_cache.json
    cache_file = get_cache_path()
    
    # save the cache information to the json file
    with cache_file.open("w", encoding="utf-8") as f:
        json.dump({"tools_to_open": opened_tools}, f, indent=2)


def startup():
    """Open any editor tools from the previous editor session"""

    # get the cache file and check if it's valid
    cache_file = get_cache_path()
    if not cache_file.exists():
        return

    # loop through and launch our tools
    data = json.loads(cache_file.read_text())
    for tool in data.get("tools_to_open", []):
        print(f"Opening cached editor tool: {tool}")
        asset = EditorAssetLibrary.load_asset(tool)
        EditorUtilitySubsystem.spawn_and_register_tab(asset)

def launch_editor_utility_widget(asset):
    """
    Launch the given utility widget from a loaded object or its string asset path

    parameters:
        asset: A loaded Editor Utility Widget Asset or its string asset_path
    """

    # Load the editor utility widget if an asset path was provided to the function
    if isinstance(asset, str):
        if EditorAssetLibrary.does_asset_exist(asset):
            asset = EditorAssetLibrary.load_asset(asset)
        else:
            unreal.log_error(f"The given Editor Utility Widget path does not exist: {asset}")
            return

    # launch the editor utility widget and cache it
    EditorUtilitySubsystem.spawn_and_register_tab(asset)
