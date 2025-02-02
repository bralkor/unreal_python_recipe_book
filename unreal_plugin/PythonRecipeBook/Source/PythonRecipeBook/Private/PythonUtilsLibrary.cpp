#include "PythonUtilsLibrary.h"

#include "Editor.h"
#include "EditorUtilityWidgetBlueprint.h"
#include "EditorUtilitySubsystem.h"
#include "UObject/ObjectRedirector.h"
#include "ObjectTools.h"
#include "UObject/SoftObjectPath.h"

#define LOCTEXT_NAMESPACE "PythonUtils"

TArray<FString>
UPythonUtilsLibrary::GetClassPropertyNames(UClass* Class) {
    TArray<FString> Ret;
    if (Class) {
        for (TFieldIterator<FProperty> It(Class); It; ++It) {
            FProperty* Property = *It;
            if (Property->HasAnyPropertyFlags(EPropertyFlags::CPF_Edit)) {
                Ret.Add(Property->GetName());
            }
        }
    }
    return Ret;
}

void
UPythonUtilsLibrary::ClearEditorTools() {
    UEditorUtilitySubsystem* EUS = GEditor->GetEditorSubsystem<UEditorUtilitySubsystem>();
    EUS->LoadedUIs.Empty();
    EUS->SaveConfig();
}

void
UPythonUtilsLibrary::ClearEditorToolFromPrefs(UEditorUtilityWidgetBlueprint* EditorWidget) {
    UEditorUtilitySubsystem* EUS = GEditor->GetEditorSubsystem<UEditorUtilitySubsystem>();
    EUS->LoadedUIs.Remove(EditorWidget);
    EUS->SaveConfig();
}

void
UPythonUtilsLibrary::RegisterMetadataTags(const TArray<FName>& Tags)
{
	TSet<FName>& GlobalTagsForAssetRegistry = UObject::GetMetaDataTagsForAssetRegistry();
	for (FName Tag : Tags)
	{
		if (!Tag.IsNone())
		{
			if (!GlobalTagsForAssetRegistry.Contains(Tag))
			{
				GlobalTagsForAssetRegistry.Add(Tag);
			}
		}
	}
}

#undef LOCTEXT_NAMESPACE