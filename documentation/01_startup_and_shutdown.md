# <span style="color:white">Python Startup and Shutdown in Unreal</span>

When opening or closing an application we may want to set some environment properties or run certain scripts.
In Unreal there are a few callbacks and functions we can use to track the various startup / shutdown events.
We can use that information to run our desired startup / shutdown scripts at the appropriate times!

This page covers the [init_unreal](../unreal_plugin/PythonRecipeBook/Content/Python/init_unreal.py) and
[startup_shutdown](../unreal_plugin/PythonRecipeBook/Content/Python/demo/startup_shutdown.py) python module

<br>



## <span style="color:yellow">init_unreal.py</span>
<ul>

Unreal will look for and run any `/Python/init_unreal.py` files in its environment during startup.
This file may be in the Content Browser, a Plugin, or even a rez package if you're managing Unreal with rez, as long as
it's directly under a top-level `/Python/` folder it should run. The
[Unreal Scripting the Editor using Python](https://docs.unrealengine.com/5.2/en-US/scripting-the-unreal-editor-using-python/)
Epic doc page has a section covering init_unreal that's worth reading.

A preference of mine is to treat `init_unreal.py` more like an `__init__`, the only thing I put in my
`init_unreal` is an import and run for a dedicated startup script:

```python
from demo import startup_shutdown
startup_shutdown.run()
```

Because this module has to be on the top level it seldom lives next to the rest of my Python logic, having a dedicated
`startup_shutdown` module lets me clearly define what the module is expected to handle and it can live with the rest
of my Python logic. This is of course just a preference and the setup should work just as fine in `init_unreal`.

</ul>
<br>


## <span style="color:yellow">Startup</span>
<ul>

Python gets initialized before the Asset Registry has fully loaded the contents of our Unreal Project.
This means that Unreal might not have full awareness of everything available in the Project, it may
cause issues if we attempt to query, inspect, or otherwise load assets too soon.

As such, there's really two steps to the startup process that we want to capture:
1) Before the Asset Registry has processed the Project, we'll call this `pre startup`
2) After the Asset Registry has processed the Project, we'll call this `post startup`

<br>

### Pre Startup
<ul>

Pre startup occurs BEFORE the Asset Registry has processed the contents of our Project.
At this stage it should be safe to set any environment variables, load any Blueprint Function Libraries, and extend any Menus.
There is no magic to running `pre startup` scripts, you can simply call them immediately when your module is imported
or from a function:
    
```python
def pre_startup():
    # (actual pre startup commands...)
    # this function can be called imediately when the module is imported
```

</ul>
<br>
    
    

### Post Startup
<ul>

Post startup should occur AFTER the Asset Registry has processed the contents of our Project.
At this stage it is now safe to search for, load, and use assets from the Content Browser.
With this setup we can use custom Blueprint Assets in the Content Browser as Configs for our Project, 
safely launch Editor Utility Widgets, or load any cached states from a previous editor session.

There isn't a provided Unreal callback for this, instead we'll use 
[register_slate_post_tick_callback()](https://docs.unrealengine.com/5.2/en-US/PythonAPI/module/unreal.html#unreal.register_slate_post_tick_callback)
to add a per-frame callback during `Pre Startup`to check the Asset Registry's
[is_loading_assets()](https://docs.unrealengine.com/5.2/en-US/PythonAPI/class/AssetRegistry.html#unreal.AssetRegistry.is_loading_assets)
function. Once the Asset Registry is done loading assets we can safely run our `Post Startup` script:
```python
# in our pre_startup function we'll create a post-tick callback and save its ID to a module variable
def pre_startup():
    # (actual pre startup commands...)
    
    # at the end of pre startup, register a post tick callback function and cache it
    global post_startup_id
    post_startup_id = unreal.register_slate_post_tick_callback(post_startup_check)
```
```python
# this function will run after every Unreal UI redraw to check if the Project is fully loaded yet
def post_startup_check(ignore=None):
    # check if the asset registry is still loading everything
    if unreal.AssetRegistryHelpers().get_asset_registry().is_loading_assets():
        print("Asset Registry scan is still in progress...")
        return
    
    # disable the callback (no longer needed)
    global post_startup_id
    unreal.unregister_slate_post_tick_callback(post_startup_id)
    
    # we can now safely run our post startup:
    post_startup()
```
```python
# this function is where we'll add the operations we want to run after the Project is fully loaded
def post_startup():
    # (actual post startup commands...)
```

Anything we place in a `post_startup` function will have full access to everything in the Project

</ul>
</ul>
<br>




# <span style="color:yellow">Shutdown</span>
<ul>

Python shutdown is run after the Editor UI and any open tools have been closed. Any tool shutdown logic should be 
handled by the tools directly as the Python shutdown event will have limited information available. It's best to only
expect access to the last 3D Level that was open and any environment variables.

To setup our Shutdown event we'll add 
[register_python_shutdown_callback()](https://docs.unrealengine.com/5.2/en-US/PythonAPI/module/unreal.html#unreal.register_python_shutdown_callback)
to the end of `Post Startup`, :

```python
# in our post_startup function we'll create a shutdown callback and save its ID to a module variable

def post_startup():
    # (actual post startup commands...)
    
    # at the end of post startup, register a shutdown callback function and cache it
    global shutdown_id
    shutdown_id = unreal.register_python_shutdown_callback(shutdown)
```
```python
# this function is where we'll add the operations we want to run on shutdown
def shutdown(ignore=None):
    # (actual shutdown commands...)
    
```
    
And that's all there is to it! Our `shutdown()` function will be called just before Unreal is fully closed to save any last moment python settings

</ul>
<br>



# <span style="color:yellow">Summary</span>
<ul>

Python initialization happens just before the Asset registry has loaded the Project's contents. To get the most out of our
startup process we can use callbacks to delay certain operations until it is safe to run.
    
Here's some additional links I found useful or learned from:
 - [Unreal Scripting the Editor using Python](https://docs.unrealengine.com/5.2/en-US/scripting-the-unreal-editor-using-python/)
</ul>
