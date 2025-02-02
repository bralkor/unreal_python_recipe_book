"""
This module shows two styles of adding editor menus
We can add a `ToolMenuEntryScript` directly to the end of a menu
or wrap it in a `ToolMenuEntry` to control where it's added
"""


import json
import unreal

from recipebook import (
    actors,
    editor_tools
)
from recipebook.unreal_systems import ToolMenus


# ---------      Demo base class setups     --------- #


@unreal.uclass()
class PythonMenuTool(unreal.ToolMenuEntryScript):
    name = "programatic_name"
    label = "display Name"
    tool_tip = "tool tip!"

    def __init__(self, menu, section=""):
        """
        given a menu object and a section name,
        initialize this python tool and add it to the menu
        """
        super().__init__()

        if section:
            menu.add_section(section, section)

        # Initialize the entry data
        self.init_entry(
            owner_name="custom_owner",
            menu=menu.menu_name,
            section=section,
            name=self.name,
            label=self.label,
            tool_tip=self.tool_tip
        )

        # Add this tool to the desired menu
        menu.add_menu_entry_object(self)

    @unreal.ufunction(override=True)
    def execute(self, context):
        """The Python code to execute when pressed"""
        print(f"Provided context: {context}")


@unreal.uclass()
class DynamicMenuTest(PythonMenuTool):
    name = "dynamic_test"
    label = "Use CTRL"

    @unreal.ufunction(override=True)
    def can_execute(self, context):
        """Can the user press this menu entry?"""
        is_ctrl_down = unreal.InputLibrary.modifier_keys_state_is_control_down(
            unreal.InputLibrary.get_modifier_keys_state()
        )
        return is_ctrl_down

    @unreal.ufunction(override=True)
    def get_label(self, context):
        """Update the Display Name"""
        is_ctrl_down = unreal.InputLibrary.modifier_keys_state_is_control_down(
            unreal.InputLibrary.get_modifier_keys_state()
        )
        return "CTRL is GO!" if is_ctrl_down else "Press CTRL to use"


@unreal.uclass()
class PythonMenuToolInsert(unreal.ToolMenuEntryScript):
    name = "inserted_menu"
    label = "Inserted Menu Class"
    tool_tip = "tool tip!"

    def __init__(self, menu, section="", insert_policy=None):
        """Initialize our entry for the given menu_object's section"""
        super().__init__()

        if section:
            menu.add_section(section, section)

        # Initialize the entry data
        self.init_entry(
            owner_name="custom_owner",
            menu=menu.menu_name,
            section=section,
            name=self.name,
            label=self.label,
            tool_tip=self.tool_tip
        )

        # if an insert policy was provided
        if insert_policy:
            # Build the entry insert object
            entry = unreal.ToolMenuEntry(
                name=self.name,
                type=self.data.advanced.entry_type,
                owner=unreal.ToolMenuOwner("custom_owner"),
                insert_position=insert_policy,
                script_object=self
            )

            # insert policy method
            menu.add_menu_entry(section, entry)

        else:
            # default method - add at the bottom of the menu
            menu.add_menu_entry_object(self)


@unreal.uclass()
class PythonMenuToolWithIcon(unreal.ToolMenuEntryScript):
    name = "icon_menu"
    label = "Menu Class w/ Icon"
    tool_tip = "tool tip!"

    def __init__(self, menu, section=""):
        """Initialize our entry for the given menu_object's section"""
        super().__init__()

        # Initialize the entry data
        self.init_entry(
            owner_name="custom_owner",
            menu=menu.menu_name,
            section=section,
            name=self.name,
            label=self.label,
            tool_tip=self.tool_tip
        )
        self.data.icon = unreal.ScriptSlateIcon(
            "EditorStyle",
            "WorldBrowser.DetailsButtonBrush"
        )

        menu.add_menu_entry_object(self)

    @unreal.ufunction(override=True)
    def get_icon(self, context):
        """The Python code to execute when pressed"""
        is_ctrl_down = unreal.InputLibrary.modifier_keys_state_is_control_down(
            unreal.InputLibrary.get_modifier_keys_state()
        )
        active_icon = unreal.ScriptSlateIcon(
            "EditorStyle",
            "SourceControl.StatusIcon.On"
        )
        inactive_icon = unreal.ScriptSlateIcon(
            "EditorStyle",
            "SourceControl.StatusIcon.Error"
        )
        return active_icon if is_ctrl_down else inactive_icon


@unreal.uclass()
class EditorUtilityWidgetMenuTool(PythonMenuTool):
    """
    menu tool base class to launch specified Editor Utility Widgets
    """
    widget_path = "/Game/editor/utility/widget/path"

    @unreal.ufunction(override=True)
    def execute(self, context):
        """Open the EUW when pressed"""
        editor_tools.launch_editor_utility_widget(self.widget_path)


# ---------      Demo Tool class setups     --------- #


@unreal.uclass()
class OpenRecipeBookDocumentation(PythonMenuTool):
    """A recipebook tool that will print the current level's actor hierarchy"""
    name = "open_recipe_book"
    label = "Recipe Book Documentation"

    @unreal.ufunction(override=True)
    def execute(self, context):
        """
        print the current scene's actor hierarchy in a json format
        """
        unreal.SystemLibrary.launch_url(r"https://bkortbus.gitbook.io/unreal-python-recipe-book")




# Python tools we can focus on the menu name and the execute function
@unreal.uclass()
class ActorHierarchy(PythonMenuTool):
    """A recipebook tool that will print the current level's actor hierarchy"""
    name = "print_actor_hierarchy"
    label = "Print Actor hierarchy"

    @unreal.ufunction(override=True)
    def execute(self, context):
        """
        print the current scene's actor hierarchy in a json format
        """
        print(json.dumps(actors.get_scene_hierarchy(), indent=4))


@unreal.uclass()
class Huzzah(PythonMenuToolInsert):
    name = "huzzah"
    label = "Huzzah!"
    tool_tip = "huzzahhhhhh!!!!"

    @unreal.ufunction(override=True)
    def execute(self, context):
        print(f"Huzzah, good day to you! {context}")


@unreal.uclass()
class TrackActors(PythonMenuTool):
    name = "track_actors"
    label = "Track Actor Selection Changes"
    tool_tip = "Enable tracking the current actor selection"

    active = unreal.uproperty(bool)

    def __init__(self, menu, section=""):
        super().__init__(menu, section)
        self.active = False

        # Change the menu type and re-add it to the menu to update it
        self.data.advanced.user_interface_action_type = unreal.UserInterfaceActionType.TOGGLE_BUTTON
        menu.add_menu_entry_object(self)

    @unreal.ufunction(override=True)
    def get_check_state(self, context):
        """determine the icon to display"""
        checked = unreal.CheckBoxState.CHECKED
        unchecked = unreal.CheckBoxState.UNCHECKED
        return checked if self.active else unchecked

    @unreal.ufunction(override=True)
    def execute(self, context):
        self.active = not self.active

        actors.toggle_selection_tracking(self.active)



@unreal.uclass()
class MetaViewerTool(EditorUtilityWidgetMenuTool):
    name = "meta_viewer"
    label = "Meta Viewer GUI"
    tool_tip = "Launch the Meta Viewer tool"
    widget_path = "/PythonRecipeBook/sample_tools/meta_viewer"


# ---------      Create the menu     --------- #


def populate_menus():
    """
    call this menu during unreal startup to populate our desired menus
    we'll use separate functions to keep track of which menus we're extending
    """
    populate_main_menu()
    populate_edit_menu()

    ToolMenus.refresh_all_widgets()


def populate_main_menu():
    """
    populate our recipebook dropdown menu on the main menu bar
    """
    # The main menu we'll add our tools to:
    main_menu = ToolMenus.find_menu("LevelEditor.MainMenu")

    # First, let's create a new sub menu:
    demo_menu = main_menu.add_sub_menu(
        owner="demo_tools_tracker",
        section_name="",
        name="recipe_book_demo",
        label="Recipe Book"
    )

    # Next, initialize our menu classes into the demo_menu in the desired sections
    # these menu entries will be added in sequential order (no insert policy provided)
    section = "scene"
    ActorHierarchy(menu=demo_menu, section=section)
    TrackActors(menu=demo_menu, section=section)

    section = "tools"
    MetaViewerTool(menu=demo_menu, section=section)
    DynamicMenuTest(menu=demo_menu, section=section)

    section = "Resources"
    OpenRecipeBookDocumentation(menu=demo_menu, section=section)


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
