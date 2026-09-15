# Tenant Role Catalogue Power Automate Collector Flow

Use this collector design when you need tenant-level security-role inventory without adding an app registration or custom service.

## Connector actions

Preferred actions:

| Connector | Action | Purpose |
|---|---|---|
| Power Platform for Admins V2 | List Environments as Admin | Discovers environments visible to the admin connection |
| Dataverse or HTTP with Microsoft Entra ID | List rows / Web API request | Reads `roles` from each environment |
| SharePoint or OneDrive for Business | Create file | Saves the collector JSON |

Graceful fallbacks when **Power Platform for Admins V2** is unavailable:

| Fallback | When to use | Output expected by the HTML tool |
|---|---|---|
| Power Platform for Admins legacy action | V2 action is not present in the tenant or cloud | Same environment fields as V2 when available |
| Manual environment array trigger input | Admin connector cannot enumerate environments | JSON array with environment name, display name, and Dataverse URL |
| Partial export with failures | Some environments deny access or lack Dataverse metadata | `failures[]`, `SkippedEnvironments[]`, or `EnvironmentFallbacks[]` |

## Flow outline

1. Create an instant cloud flow restricted to administrators.
2. Add optional trigger inputs:
   - `ManualEnvironmentsJson`
   - `OutputSiteUrl`
   - `OutputFolderPath`
   - `IncludePrivilegeCounts`
3. Initialize arrays named `Environments`, `Roles`, and `Failures`.
4. Try **Power Platform for Admins V2 - List Environments as Admin**.
5. If the V2 action is unavailable or fails, try the legacy Power Platform admin connector action.
6. If admin connector discovery still fails, parse `ManualEnvironmentsJson`.
7. For each environment, resolve a Dataverse organization URL from connector metadata or the manual input.
8. For each resolved environment URL, read roles from Dataverse:
   - `roles?$select=name,roleid,_businessunitid_value,ismanaged&$orderby=name asc`
9. Optionally add privilege counts by reading `roleprivilegescollection` or `roleprivileges` per role.
10. Append successful rows under that environment's `roles` array.
11. Append denied, skipped, or malformed environments to `Failures` with the connector action and message.
12. Create a JSON file and import it in Tenant Role Catalogue.

## Expected JSON shape

```json
{
  "schema": "DataverseHtmlTools.TenantRoleCatalogue.v1",
  "environmentDiscoveryMode": "Power Platform for Admins V2",
  "exportedAt": "2026-09-15T17:55:20.701Z",
  "environments": [
    {
      "environmentName": "Default-00000000-0000-0000-0000-000000000000",
      "environmentDisplayName": "Default",
      "environmentId": "00000000-0000-0000-0000-000000000000",
      "environmentUrl": "https://org.crm.dynamics.com",
      "roles": [
        {
          "roleName": "System Administrator",
          "roleId": "00000000-0000-0000-0000-000000000000",
          "businessUnitName": "Contoso",
          "businessUnitId": "00000000-0000-0000-0000-000000000000",
          "isManaged": true,
          "privilegeCount": 1234
        }
      ]
    }
  ],
  "failures": []
}
```

## Manual environment fallback input

When environment discovery cannot use either admin connector version, provide a trigger input like:

```json
[
  {
    "environmentName": "Default-00000000-0000-0000-0000-000000000000",
    "environmentDisplayName": "Default",
    "environmentUrl": "https://org.crm.dynamics.com"
  }
]
```

The flow should include a failure row stating which discovery method failed and that manual input was used.

## Role-create request processing

Tenant Role Catalogue can generate request JSON with schema `DataverseHtmlTools.TenantRoleCatalogue.CreateRoles.v1`.

A role-create flow should:

1. Parse and validate the request schema.
2. Require an explicit administrator confirmation before writes.
3. For each target environment, connect to that environment's Dataverse URL.
4. Resolve the optional source role by name and business unit in that environment.
5. Create the new role in the intended business unit.
6. Copy source privileges only after resolving privilege records in the same environment.
7. Return per-environment success, skipped, and failure rows.

## Notes

- Do not reuse role IDs, business-unit IDs, or privilege IDs across environments.
- Keep connector connections restricted to administrators.
- Store generated files in a controlled location because tenant role catalogues are sensitive.
- Capture partial failures instead of failing the entire run when one environment denies access.
