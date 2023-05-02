<h2 align="center">Documentation</h2>

<p align="center">
This documentation will cover how Unreal's systems work in Python<br>
and help to expose what's possible with it
</p>

<br>

This Python documentation covers many aspects of Unreal and is meant for users who are familiar with both
Python and Unreal Engine. It will provide links to official documentation when possible, but the primary
focus is on building working examples rather than explaining Unreal's toolsets or concepts. The primary goal of
this project is to show how the pieces go together in Python.

Any code shown should be present in the provided Unreal plugin's Python modules but there may be some differences
to help with clutter and formatting. Some code snippets may reference modules such as `ue` or `metadata` from the plugin's
Python modules, if it doesn't start with `unreal` and hasn't been explained it's probably from another module within this project.

<br>

Currently available pages:

<table>
<tr><td>

(0) [Dev Conveniences](./00_conveniences.md)

</td><td>

Some small conveniences I've found and make use of in my own code.


</td></tr><tr><td>


(1) [Startup and Shutdown](./01_startup_and_shutdown.md)
</td><td>

How to run code at various points of Unreal's startup and shutdown sequences. 

</td></tr><tr><td>


(2) [Blueprint Function Libraries](./02_blueprint_function_libraries.md)
</td><td>

How to create Blueprint Graph function nodes in Python. This allows us far greater freedom and possibilities to call Python logic from the BP Graph.
Examples with screenshots are provided for each individual option.

</td></tr><tr><td>


(3) [Using Assets in Python](./03_using_assets_in_python.md)
</td><td>

How to interact with Content Browser assets in Python. This covers instancing, properties, and calling Blueprint functions.

</td></tr><tr><td>


(4) [Extending Menus](./04_extending_menus.md)
</td><td>

How to create and insert new menus in the Editor. This covers how to find menus, create drop down menus, and two styles of adding menu buttons.

</td></tr><tr><td>


(5) [Actor and Component Interactions](./05_actors_and_components.md)
</td><td>

How to interact with actors and components. This covers walking actor and component hierarchies as well as some basic interactions, 
such as determining the source asset of an actor.

</td></tr><tr><td>


(6) [Using Asset Metadata](./06_using_asset_metadata.md)
</td><td>

How to use and interact with Content Browser Asset metadata. This covers getting, setting, and searching for assets via metadata.

</td></tr><tr><td>


(7) [Editor Utility Widgets (EUWs) and Python](./07_editor_utility_widgets.md)
</td><td>

How to manage EUWs with Python. This covers opening and closing EUWs, managing user prefs, and a danger when using EUWs with Python.

</td></tr><tr><td>


(8) [An Editor Utility Widget Example](./08_editor_widget_example.md)
</td><td>

An example Editor Tool which makes use of Python. This tool displays arbitrary assets and allows for filtering based on their metadata values.

</td></tr>
</table>


<br>
