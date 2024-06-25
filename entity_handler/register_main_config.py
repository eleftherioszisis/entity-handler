import logging
from pathlib import Path
from kgforge.core import Resource
import json
from cwl_registry.nexus import get_forge

from . import register_macro_connectome_config, register_micro_connectome_config

logging.basicConfig(level=logging.DEBUG)

# forge(bucket='bbp/mmb-point-neuron-framework-model')
# forge(bucket='nse/test')

ROOT_ID = "http://api.brain-map.org/api/v2/data/Structure/997"


CONFIGS_DIR = Path(__file__).parent / "configs"
OUTPUT_DIR = Path(__file__).parent / "out"

WARNING = "[DO NOT USE | DO NOT DEPRECATE]"


def register_json_config(forge, generator_name, resource_type, path, existing_id=None):
    assert path.exists()

    r = get_resource(forge, existing_id) if existing_id else Resource()

    r.name = f"{resource_type} manual example {WARNING}"
    r.type = resource_type
    r.distribution = forge.attach(path, content_type="application/json")

    if generator_name:
        r.generatorName = generator_name

    if existing_id:
        forge.update(r)
        print(f"Updated {resource_type}: {r._store_metadata._self}")
    else:
        forge.register(r)
        print(f"Registered {resource_type}: {r._store_metadata._self}")

    return r.id, r._store_metadata._rev


generator_configs = {
    "cellCompositionConfig": {
        "generator_name": "cell_composition",
        "filename": "cell-composition-config.json",
        "function": register_json_config,
        "id": {
            "prod": "https://bbp.epfl.ch/neurosciencegraph/data/d199df29-d511-4681-b807-a8c82ccf1310",
            "staging": None,
        },
    },
    "cellPositionConfig": {
        "generator_name": "cell_position",
        "filename": "cell-position-config.json",
        "function": register_json_config,
        "id": {
            "prod": "https://bbp.epfl.ch/neurosciencegraph/data/d019400e-54c1-4cf4-aeeb-6c962e66eb51",
            "staging": None,
        },
    },
    "eModelAssignmentConfig": {
        "generator_name": "placeholder",
        "filename": "emodel-assignment-config.json",
        "function": register_json_config,
        "id": {
            "prod": "https://bbp.epfl.ch/neurosciencegraph/data/01fa65c0-8f75-4c7e-b1e7-0564319597ef",
            "staging": None,
        },
    },
    "morphologyAssignmentConfig": {
        "generator_name": "placeholder",
        "filename": "morphology-assignment-config.json",
        "function": register_json_config,
        "id": {
            "prod": "https://bbp.epfl.ch/neurosciencegraph/data/6fe9f2ba-6765-4a4b-a073-21d4e9183c14",
            "staging": None,
        },
    },
    "macroConnectomeConfig": {
        "generator_name": None,
        "filename": "macroconnectome-config.json",
        "function": register_json_config,
        "id": {
            "prod": "https://bbp.epfl.ch/neurosciencegraph/data/6aef1bea-e66f-4b9f-b3ac-70fcce4e3636",
            "staging": None,
        },
    },
    "microConnectomeConfig": {
        "generator_name": "connectome",
        "filename": "microconnectome-config.json",
        "function": register_json_config,
        "id": {
            "prod": "https://bbp.epfl.ch/neurosciencegraph/data/fc6ee68a-2278-4dd6-96c9-a3824d4690f2",
            "staging": None,
        },
    },
    "synapseConfig": {
        "generator_name": "connectome_filtering",
        "filename": "synapse-editor-config.json",
        "function": register_json_config,
        "id": {
            "prod": "https://bbp.epfl.ch/neurosciencegraph/data/synapseconfigs/689eaae6-e7bf-4643-977d-30267eaaf963",
            "staging": None,
        },
    },
}


def main(forge, mode, existing_id=None):
    configs_dir = CONFIGS_DIR / mode

    configs = {}
    for name, config in generator_configs.items():
        config_type = [name[0].upper() + name[1:], "Entity"]

        resource_id, rev = config["function"](
            forge=forge,
            resource_type=config_type,
            path=configs_dir / config["filename"],
            generator_name=config["generator_name"],
            existing_id=config["id"][mode],
        )

        configs[name] = {
            "@id": resource_id,
            "@type": config_type,
        }

    resource = get_resource(forge, existing_id) if existing_id else Resource()

    resource.name = f"ModelBuildingConfig manual example {WARNING}"
    resource.type = ["ModelBuildingConfig", "Entity"]
    resource.configs = configs

    if existing_id:
        forge.update(resource)
    else:
        forge.register(resource)

    print(resource._store_metadata._self)


if __name__ == "__main__":
    prod_existing_id = "https://bbp.epfl.ch/neurosciencegraph/data/09e7e53d-d519-45c0-ba51-df0967fce989"

    nexus_org = "bbp_test"
    nexus_project = "studio_data_11"

    forge = get_forge(nexus_org=nexus_org, nexus_project=nexus_project)
    main(forge, "prod", existing_id=prod_existing_id)

    # nexus_org = "bbp"
    # nexus_project = "mmb-point-neuron-framework-model"
    # forge = get_forge(nexus_org=nexus_org, nexus_project=nexus_project)
    # main(forge, "staging")
