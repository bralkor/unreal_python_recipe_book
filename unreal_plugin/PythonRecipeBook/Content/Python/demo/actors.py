"""
This module shows some basic actor interactions
with a focus on processing the actor hierarchy
in our current 3D level
"""


import unreal

from .unreal_systems import (
    EditorAssetLibrary,
    EditorActorSubsystem
)

function_demo_class = None
def is_functions_demo_actor(actor):
    """
    check if the given actor is a 'ue_functions_demo' blueprint actor

    parameters:
        actor: the actor to process

    return:
        True if the actor is an ue_functions_demo BP
    """
    global function_demo_class

    if not function_demo_class:
        asset_path = "/PythonRecipeBook/sample_assets/ue_functions_demo"
        if EditorAssetLibrary.does_asset_exist(asset_path):
            function_demo_class = EditorAssetLibrary.load_asset(asset_path).generated_class()
        else:
            unreal.log_warning(f"functions_demo asset not found in its expected location: {asset_path}")
            return

    return unreal.MathLibrary.class_is_child_of(actor.get_class(), function_demo_class)


def get_scene_hierarchy():
    """
    process the 3D level for basic actor hierarchy information

    return:
        the scene's actor hierarchy in a json compliant dict
    """

    # get all top level actors
    top_level_actors = [
        actor
        for actor in EditorActorSubsystem.get_all_level_actors()
        if not actor.get_attach_parent_actor()
        and not actor.get_parent_actor()
    ]

    # get the hierarchy for each top level actor
    data = {
        str(actor.get_path_name()): walk_actor(actor)
        for actor in top_level_actors
    }

    return data


def walk_actor(actor):
    """
    walk the given actor's hierarchy and convert it to a json compliant dict

    parameters:
        actor: the actor to process

    return:
        dict: the actor's hierarchy in a json compliant dict
    """
    # Get the asset path
    asset_path = get_asset_from_actor(actor)

    # separate the nested actors from the spawned actors:
    spawned_actors = actor.get_all_child_actors()
    nested_actors = [
        child
        for child in actor.get_attached_actors()  # all actors under the current actor
        if child not in spawned_actors  # actors spawned by the current actor
    ]

    if spawned_actors:
        print(f"{actor.get_actor_label()} spawns the following actors:")
        for child in spawned_actors:
            print(f"\t> {child.get_actor_label()}")

    # Recurse through any nested actors
    children = {
        str(child.get_path_name()): walk_actor(child)
        for child in nested_actors
    }

    # Store the actor data
    data = {
        "display_name": str(actor.get_actor_label()),
        "actor_class": str(actor.get_class().get_name()),
        "asset_path": str(asset_path),
        "transform": get_actor_root_transform(actor),
        "children": children
    }

    # if we know the class we're interacting with we can use `call_method`
    # to run functions declared in the Blueprint Graph
    if is_functions_demo_actor(actor):
        data["arbitrary_data"] = str(actor.call_method("get_arbitrary_data"))
        data["prefixed_data"] = str(actor.call_method("add_prefix", ("my_input",)))

        print(
            f"Processed the following additional data on {data['display_name']}:\n\t"
            f"arbitrary_data: {data['arbitrary_data']}\n\t"
            f"prefixed_data : {data['prefixed_data']}"
        )

    # print out the component hierarchy of this actor
    print(f"{actor.get_actor_label()} components:")
    walk_component(actor.root_component, actor)

    return data


def walk_component(component, owner=None, indent=2):
    """
    walk the given component's hierarchy and print it
    It's best to call this on an actor's root component

    parameters:
        component: the component to process
        owner: the actor that owns this component,
               if provided this will keep the results
               local to the immediate actor
    """
    if component and (component.get_owner() == owner or not owner):
        print(f"{'. '*indent}{component.get_name()}")

        # recurse through any immediate children
        for child in component.get_children_components(False):
            walk_component(child, owner, indent+2)


def get_actor_root_transform(actor):
    """
    Get the actor's root component transform data as a dict

    parameters:
        actor: the actor to process

    returns:
        dict: the actor's root transform data as a dict
    """

    # an actor's transforms is stored on its root component
    root = actor.root_component
    if not root:
        return dict()

    # break up the transform data to make it easier to pack into json
    xform = root.get_relative_transform()
    translate = xform.translation
    rotate = xform.rotation.rotator()
    scale = xform.scale3d

    return {
        "location": [float(v) for v in [translate.x, translate.y, translate.z]],
        "rotate": [float(v) for v in [rotate.roll, rotate.pitch, rotate.yaw]],
        "scale": [float(v) for v in [scale.x, scale.y, scale.z]],
        "is_absolute": [root.absolute_location, root.absolute_rotation, root.absolute_scale]
    }


def get_asset_from_actor(actor):
    """
    Get the content browser asset path of the given actor,
    support must be added for each asset type

    parameters:
        actor: the actor to process

    returns:
        the actor's source asset (if supported & found)
    """

    # the source asset is usually stored on the root component
    # and is generally unique per component class type,
    # support will need to be added for each type
    if isinstance(actor.get_class(), unreal.BlueprintGeneratedClass):
        asset = actor.get_class().get_outer()
    elif isinstance(actor, unreal.StaticMeshActor):
        asset = actor.static_mesh_component.static_mesh.get_outer()
    elif isinstance(actor, unreal.SkeletalMeshActor):
        asset = actor.skeletal_mesh_component.skeletal_mesh.get_outer()
    else:
        unreal.log_warning(
            f"\n\tActor {actor.get_actor_label()} has an unknown or unsupported source asset ({actor.get_class()})"
            "\n\t\tEither the actor does not have a source asset in the Content Browser"
            "\n\t\tor get_asset_from_actor() does not yet support its class type"
        )
        return ""

    return str(asset.get_path_name())


def enable_selection_tracking():
    """
    Enable the tracking of the user's selection
    """
    # Track the actor selection changes in the 3D level
    level_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    selection_set = level_editor_subsystem.get_selection_set()
    selection_set.on_selection_change.remove_callable(selection_tracker)
    selection_set.on_selection_change.add_callable(selection_tracker)

def selection_tracker(selection_set):
    """
    List the contents of the provided selection set object

    parameters:
        selection_set: the unreal.TypedElementSelectionSet selection set to query
    """
    if selection_set.get_num_selected_elements():
        print(f"The following objects are currently selected:")
        for selected in selection_set.get_selected_objects():
             print(f"\t{selected.get_path_name()}")
    else:
        print("no objects selected!")
