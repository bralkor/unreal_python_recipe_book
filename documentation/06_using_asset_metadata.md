# <span style="color:white">Using Asset Metadata</span>

The Asset Registry in Unreal can be a powerful ally. We aren't limited to tracking our assets by their folder
path or their file type, we can also use any metadata keys that are declared in the Asset Registry.

This page covers the [metadata](../unreal_plugin/PythonRecipeBook/Content/Python/demo/metadata.py) python module

<br>

## <span style="color:yellow">Declaring Our Metadata</span>
<ul>

In the Unreal Project we first need to register our metadata names. This can be done in the `Asset Registry` section
of the `Project Settings` Editor Window:

![https://www.google.com/search?q=unreal+5+metadata&rlz=1C1CHBF_enUS722US722&oq=unreal+5+metadata&aqs=chrome..69i57j69i60l2.3181j0j1&sourceid=chrome&ie=UTF-8](https://docs.unrealengine.com/5.1/Images/understanding-the-basics/assets-content-packs/asset-metadata/fbx-metadata-asset-registry.png)

(image is from Epic's [Asset Metadata in Unreal Engine](https://docs.unrealengine.com/5.1/en-US/asset-metadata-in-unreal-engine/)
page, it's well worth reading!)

Metadata **must be properly declared** before we can make full use of them in Python. The most direct way to do this
is in the Project Settings window within the Editor. In Unreal 5.1 there is no direct means of adding Metadata names on the fly using Python,
that functionality needs to be exposed from c++ ourselves if desired. 

</ul>
<br>



## <span style="color:yellow">Setting Asset Metadata in Python</span>
<ul>

We can set an asset's metadata using 
[set_metadata_tag()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorAssetLibrary.html#unreal.EditorAssetLibrary.set_metadata_tag)
on the asset. An important note to remember is that Unreal uses strings to store its metadata:
```python
unreal_systems.EditorAssetLibrary.set_metadata_tag(asset, "asset_name", str("Eugene"))
unreal_systems.EditorAssetLibrary.set_metadata_tag(asset, "asset_version", str(500))
```
This is fine for most information, just remember to convert any complex data types to be a string first!

If we wanted to, we could wrap this function to handle the str() for us:
```python
def set_metadata(asset, key, value):
    """set the asset's metadata value"""
    unreal_systems.EditorAssetLibrary.set_metadata_tag(asset, key, str(value))
```

</ul>
<br>



## <span style="color:yellow">Getting Asset Metadata in Python</span>
<ul>

We can get an asset's metadata values from two places: the 
[loaded object](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorAssetLibrary.html#unreal.EditorAssetLibrary.get_metadata_tag)
or from an 
[AssetData reference](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/AssetData.html#unreal.AssetData.get_tag_value)


### From a Loaded Object

<ul>

If we have a loaded asset we can use 
[get_metadata_tag()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/EditorAssetLibrary.html#unreal.EditorAssetLibrary.get_metadata_tag)
to query for a given metadata's value:
```python
value = unreal_systems.EditorAssetLibrary.get_metadata_tag(asset, "asset_name")
```
This will return the metadata value as a string if found.

</ul>

### From an AssetData Object

<ul>

If we use the Asset Registry to find a list of assets we'll get the results as an
[AssetData](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/AssetData.html)
class. These are unloaded references that provide header information we can quickly query without paying the cost of loading the asset. 
Metadata on this class type can be retrieved using
[get_tag_value()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/AssetData.html#unreal.AssetData.get_tag_value):
```python
value = asset_data.get_tag_value("asset_name")
```
This will return the metadata value as a string if found.
</ul>

This is something we can wrap into our own utility function to handle both cases:
```python
def get_metadata(asset, key)
    """Get the loaded object or AssetData's metadata"""
    if isinstance(asset, unreal.AssetData):
        return asset.get_tag_value(key)
    else:
        return unreal_systems.EditorAssetLibrary.get_metadata_tag(asset, key)
```
Now we don't have to worry about remembering which one to use!

</ul>
<br>



## <span style="color:yellow">Extending Metadata Data Types with Python</span>
<ul>

A frustration of the get/set so far is that we're working with strings. If we're already wrapping the get/set functionality 
we might as well make it more convenient, let's return our `asset_version` metadata as an int directly!

The first thing we'll need is a Python dict, this is where we'll store the data type of any non-string metadata names:
```python
METADATA_TYPE_MAP = {
    "managed_asset": bool,
    "asset_version": int
}
```

Now we'll extend out `get_metadata()` function to make use of this. We'll store the unreal metadata value and, if it's
valid, check the `METADATA_TYPE_MAP` to determine what type of return is expected:
```python
def get_metadata(asset, key):
    """Get the loaded object or AssetData's metadata as its expected type"""
    # Get the unreal metadata value
    if isinstance(asset, unreal.AssetData):
        value = asset.get_tag_value(key)
    else:
        value = unreal_systems.EditorAssetLibrary.get_metadata_tag(asset, key)
    
    # If the metadata was found let's wrap it!
    if value:
        # Get this metadata key's expected value type, default is str (as-is)
        value_type = METADATA_TYPE_MAP.get(key, str)

        if value_type == bool:
            # bools are a special case as bool(str) only checks for length
            return value.lower() == "true"
        else:
            # most singular value types may be directly converted
            return value_type(value)
```

If we use this to query our asset's version number we'll get an int right away:
```python
value = get_metadata(asset, "asset_version")
type(value)

#  <type 'int'>
```

</ul>
<br>



## <span style="color:yellow">Searching for Assets by Metadata</span>
<ul>

If the assets we wish to search for are tagged with certain metadata values we can use the Asset Registry to find them!
We'll provide two inputs to our search: which class types to look for and a dict of {key:value} metadata pairs.

The search might be on the complicated side, here is what the function will do with unreal doc links:
1) It will use an [ARFilter](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/ARFilter.html#unreal.ARFilter)
object to tell the Asset Registry what class types we're looking for
2) The Asset Registry's [get_assets()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/AssetRegistry.html#unreal.AssetRegistry.get_assets)
function is what will return our initial list of [AssetData](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/AssetData.html#unreal.AssetData)
objects. We'll only filter for the class at this point
3) To filter based on metadata we'll be converting the {key:value} metadata search into 
[TagAndValue](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/TagAndValue.html#unreal.TagAndValue)
objects and create new ARFilters using 
[set_filter_tags_and_values()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/AssetRegistryHelpers.html#unreal.AssetRegistryHelpers.set_filter_tags_and_values)
4) For each metadata ARFilter we'll use [run_assets_through_filter()](https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/AssetRegistry.html#unreal.AssetRegistry.run_assets_through_filter)
to reduce the list of AssetData objects to only those matching each  filter

<br>

And this is what the python looks like:
```python
def find_assets_by_metadata(meta_dict, class_names=["object"]):
    """Find assets in the Content Browser based on a given dict of metadata {key:value} pairs"""

    # create a basic Asset Registry filter based on the class_names
    base_filter = unreal.ARFilter(
        class_names=class_names,
        recursive_classes=True
    )

    # Get the initial class-based search results
    results = unreal_systems.asset_registry.get_assets(base_filter) or []

    for key, value in meta_dict.items():
        # Create a new ARFilter based on the {key:value} pair
        query = [unreal.TagAndValue(key, str(value))]
        meta_filter = unreal_systems.asset_registry_helper.set_filter_tags_and_values(base_filter, query)

        # reduce the results to only those matching the given metadata
        results = unreal_systems.asset_registry.run_assets_through_filter(results, meta_filter) or []

    # return the results as a Python list as it might currently be an unreal.Array
    return list(results)
```
    
<br>
    
With our search function in place this is all we need to do to use it:
```python
metadata_search_data = {
    "asset_name": "Eugene",
    "asset_version": 500
}
results = find_assets_by_metadata(metadata_search_data)
```
Success, We now have a list of every "Eugene" marked asset in our project that's marked as version 500!
    
<br>
    
with the `class_names` argument we could further refine our results to a list of desired asset classes:
```python
results = find_assets_by_metadata(metadata_search_data, ["LevelSequence"])
```
This will only return level sequence assets matching the given metadata. This allows us to use the same metadata on different asset types, we could
query for all assets related to Eugene or only get its 3D Level, or its materials, or its textures, just by specifying the class type.
    
</ul>
<br>



# <span style="color:yellow">Summary</span>
<ul>

Metadata allows us to further manage our assets within Unreal. Assets of the same class can be marked for different
purposes regardless of folder location. This allows us to build more intuitive tools that might only offer assets
matching certain criteria or offer certain actions depending on the metadata values. 

Here's some additional links I found useful or learned from:
 - [Asset Metadata in Unreal Engine](https://docs.unrealengine.com/5.1/en-US/asset-metadata-in-unreal-engine/)
</ul>
