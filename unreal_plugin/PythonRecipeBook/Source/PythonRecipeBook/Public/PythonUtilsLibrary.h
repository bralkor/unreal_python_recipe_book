#pragma once

#include "Kismet/BlueprintFunctionLibrary.h"
#include "EditorUtilityWidgetBlueprint.h"

#include "PythonUtilsLibrary.generated.h"

/**
 * Blueprint Function Library to expose c++ functionality to Python
 *
 * This function library should be available in Python as:
 *     unreal.PythonUtils.*
*/
UCLASS()
class PYTHONRECIPEBOOK_API UPythonUtilsLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()
public:
    /**  List the Editor Property names of the given class
     * @param  Class  the Unreal Class to query the properties from
     *
     * @return  an array of property names for the given class
     */
    UFUNCTION(BlueprintCallable, Category = "Python | Utils")
    static TArray<FString> GetClassPropertyNames(UClass* Class);

    /**  Clear all Editor Utility Widgets from the User Prefs
     */
    UFUNCTION(BlueprintCallable, Category = "Python | Utils")
    static void ClearEditorTools();

    /**  Remove the given Editor Utility Widget from the User Prefs
     * @param  EditorWidgetInstance  the Editor Tool Instance
     */
    UFUNCTION(BlueprintCallable, Category = "Python | Utils")
    static void ClearEditorToolFromPrefs(UEditorUtilityWidgetBlueprint* EditorWidget);

    /**  Add new metadata tag names to the Asset Registry
     * @param  Tags  the metadata tags to add
     */
    UFUNCTION(BlueprintCallable, Category = "Python | Utils")
    static void RegisterMetadataTags(const TArray<FName>& Tags);
};