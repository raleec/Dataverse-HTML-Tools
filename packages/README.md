# Packages

This folder contains importable Dataverse solution packages.

Each listed tool currently has managed and unmanaged ZIP packages. The Suite is the recommended package for a complete installation.

## Recommended: Full Suite

Install the **Dataverse HTML Tools Suite** to get the `Admin Tools` model-driven app, dedicated User and Team forms, standalone tool pages including Tenant Role Catalogue, and every included web resource.

| Suite | Unmanaged package | Managed package |
|---|---|---|
| Dataverse HTML Tools Suite | [Unmanaged ZIP](dataverse-html-tools-suite/DataverseHTMLToolsSuite.zip) | [Managed ZIP](dataverse-html-tools-suite/DataverseHTMLToolsSuite_managed.zip) |

## Individual Tool Packages

Use an individual package only when the target environment needs a specific tool rather than the complete Suite. Individual packages do not add the `Admin Tools` app or its dedicated forms.

| Tool | Unmanaged package | Managed package |
|---|---|---|
| User Effective Security Roles | [Unmanaged ZIP](user-effective-security-roles/UserEffectiveSecurityRolesSolution.zip) | [Managed ZIP](user-effective-security-roles/UserEffectiveSecurityRolesSolution_managed.zip) |
| Role Table Permission Copier | [Unmanaged ZIP](role-table-permission-copier/RoleTablePermissionCopierSolution.zip) | [Managed ZIP](role-table-permission-copier/RoleTablePermissionCopierSolution_managed.zip) |
| Team Role and People Manager | [Unmanaged ZIP](team-role-people-manager/TeamRolePeopleManagerSolution.zip) | [Managed ZIP](team-role-people-manager/TeamRolePeopleManagerSolution_managed.zip) |
| Flow Dependency Viewer | [Unmanaged ZIP](flow-dependency-viewer/FlowDependencyViewerSolution.zip) | [Managed ZIP](flow-dependency-viewer/FlowDependencyViewerSolution_managed.zip) |
| Solution Service Inspector | [Unmanaged ZIP](solution-service-inspector/SolutionServiceInspectorSolution.zip) | [Managed ZIP](solution-service-inspector/SolutionServiceInspectorSolution_managed.zip) |
| Business Unit Configuration | [Unmanaged ZIP](business-unit-configuration/DataverseHtmlToolsBusinessUnitConfiguration.zip) | [Managed ZIP](business-unit-configuration/DataverseHtmlToolsBusinessUnitConfiguration_managed.zip) |

Tenant Role Catalogue is bundled in the Suite as an `Admin Tools` standalone page. It can still be deployed manually from `tools/tenant-role-catalogue` for source-only scenarios; tenant-wide inventory/create automation must be configured separately.

## Regenerating packages

Every ZIP in this folder is produced by SolutionPackager from the matching `tools/<tool>/solution/src` folder. Hand-assembled archives are rejected by Dataverse with `The solution file is invalid. The compressed file must contain the following files at its root: solution.xml, customizations.xml, and [Content_Types].xml.`

Build the `.cdsproj` in Release configuration, or use the Power Platform CLI directly:

```
pac solution pack --zipfile packages/<tool>/<Name>.zip --folder tools/<tool>/solution/src --packagetype Unmanaged
pac solution pack --zipfile packages/<tool>/<Name>_managed.zip --folder tools/<tool>/solution/src --packagetype Managed
```
