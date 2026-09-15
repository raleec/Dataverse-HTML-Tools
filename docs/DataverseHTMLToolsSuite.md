# Dataverse HTML Tools Suite

The Suite is the single installable option for the complete admin-tool set. It contains the `Admin Tools` model-driven app and all eight HTML web resources.

## Admin Tools app

The app provides the default Team and User list views. It intentionally does not replace them with custom views.

Opening a Team record uses only the `Admin Tools Team` form. That form keeps the standard Team tabs and adds the `Team Role and People Manager` tab.

Opening a User record uses only the `Admin Tools User` form. That form keeps the standard User tabs and adds `Effective Security Roles` and `User Record Access` tabs.

The app also contains standalone navigation pages for Flow Dependency Viewer, Role Table Permission Copier, Solution Service Inspector, Business Unit Configuration, and Tenant Role Catalogue.

## Install

Choose the managed or unmanaged archive in [`packages/dataverse-html-tools-suite`](../packages/dataverse-html-tools-suite). Import it into a Dataverse environment, publish customizations if prompted, and give administrators access to the `Admin Tools` model-driven app.

The Suite does not grant privileges. Each web resource runs under the signed-in user's Dataverse security context. Tenant Role Catalogue tenant-wide inventory and role-create execution still require separately configured and reviewed Power Automate automation; the Suite bundles the UI, not those flows.