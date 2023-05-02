"""
This module provides examples of running python code during Unreal startup and shutdown

There are three events handled in this module:
  1) pre_startup: run immediately on module load
  2) post_startup: run once the UE Asset Registry has loaded
  3) shutdown: run on Editor shutdown
"""


import unreal

from . import (
    actors,
    menus,
    metadata,
    bp_library,
    editor_tools
)
from .unreal_systems import asset_registry


# This module will make use of callbacks to handle two of its steps
# using a module variable cache we can prevent any duplicate work from happening
post_startup_id = None
shutdown_id = None


def pre_startup():
    """
    pre startup occurs when the Project is first opening in Unreal and Python is initialized

    This may occur before the Asset Registry has fully processed the Content Browser.
    It is safe to extend menus, initialized Python-based Blueprint Function Libraries,
    as well as anything not dependent on assets / files within the Content Browser
    """
    print(f"running pre startup, is asset registry available? {not asset_registry.is_loading_assets()}")
    bp_library.PyDemoBPLibrary()
    menus.populate_menus()
    metadata.metadata_startup()


def post_startup():
    """
    post startup occurs after the Asset Registry has loaded all Content Browser assets

    It should be safe to run any Python logic within Unreal at this point
    """
    print(f"running post startup, is asset registry available? {not asset_registry.is_loading_assets()}")
    editor_tools.startup()

    # Track the actor selection changes in the 3D level
    actors.enable_selection_tracking()


def shutdown(ignore=None):
    """
    shutdown occurs as Unreal is unloading Python.

    The Editor UI as well as any tools are probably closed by the time this is called.
    editor tools should handle their own shutdown, this is best for capturing any Editor states
    such as what the last-opened 3D Level was or saving information to a user temp file
    """
    print("You won't actually see this because the GUI is already gone, but it does run!")
    editor_tools.shutdown()


def run():
    """
    call this function from init_unreal to handle the Python startup process
    """
    # Ensure startup only run once
    global post_startup_id
    if post_startup_id:
        print("Package has already been initialized!")
        return

    # register and cache the post_startup callback and then run pre_startup
    post_startup_id = unreal.register_slate_post_tick_callback(asset_registry_callback)
    pre_startup()


def asset_registry_callback(ignore=None):
    """
    call post_startup() once the Asset Registry is fully loaded
    This function handles the cache and will also set up the shutdown callback
    """
    # check the asset registry
    if asset_registry.is_loading_assets():
        print("Asset Registry scan is still in progress...")
        return

    # unregister the callback
    global post_startup_id
    if post_startup_id:
        unreal.unregister_slate_post_tick_callback(post_startup_id)

    # run post startup
    post_startup()

    # register and cache the shutdown callback
    print("Registering Python Shutdown callback: startup_shutdown.shutdown()")
    global shutdown_id
    if not shutdown_id:
        shutdown_id = unreal.register_python_shutdown_callback(shutdown)
