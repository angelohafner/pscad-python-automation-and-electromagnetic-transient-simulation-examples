"""
PSCAD Component Catalog Generator

Creates a database containing all component definitions
available in the currently loaded PSCAD workspace.

Outputs:
    pscad_component_catalog.csv
    pscad_component_catalog.json
"""

import csv
import json
from pathlib import Path

import mhi.pscad


OUTPUT_DIR = Path(__file__).resolve().parent / "pscad_component_database"

CSV_FILE = OUTPUT_DIR / "pscad_component_catalog.csv"
JSON_FILE = OUTPUT_DIR / "pscad_component_catalog.json"


def get_definition_metadata(definition):
    """
    Retrieve metadata associated with a PSCAD component definition.
    """

    try:
        metadata = definition.parameters() or {}
    except Exception:
        metadata = {}

    return metadata


def collect_definitions(pscad):
    """
    Collect all component definitions from all loaded PSCAD projects.
    """

    catalog = []

    projects = pscad.projects()

    for project_info in projects:

        project_name = project_info["name"]
        project_type = project_info["type"]

        print("=" * 80)
        print(f"Project: {project_name}")
        print(f"Type   : {project_type}")
        print("=" * 80)

        project = pscad.project(project_name)

        try:
            definition_names = project.definitions()
        except Exception as exc:
            print(f"Could not retrieve definitions: {exc}")
            continue

        for definition_name in sorted(definition_names):

            try:
                definition = project.definition(definition_name)
            except Exception as exc:
                print(
                    f"Could not access definition "
                    f"{project_name}:{definition_name}: {exc}"
                )
                continue

            metadata = get_definition_metadata(definition)

            try:
                scoped_name = definition.scoped_name
            except Exception:
                scoped_name = f"{project_name}:{definition_name}"

            try:
                is_module = definition.is_module()
            except Exception:
                is_module = None

            record = {
                "project": project_name,
                "project_type": project_type,
                "definition": definition_name,
                "scoped_name": scoped_name,
                "description": metadata.get("desc", ""),
                "group": metadata.get("group", ""),
                "tags": metadata.get("tags", ""),
                "url": metadata.get("url", ""),
                "is_module": is_module,
            }

            catalog.append(record)

            print(
                f"{scoped_name:<40} "
                f"{record['description']}"
            )

        print(f"\nDefinitions found: {len(definition_names)}\n")

    return catalog


def export_csv(catalog):
    """
    Export the component catalog to CSV.
    """

    if not catalog:
        return

    fieldnames = [
        "project",
        "project_type",
        "definition",
        "scoped_name",
        "description",
        "group",
        "tags",
        "url",
        "is_module",
    ]

    with CSV_FILE.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(catalog)


def export_json(pscad, catalog):
    """
    Export the component catalog to JSON.
    """

    try:
        pscad_version = str(pscad.version)
    except Exception:
        pscad_version = "unknown"

    database = {
        "pscad_version": pscad_version,
        "total_definitions": len(catalog),
        "components": catalog,
    }

    with JSON_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            database,
            file,
            indent=4,
            ensure_ascii=False,
        )


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 80)
    print("Connecting to PSCAD")
    print("=" * 80)

    pscad = mhi.pscad.application()

    print("Connected successfully.")

    print("\n" + "=" * 80)
    print("Collecting PSCAD Component Definitions")
    print("=" * 80)

    catalog = collect_definitions(pscad)

    export_csv(catalog)
    export_json(pscad, catalog)

    print("=" * 80)
    print("Catalog completed")
    print("=" * 80)

    print(f"Total definitions: {len(catalog)}")
    print(f"CSV : {CSV_FILE}")
    print(f"JSON: {JSON_FILE}")


if __name__ == "__main__":
    main()