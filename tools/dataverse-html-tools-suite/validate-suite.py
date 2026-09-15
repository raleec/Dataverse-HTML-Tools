#!/usr/bin/env python3
"""Static validation for the Dataverse HTML Tools Suite solution metadata."""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "tools" / "dataverse-html-tools-suite"
SOLUTION = SUITE / "solution" / "src"
TENANT_SOURCE = ROOT / "tools" / "tenant-role-catalogue" / "src" / "TenantRoleCatalogue.html"
TENANT_SUITE = SOLUTION / "WebResources" / "dht_" / "TenantRoleCatalogue.html"
TENANT_METADATA = TENANT_SUITE.with_suffix(TENANT_SUITE.suffix + ".data.xml")
TENANT_PAYLOAD = "WebResources/dht_TenantRoleCataloguehtml9B0A9949-2D2D-4F35-8D22-56D5377EDC2F"
REQUIRED_NAV_URLS = {
    "$webresource:fdv_/flowdependencyviewer.htm": "Flow Dependency Viewer",
    "$webresource:dht_/RoleTablePermissionCopier.html": "Role Table Permission Copier",
    "$webresource:dht_/SolutionServiceInspector.html": "Solution Service Inspector",
    "$webresource:dht_/BusinessUnitConfiguration.html": "Business Unit Configuration",
    "$webresource:dht_/TenantRoleCatalogue.html": "Tenant Role Catalogue",
}
ZIP_PATHS = [
    ROOT / "packages" / "dataverse-html-tools-suite" / "DataverseHTMLToolsSuite.zip",
    ROOT / "packages" / "dataverse-html-tools-suite" / "DataverseHTMLToolsSuite_managed.zip",
]


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def validate_source(failures: list[str]) -> None:
    require(TENANT_SOURCE.exists(), f"Missing source HTML: {TENANT_SOURCE}", failures)
    require(TENANT_SUITE.exists(), f"Missing suite web resource: {TENANT_SUITE}", failures)
    if TENANT_SOURCE.exists() and TENANT_SUITE.exists():
        require(
            TENANT_SOURCE.read_bytes() == TENANT_SUITE.read_bytes(),
            "Suite TenantRoleCatalogue.html must match tools/tenant-role-catalogue/src/TenantRoleCatalogue.html",
            failures,
        )

    metadata = read(TENANT_METADATA) if TENANT_METADATA.exists() else ""
    require(TENANT_METADATA.exists(), f"Missing metadata: {TENANT_METADATA}", failures)
    for expected in [
        "<Name>dht_/TenantRoleCatalogue.html</Name>",
        "<DisplayName>Tenant Role Catalogue</DisplayName>",
        "<WebResourceType>1</WebResourceType>",
        f"<FileName>/{TENANT_PAYLOAD}</FileName>",
    ]:
        require(expected in metadata, f"Tenant metadata missing {expected}", failures)

    solution = read(SOLUTION / "Other" / "Solution.xml")
    require(
        '<RootComponent type="61" schemaName="dht_/TenantRoleCatalogue.html" behavior="0" />' in solution,
        "Solution.xml is missing Tenant Role Catalogue root component",
        failures,
    )

    for sitemap in [
        SOLUTION / "AppModuleSiteMaps" / "admin_tools_0b5e60bd" / "AppModuleSiteMap.xml",
        SOLUTION / "AppModuleSiteMaps" / "admin_tools_0b5e60bd" / "AppModuleSiteMap_managed.xml",
    ]:
        content = read(sitemap)
        for url, title in REQUIRED_NAV_URLS.items():
            require(url in content, f"{sitemap.name} missing navigation URL {url}", failures)
            require(f'Title="{title}"' in content, f"{sitemap.name} missing title {title}", failures)


def validate_packages(failures: list[str]) -> None:
    for package in ZIP_PATHS:
        require(package.exists(), f"Missing package ZIP: {package}", failures)
        if not package.exists():
            continue
        with zipfile.ZipFile(package) as archive:
            names = set(archive.namelist())
            require(TENANT_PAYLOAD in names, f"{package.name} missing {TENANT_PAYLOAD}", failures)
            if "solution.xml" in names:
                solution = archive.read("solution.xml").decode("utf-8-sig")
                require("dht_/TenantRoleCatalogue.html" in solution, f"{package.name} solution.xml missing Tenant Role Catalogue", failures)
            else:
                failures.append(f"{package.name} missing solution.xml")
            if "customizations.xml" in names:
                customizations = archive.read("customizations.xml").decode("utf-8-sig")
                require("dht_/TenantRoleCatalogue.html" in customizations, f"{package.name} customizations.xml missing Tenant Role Catalogue", failures)
                require("Tenant Role Catalogue" in customizations, f"{package.name} customizations.xml missing Tenant Role Catalogue navigation title", failures)
            else:
                failures.append(f"{package.name} missing customizations.xml")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-packages", action="store_true", help="also validate regenerated suite ZIP contents")
    args = parser.parse_args()

    failures: list[str] = []
    validate_source(failures)
    if args.check_packages:
        validate_packages(failures)

    if failures:
        print("Suite validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    suffix = " and packages" if args.check_packages else ""
    print(f"Suite validation passed for source metadata{suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
