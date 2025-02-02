"""
This module provides examples of running python code during Unreal startup and shutdown

There are three events handled in this module:
  1) pre_startup: run immediately on module load
  2) post_startup: run once the UE Asset Registry has loaded
  3) shutdown: run on Editor shutdown
"""


import unreal

from recipebook import (
    menus,
    metadata,
    bp_library
)
from recipebook.unreal_systems import asset_registry


# This module will make use of callbacks to handle two of its steps
# using a module variable cache we can prevent any duplicate work from happening
startup_id = None
shutdown_id = None


def on_pre_startup():
    """
    pre startup occurs when the Project is first opening in Unreal and Python is initialized

    This may occur before the Asset Registry has fully processed the Content Browser.
    It is safe to extend menus, initialized Python-based Blueprint Function Libraries,
    as well as anything not dependent on assets / files within the Content Browser
    """
    print(f"running pre startup, is asset registry available? {not asset_registry.is_loading_assets()}")
    metadata.metadata_startup()


def on_post_startup():
    """
    post startup occurs after the Asset Registry has loaded all Content Browser assets

    It should be safe to run any Python logic within Unreal at this point
    """
    print(f"running post startup, is asset registry available? {not asset_registry.is_loading_assets()}")
    menus.populate_menus()


def on_editor_shutdown():
    """
    shutdown occurs as Unreal is unloading Python.

    The Editor UI as well as any tools are probably closed by the time this is called.
    editor tools should handle their own shutdown, this is best for capturing any Editor states
    such as what the last-opened 3D Level was or saving information to a user temp file
    """
    print("You won't actually see this because the GUI is already gone, but it does run!")


def run():
    """run Pre Startup and then schedule Post Startup"""

    # Pre Startup can run right away
    on_pre_startup()

    # Schedule Post Startup
    global startup_id
    if not startup_id:
        startup_id = unreal.register_slate_post_tick_callback(wait_for_asset_registry)
    else:
        unreal.log_warning("Unreal Startup has already been run!")

    # Add Shutdown Hook
    global shutdown_id
    shutdown_id = unreal.register_python_shutdown_callback(on_editor_shutdown)


def wait_for_asset_registry(ignore=None):
    """Wait until the Asset Registry is ready before continuing"""
    if asset_registry.is_loading_assets():
        print(f"Still waiting on the Asset Registry...")
        return

    print(f"Asset Registry is ready!")

    # We can now remove the callback and continue
    global startup_id
    unreal.unregister_slate_post_tick_callback(startup_id)

    # Run Post Startup
    on_post_startup()
