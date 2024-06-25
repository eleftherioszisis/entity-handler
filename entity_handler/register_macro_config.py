from cwl_registry.nexus import get_forge
from kgforge.core import Resource
import json
from pathlib import Path


CONFIGS_DIR = Path(__file__).parent / "configs"
OUTPUT_DIR = Path(__file__).parent / "out"


DATA_DIR = Path(__file__).parent / "data"

PROD_CONNECTION_MATRIX = "https://bbp.epfl.ch/neurosciencegraph/data/connectomestrength/8e285d4b-4d09-4357-98ae-9e9fc61face6"


PROD_MACRO_CONFIG_ID = "https://bbp.epfl.ch/neurosciencegraph/data/6aef1bea-e66f-4b9f-b3ac-70fcce4e3636"



def overrides_resource(forge):

    r = Resource(
        type=["Entity", "Dataset", "BrainConnectomeStrengthOverrides"],
        distribution=forge.attach(
            path=str(DATA_DIR / "overrides_130263.arrow"),
            content_type="application/arrow"
        )
    )
    forge.register(r)
    assert r.id

    return r.id


def base_matrix_resource(forge):
    r = Resource(
        type=["Entity", "Dataset", "BrainConnectomeStrength"],
        distribution=forge.attach(
            path=str(DATA_DIR / "all.arrow"),
            content_type="application/arrow"
        )
    )
    forge.register(r)
    assert r.id

    return r.id


def prod_json_macro_payload(forge):
    return {
        "bases": {
            "connection_strength": {
                "id": PROD_CONNECTION_MATRIX,
                "type": ["Entity", "Dataset", "BrainConnectomeStrength"],
                "rev": 1
            }
        },
        "overrides": {
            "connection_strength": {
                "id": overrides_resource(forge),
                "type": ["Entity", "Dataset", "BrainConnectomeStrengthOverrides"],
                "rev": 1
            }
        }
    }


def register_macro_connectome_config(forge, existing_id=None):

    name = "MacroConnectomeConfig manual example [DO NOT USE]"

    if existing_id:

        config_path = Path(CONFIGS_DIR / "macroconnectome-config.json")
        r = forge.retrieve(existing_id, cross_bucket=True)
        r.name = name
        r.distribution=forge.attach(config_path, content_type="application/json")
        forge.update(r)

    else:

        json_data = prod_json_macro_payload(forge)
        raw_file = Path(OUTPUT_DIR / "macroconnectome-config.json")
        raw_file.write_text(json.dumps(json_data, indent=2))

        r = Resource(
            name=name,
            type="MacroConnectomeConfig",
            distribution=forge.attach(raw_file, content_type="application/json"),
        )

        forge.register(r)
    assert r.id
    print(r._store_metadata._self)


if __name__ == "__main__":
    forge = get_forge()
    register_macro_connectome_config(forge, existing_id=PROD_MACRO_CONFIG_ID)
