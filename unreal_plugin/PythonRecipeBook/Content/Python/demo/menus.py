"""
This module shows two styles of adding editor menus
We can add a `ToolMenuEntryScript` directly to the end of a menu
or wrap it in a `ToolMenuEntry` to control where it's added
"""


import json
import unreal

from . import (
    actors,
    editor_tools
)
from .unreal_systems import ToolMenus


# ---------      Demo base class setups     --------- #


@unreal.uclass()
class PythonMenuTool(unreal.ToolMenuEntryScript):
    """
    menu tool base class for python tools
    """
    name = "unique_programatic_tool_name"
    display_name = "menu display name"
    tool_tip = "tool tip message"

    def __init__(self, menu, section, insert_policy=None):
        """
        initialize this python tool and add it to the given menu's section

        parameters:
            menu: the menu object to add this tool to
            section: the section to group this tool under
            insert_policy: if provided, how to add this entry to the parent menu
        """
        super().__init__()

        # Add the given section if not already present
        menu.add_section(section, section)

        # Initialize the entry data
        self.init_entry(
            owner_name="demo_tools_tracker",
            menu=menu.menu_name,
            section=section,
            name=self.name,
            label=self.display_name,
            tool_tip=self.tool_tip
        )

        if insert_policy:
            # Build the entry insert object
            entry = unreal.ToolMenuEntry(
                name="huzzah",
                type=unreal.MultiBlockType.MENU_ENTRY,
                insert_position=insert_policy,
                script_object=self
            )

            # Add this tool to the desired menu
            # this will insert using the given policy
            menu.add_menu_entry(section, entry)

        else:
            # Add this tool to the desired menu
            # this will insert at the bottom of the menu
            menu.add_menu_entry_object(self)

    @unreal.ufunction(override=True)
    def execute(self, context):
        """
        The Python code to execute when pressed,
        a context is provided to determine where this button was pressed from

        This should be overridden in child classes
        """
        print(f"Provided context: {context}")


@unreal.uclass()
class EditorUtilMenuTool(PythonMenuTool):
    """
    menu tool base class to launch specified Editor Utility Widgets
    """
    widget_path = "some/path"

    @unreal.ufunction(override=True)
    def execute(self, context):
        """Open the EUW when pressed"""
        print(f"Provided context: {context}")
        editor_tools.launch_editor_utility_widget(self.widget_path)


# ---------      Demo Tool class setups     --------- #

# Python tools we can focus on the menu name and the execute function
@unreal.uclass()
class ActorHierarchy(PythonMenuTool):
    """A demo tool that will print the current level's actor hierarchy"""
    name = "print_actor_hierarchy"
    display_name = "Print Actor hierarchy"

    @unreal.ufunction(override=True)
    def execute(self, context):
        """
        print the current scene's actor hierarchy in a json format
        """
        print(json.dumps(actors.get_scene_hierarchy(), indent=4))


@unreal.uclass()
class Huzzah(PythonMenuTool):
    name = "huzzah"
    display_name = "Huzzah!"
    tool_tip = "huzzahhhhhh!!!!"

    @unreal.ufunction(override=True)
    def execute(self, context):
        print(f"Huzzah, good day to you! {context}")


@unreal.uclass()
class TrackActors(PythonMenuTool):
    name = "track_Actors"
    display_name = "Track Actors"
    tool_tip = "Enable tracking the current actor selection"

    @unreal.ufunction(override=True)
    def execute(self, context):
        actors.enable_selection_tracking()


@unreal.uclass()
class MetadataFilterTool(EditorUtilMenuTool):
    name = "meta_viewer"
    display_name = "Meta Viewer GUI"
    widget_path = "/PythonRecipeBook/sample_tools/meta_viewer"


# ---------      Create the menu     --------- #


def populate_menus():
    """
    call this menu during unreal startup to populate our desired menus
    we'll use separate functions to keep track of which menus we're extending
    """
    populate_main_menu()
    populate_edit_menu()


def populate_main_menu():
    """
    populate our demo dropdown menu on the main menu bar
    """
    # The main menu we'll add our tools to:
    main_menu = ToolMenus.find_menu("LevelEditor.MainMenu")

    # First, let's create a new sub menu:
    demo_menu = main_menu.add_sub_menu(
        owner="demo_tools_tracker",
        section_name="",
        name="demo_tools",
        label="Demo Tools"
    )

    # Next, initialize our menu classes into the demo_menu in the desired sections
    # these menu entries will be added in sequential order (no insert policy provided)
    section = "scene"
    ActorHierarchy(menu=demo_menu, section=section)
    TrackActors(menu=demo_menu, section=section)

    section = "tools"
    MetadataFilterTool(menu=demo_menu, section=section)


def populate_edit_menu():
    """
    insert our entry class to the Edit menu after the `Paste` option
    """
    # The edit menu we'll add our tools to:
    edit_menu = ToolMenus.find_menu("LevelEditor.MainMenu.Edit")

    # First, we'll create our insert policy: after the menu entry named "Paste"
    insert_policy = unreal.ToolMenuInsert("Paste", unreal.ToolMenuInsertType.AFTER)

    # Next, initialize our menu classes into the edit_menu in the desired section
    # this menu entry will be added after the Paste entry (insert policy provided)
    section = "EditMain"
    Huzzah(menu=edit_menu, section=section, insert_policy=insert_policy)
