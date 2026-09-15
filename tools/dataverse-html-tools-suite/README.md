# Dataverse HTML Tools Suite

`Dataverse HTML Tools Suite` is the combined installation option for all repository tools. It includes the `Admin Tools` model-driven app, eight HTML web resources, dedicated User and Team forms, and the Tenant Role Catalogue standalone page.

## Included experience

- `Admin Tools` model-driven app.
- Default User and Team list views.
- `Admin Tools User` form, preserving standard tabs and adding `Effective Security Roles` and `User Record Access`.
- `Admin Tools Team` form, preserving standard tabs and adding `Team Role and People Manager`.
- Standalone navigation pages for Flow Dependency Viewer, Role Table Permission Copier, Solution Service Inspector, Business Unit Configuration, and Tenant Role Catalogue.

Business Unit Configuration filters and sorts users, previews batch business-unit moves, calls the supported Dataverse `SetBusinessSystemUser` action, requires a record-reassignment principal, and can optionally clone destination-business-unit role matches and owner-team memberships from a source user.

The included User tool supports direct-role, owner-team, and optional record-specific access-team copying with `Add` and `Clone` modes. The User and Team tools identify group-backed Dataverse teams and link available Entra group IDs to the correct Commercial, GCC, GCC High, or DoD Entra admin center.

Tenant Role Catalogue loads roles from the current Dataverse environment, imports tenant-wide inventory JSON from a separately configured Power Automate collector, filters and exports JSON/CSV, and generates explicit reviewed role-create request JSON for separate automation. Importing the Suite bundles the UI only; it does not install a tenant-wide collector or role-create cloud flow.

## Install

Import one archive from [`packages/dataverse-html-tools-suite`](../../packages/dataverse-html-tools-suite):

- `DataverseHTMLToolsSuite_managed.zip` for a managed deployment.
- `DataverseHTMLToolsSuite.zip` for development or customization.

After import, publish customizations if Dataverse prompts for it, then grant users access to the `Admin Tools` app and required Dataverse privileges. The tools execute using the signed-in user's permissions. Tenant-wide Tenant Role Catalogue inventory and role-create execution still require separately reviewed and configured Power Automate flows with appropriate administrator connections.

## Build

From `tools/dataverse-html-tools-suite`, run `python3 validate-suite.py` before building. Build `solution/DataverseHTMLToolsSuite.cdsproj` in Release configuration; it produces both managed and unmanaged solution ZIPs. Alternatively run `pac solution pack --zipfile <output>.zip --folder solution/src --packagetype Unmanaged` (and `Managed`). Always regenerate the package ZIPs with SolutionPackager: archives assembled by hand are rejected on import with `The solution file is invalid`. After regenerating the package ZIPs, run `python3 validate-suite.py --check-packages`.