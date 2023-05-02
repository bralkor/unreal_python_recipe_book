# <span style="color:white">Editor Utility Widgets (EUWs) and Python</span>

In Python, we can open, close, and query the currently running EUW editor tools. We can also call
Python logic from our editor tools using Python-based BP nodes, such as to save/load user prefs.
This page covers both topics and includes a general warning for any editor tools using Python-based BP nodes.

This page covers the [editor_tools](../unreal_plugin/PythonRecipeBook/Content/Python/demo/editor_tools.py)
python module

<br>


## <span style="color:yellow">Opening/Closing Editor Utility Widgets</span>
<ul>

When it comes to editor tools we have a couple convenient functions to rely on.
The [EditorUtilitySubsystem](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorUtilitySubsystem.html)
has everything we need to launch, query, and close our tools.

### <span style="color:orange">Launching Editor Utility Widgets</span>
<ul>

To launch an Editor Widget from python we have two options depending on whether we wish to save its window ID: 
[spawn_and_register_tab()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorUtilitySubsystem.html#unreal.EditorUtilitySubsystem.spawn_and_register_tab)
or
[spawn_and_register_tab_and_get_id()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorUtilitySubsystem.html#unreal.EditorUtilitySubsystem.spawn_and_register_tab_and_get_id).

For this example we'll intentionally ignore the ID. If we know our asset path here's how we can launch our tool:
```python
asset_path = "/PythonRecipeBook/sample_tools/meta_viewer"
asset = unreal.load_asset(asset_path)
unreal_systems.EditorUtilitySubsystem.spawn_and_register_tab(asset)
```

</ul>

### <span style="color:orange">Is an Editor Utility Widget Running?</span>
<ul>

If we want to know whether an editor tool is running we can use one of two options
depending on if we know the Tab ID name for the given tool.

If we know the `asset_tab_id` we can look for it using 
[does_tab_exist()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorUtilitySubsystem.html#unreal.EditorUtilitySubsystem.does_tab_exist):
    
```python
if unreal_systems.EditorUtilitySubsystem.does_tab_exist(asset_tab_id)
```

If we don't have the Tab ID we can use
[find_utility_widget_from_blueprint()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorUtilitySubsystem.html#unreal.EditorUtilitySubsystem.find_utility_widget_from_blueprint).
If this function returns any information at all it means the tool is running:
    
```python
if unreal_systems.EditorUtilitySubsystem.find_utility_widget_from_blueprint(asset)
```

Both methods are valid, although as the second method requires a blueprint asset it might
not be as performant if you're trying to check for all currently running editor tools.

</ul>

### <span style="color:orange">Closing an Editor Utility Widget</span>
<ul>

To close an editor tool we will need its window ID. If we have the `asset_tab_id` we can use
[close_tab_by_id()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorUtilitySubsystem.html#unreal.EditorUtilitySubsystem.close_tab_by_id):
```python
unreal_systems.EditorUtilitySubsystem.close_tab_by_id(asset_tab_id)
```

If we don't have the ID but know the asset we can still make this work! 
[find_utility_widget_from_blueprint()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorUtilitySubsystem.html#unreal.EditorUtilitySubsystem.find_utility_widget_from_blueprint)
will tell us if it's currently open, if it is we'll just re-open the window to get its ID:
```python
if unreal_systems.EditorUtilitySubsystem.find_utility_widget_from_blueprint(asset):
  instance, asset_tab_id = unreal_systems.EditorUtilitySubsystem.spawn_and_register_tab_and_get_id(asset)
  unreal_systems.EditorUtilitySubsystem.close_tab_by_id(asset_tab_id)
```

Since the tab is already open `spawn_and_register_tab_and_get_id` won't really have to do much,
it's just an easy way to get the proper Tab ID!

</ul>

### <span style="color:orange">What is the Window ID?</span>
<ul>

In Unreal `5.1` the Tab ID is based on the asset's object path like so:
```python
f"{asset.get_path_name()}_ActiveTab"
# ex: Game/Tools/my_awesome_tool.my_awesome_tool_ActiveTab
```

If we want to make sure a tool is closed we could also run:
```python
success = unreal_systems.EditorUtilitySubsystem.close_tab_by_id(f"{asset.get_path_name()}_ActiveTab")
```
It's okay if it's not running or not found, this command will only return True if it was found and closed

</ul>
</ul>
<br>


## <span style="color:yellow">Saving User Prefs</span>
<ul>

One cool thing we can do in Python is save or load user prefs for our tools. This will require Blueprint
logic as well as a Python function.

We'll start on the Python side first, for our tool we want to:
- receive an Unreal.Map(str,str) of {key:value} prefs data
- save a json dict of {key:value} settings
- make a unique prefs file for any tool
- save the data to disk

<br>

```python
@unreal.ufunction(
    static=True, params=[str, unreal.Map(str, str)]
)
def save_user_prefs(prefs_name, prefs_data) :
    """Python Blueprint Node -- save some basic prefs data"""

    # The prefs data will come in as an Unreal Map from the BP Graph
    # Convert it to a json compliant dict
    prefs = {
        str(key): str(value)
        for key, value in prefs_data.items()
    }

    # we'll save this file under '<project_dir>/Saved/pytemp/unreal_prefs_<pref>.json'
    prefs_file = Path(
        unreal.Paths.project_saved_dir(), 
        "pytemp",
        f"unreal_prefs_{prefs_name}.json"
    )
    
    # create the folder path if necessary
    if not prefs_file.exists():
        prefs_file.parent.mkdir(parents=True, exist_ok=True)
    
    # write the prefs dict to the json file
    with prefs_file.open("w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2)
```
In the Blueprint Graph we're on the hook for providing the name of each pref and what data goes in it. 
Using `Make Map` we can store any user input / properties we desire to appropriately named keys:

![](images/prefs_save.PNG)

It's best to call this function from the `Event Destruct` Event, which will trigger as the tool is closed.

</ul>
<br>

## <span style="color:yellow">Loading User Prefs</span>
<ul>

Loading our user prefs is a bit more involved in the BP Graph.

In Python, we can just return the prefs data if the prefs file exists. Unreal will convert the json
dict into an Unreal.Map for us:
```python
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
```

In the Blueprint Graph we can call this Python Function, store the results in a `Prefs` local variable,
and for each expected pref perform the appropriate action to load it:

![](images/prefs_load.PNG)

Loading the prefs is one of the first things a tool should do on `construct`. If our save and load 
states are properly in place the tool will remember our options from last time and take us back to 
our previous settings.

The sample tool `meta_viewer` (covered on the next page) uses this prefs feature, 
it's not too exciting here in the docs but try it out!

</ul>
<br>


## <span style="color:yellow">Unreal Shutdown/Startup and Python-based BP Nodes</span>
<ul>

An important consideration to be aware of is that Python is an Unreal Plugin, as such it's not
the first thing Unreal will load when launching a project. The project's default
3D level will process and open before the plugins have been loaded. Cached Editor Utility Widgets
will also open before the plugins have been loaded (editor tools that were still open during Editor shutdown). 

What this means for us is that there's a reasonable chance of these editor assets loading before their
Python-based Blueprint Nodes have been registered in the Editor. If any nodes were implemented in the way described by
[the Blueprint Function Libraries documentation page](./02_blueprint_function_libraries.md)
we will need to avoid placing these nodes in the project's default 3D level and prevent Unreal from
caching those Editor Utility Widgets.

<br>
    
It can get lost in the Output Log, but here is an example of an editor tool that broke because
Unreal reopened it before Python was initialized:
```
LogBlueprint: Error: [AssetLog] C:\ue_projects\demo_project\Plugins\PythonRecipeBook\Content\sample_tools\meta_viewer.uasset: [Compiler] In use pin  Array To Match  no longer exists on node  Get Item Data For Euw . Please refresh node or break links to remove pin.
LogBlueprint: Error: [AssetLog] C:\ue_projects\demo_project\Plugins\PythonRecipeBook\Content\sample_tools\meta_viewer.uasset: [Compiler] In use pin  Return Value  no longer exists on node  Get Item Data For Euw . Please refresh node or break links to remove pin.
LogBlueprint: Error: [AssetLog] C:\ue_projects\demo_project\Plugins\PythonRecipeBook\Content\sample_tools\meta_viewer.uasset: [Compiler] Could not find a function named "get_item_data_for_euw" in 'meta_viewer'.
Make sure 'meta_viewer' has been compiled for  Get Item Data For Euw
```
This happened because I closed the editor while the `meta_viewer` editor tool was still running.
    
<br>

In the following sections we'll go over a means of preventing this error by making sure our tool doesn't get saved to this user prefs.


### <span style="color:orange">The Necessary c++ Logic</span>
<ul>

The source of this issue is the User Prefs, which is only accessible in c++.
The user pref in question lives on the **EditorUtilitySubsystem**'s **LoadedUIs** property.
We need to get this property, remove the given entry, and then save the user prefs to disk.

Here is what that logic looks like (available in the PythonRecipeBook plugin):
```cpp
void
UPythonUtilsLibrary::ClearEditorToolFromPrefs(UEditorUtilityWidgetBlueprint* EditorWidget) {
    UEditorUtilitySubsystem* EUS = GEditor->GetEditorSubsystem<UEditorUtilitySubsystem>();
    EUS->LoadedUIs.Remove(EditorWidget);
    EUS->SaveConfig();
}
```

it may be accessed in Python via:
```python
unreal.PythonUtilsLibrary.clear_editor_tool_from_prefs(editor_widget_blueprint)
```

This c++ function will get the Editor Utility Subsystem, remove the given asset from its user prefs, 
and then update the user prefs file on disk. This function is available in both the BP Graph and
Python, but I plan to further extend this function in Python to make it more convenient.

</ul>


### <span style="color:orange">Extending the c++ Logic in a Python-based Node</span>
<ul>

I am not a proper c++ programmer, my method is usually to find & copy existing engine code
for the functionality that I need and then extend it further in Python as needed.

In my Python function is where I'll start building in some conveniences, such as working off of a `self` 
reference. Using the `DefaultToSelf` decorator arg we'll pass the current EUW instance to Python, get its 
Content Browser asset, and pass that to our c++ function.

This is what the Python-based BP function looks like:
```python
    @unreal.ufunction(
        static=True, params=[unreal.EditorUtilityWidget],
        meta=dict(DefaultToSelf="editor_tool")
    )
    def on_editor_tool_close(editor_tool):
        """Python Blueprint Node -- Manage Editor Tools using Python-based nodes"""

        # Get the Content Browser asset and remove it from the c++ User Prefs
        editor_tool_path = str(editor_tool.get_class().get_outer().get_path_name())
        editor_tool_asset = unreal.find_asset(editor_tool_path)
        unreal.PythonUtilsLibrary.clear_editor_tool_from_prefs(editor_tool_asset)
```

- The `DefaultToSelf` meta entry will auto-populate the `editor_tool` arg with a reference to `self`
- `editor_tool_path` is the EUW's package path, such as `Content/tools/my_tool`
- `editor_tool_asset` is a reference to the proper base asset needed for `clear_editor_tool_from_prefs()`

<br>

We'll call this Python-based Node on the Destruct event, which runs when the editor tool is closed:

![](images/editor_widget_node.PNG)

With this node added our tool won't save to the User Prefs INI file on Editor shutdown anymore. 
It will not open automatically anymore on Editor startup, but it will make the tool more error-proof.

</ul>

### <span style="color:orange">Limitations</span>
<ul>

This setup will work for intentional Editor shutdown, but it may not be reliable if the Editor
crashes. Following an Editor crash the user may still need to close all Editor Widgets and reopen Unreal.

To make the system more robust we could call this function after the `Construct` event is complete
or adding it to additional events such as `On Mouse Enter`, but it might not be 100% error proof.
The best case scenario would be to change the c++ code, but that may not be an option for every project.

</ul>

### <span style="color:orange">Managing Our Own Shutdown/Startup</span>
<ul>

this is a complex topic that I might write up properly another time, but it's still possible to relaunch our
tools during editor startup. This would require writing our own user prefs system and some Python magic, but
it is possible! A working solution is provided in the `editor_tools` Python module of the plugin, feel free 
to try it out and dissect it!

</ul>

</ul>
<br>
    
    
    

# <span style="color:yellow">Summary</span>
<ul>

Editor Utility Widgets using Python-based BP nodes can be dangerous by default, but with a little c++ we can 
make them safer to use. Managing these editor tools isn't entirely necessary, really it's up to how complex you want 
to go! Removing them from Unreal's user prefs INI makes them safe, but we can also write our own 
prefs / management system in Python to expand functionality.

Once we get past the dangers of EUWs using Python-based BP nodes, there is a lot of power in using Python in
editor tools: we can easily set up user prefs, manage our active tools, and write functionality beyond Unreal
with ease.

</ul>
