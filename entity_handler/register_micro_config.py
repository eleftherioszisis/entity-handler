from cwl_registry.nexus import get_forge, get_resource
from kgforge.core import Resource
import json
from pathlib import Path


CONFIGS_DIR = Path(__file__).parent / "configs"
OUTPUT_DIR = Path(__file__).parent / "out"

PROD_CONFIG_DIR = Path(__file__).parent / "configs"

DATA_DIR = Path(__file__).parent / "data"

PROD_MICRO_CONFIG_ID = "https://bbp.epfl.ch/neurosciencegraph/data/fc6ee68a-2278-4dd6-96c9-a3824d4690f2"


def register_micro_connectome_config(forge, existing_id=None):
    path = PROD_CONFIG_DIR / "microconnectome-config.json"

    name = "MicroConnectomeConfig manual example [DO NOT USE]"
    distribution = forge.attach(path, content_type="application/json")

    if existing_id:

        r = get_resource(forge, existing_id)
        r.distribution = distribution
        r.name = name
        forge.update(r)

    else:

        r = Resource(
            name=name,
            type="MicroConnectomeConfig",
            distribution=distribution
        )

        forge.register(r)
    assert r.id
    print(r._store_metadata._self)


if __name__ == "__main__":
    forge = get_forge()

    register_micro_connectome_config(forge, existing_id=PROD_MICRO_CONFIG_ID)
