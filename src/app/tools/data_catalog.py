import json
from pathlib import Path
from langchain_core.tools import StructuredTool

catalog_path = (
    Path(__file__).parent.parent.parent.parent / "resources/data_catalog.json"
)

with open(catalog_path, "r") as f:
    DATA_CATALOG = json.load(f)


def list_data_sources() -> list[dict]:
    """Return a list of available data sources & their descriptions in the catalog."""

    data_sources = DATA_CATALOG["dataCatalog"]["dataSources"]
    data_source_info = []

    for ds in data_sources:
        ds_info = {
            "id": ds["id"],
            "name": ds["name"],
            "description": ds["description"],
            "datasets": [],
        }

        for dataset in ds.get("datasets", []):
            dataset_info = {
                "id": dataset["id"],
                "name": dataset["name"],
                "description": dataset["description"],
            }
            ds_info["datasets"].append(dataset_info)

        data_source_info.append(ds_info)

    return data_source_info


list_data_sources_tool = StructuredTool.from_function(
    func=list_data_sources,
    name="list_data_sources",
    description="List all available data sources and their descriptions in the data catalog.",
)
