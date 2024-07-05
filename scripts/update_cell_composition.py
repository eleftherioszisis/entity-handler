import json
import logging
from copy import deepcopy

from entity_management.config import ModelBuildingConfig
from entity_management.atlas import CellComposition
from entity_management.core import Entity,  attributes, AttrOf, BlankNode, DataDownload
from entity_management.base import Derivation
from entity_management.exception import ResourceNotFoundError

from entity_management.util import get_entity
from entity_management.nexus import load_by_id
from entity_handler.entities.cell_composition_config import cli as cell_composition_config_cli
from entity_handler.entities.cell_composition_config.cli import update_entity_distribution

logging.basicConfig(level=logging.INFO)

@attributes({
    "distribution": AttrOf(DataDownload),
    "derivation": AttrOf(Derivation, default=None),
})
class CanonicalMorphologyModelConfig(Entity):
    """Canonical morphology model config."""


@attributes({
    "distribution": AttrOf(DataDownload, default=None),
    "derivation": AttrOf(Derivation, default=None),
})
class PlaceholderMorphologyConfig(Entity):
    """Placeholder morphologies config."""


PLACEHOLDER_ID = "https://bbp.epfl.ch/data/bbp/mmb-point-neuron-framework-model/9829da8e-33e1-4a04-97ec-7943a4a969eb"


L = logging.getLogger(__name__)


def main(config_id, composition_id):

    model_config = get_entity(config_id, cls=ModelBuildingConfig)
    sub_configs = model_config.configs

    composition = get_entity(composition_id, cls=CellComposition)

    if sub_configs.cellCompositionConfig:
        cell_composition_config_cli.update_cell_composition_id(
            config=sub_configs.cellCompositionConfig,
            composition_id=composition_id,
        )

    if sub_configs.cellPositionConfig:
        L.info("CellPositionConfig does not require changes.")

    if sub_configs.morphologyAssignmentConfig:
        update_mmodel_config_default_distributions(
            config=sub_configs.morphologyAssignmentConfig,
            composition=composition,
        )

    if sub_configs.meModelConfig:
        print("4")

    if sub_configs.microConnectomeConfig:
        print("5")

    if sub_configs.synapseConfig:
        print("6")

    if sub_configs.macroConnectomeConfig:
        print("7")


from entity_handler import query


def _is_up_to_data(config, composition):

    def _in_derivation(derivation):
        entity = derivation.entity
        return entity.get_id() == composition.get_id() and entity.get_rev() == composition.get_rev()

    defaults = config.distribution.as_dict()["defaults"]

    try:
        canonical_config = get_entity(defaults["topological_synthesis"]["@id"], cls=CanonicalMorphologyModelConfig)
        placeholder_config = get_entity(defaults["placeholder_assignment"]["@id"], cls=PlaceholderMorphologyConfig)
    except ResourceNotFoundError:
        return False

    return not (
        canonical_config._deprecated or
        placeholder_config._deprecated or
        canonical_config.derivation is None or
        placeholder_config.derivation is None or
        not _in_derivation(canonical_config.derivation) or
        not _in_derivation(placeholder_config.derivation)
    )


def update_mmodel_config_default_distributions(config, composition):

    summary = composition.cellCompositionSummary
    placeholder = get_entity(PLACEHOLDER_ID, cls=Entity)

    if _is_up_to_data(config, composition):
        L.info("Config is already up to date with the composition.")
        return

    canonical_ids = query.by_type("CanonicalMorphologyModel")

    # get all canonical models from KG bucket
    canonical_catalog = {}
    for canonical_id in query.by_type("CanonicalMorphologyModel"):

        canonical_data = load_by_id(canonical_id)
        assert canonical_data is not None

        mtype_label = canonical_data["annotation"]["hasBody"]["label"]

        assert mtype_label not in canonical_catalog

        canonical_catalog[mtype_label] = {
            "@id": canonical_data["@id"],
            "_rev": canonical_data["_rev"],
        }

    data = summary.distribution.as_dict()
    canonical_distribution = deepcopy(data)
    placeholder_distribution = deepcopy(data)

    # Traverse the summary and assign for each region/mtype a canonical or placeholder morphology
    for region_id, region_data in data["hasPart"].items():
        L.info("Region: %s", region_data["label"])
        for mtype_id, mtype_data in region_data["hasPart"].items():
            L.info("\tMType: %s", mtype_data["label"])

            mtype_label = mtype_data["label"]
            canonical_data = canonical_catalog[mtype_label]

            canonical_distribution["hasPart"][region_id]["hasPart"][mtype_id]["hasPart"] = {
                canonical_data["@id"]: {
                    "about": "CanonicalMorphologyModel",
                    "_rev": canonical_data["_rev"],
                }
            }
            placeholder_distribution["hasPart"][region_id]["hasPart"][mtype_id]["hasPart"] = {
                placeholder.get_id(): {
                  "about": "NeuronMorphology",
                  "_rev": placeholder.get_rev(),
                }
            }

    # this will help us track if we need to update again in the future
    derivation = Derivation(entity=composition)

    canonical_config = CanonicalMorphologyModelConfig(
        name="Default Canonical Morphology Models",
        description=(
            "Default canonical morphology models for all region/mtype pairs in the CellComposition."
        ),
        derivation=derivation,
        distribution=DataDownload.from_json_str(
            json_str=json.dumps(canonical_distribution, indent=2),
            name="canonicals.json",
        ),
    ).publish(include_rev=True)  # include_rev needed to pin CellComposition derivation rev
    L.info("Default canonical models registered at %s", canonical_config.get_id())

    placeholder_config = PlaceholderMorphologyConfig(
        name="Default Placeholder morphologies",
        description=(
            "Default placeholders for all region/mtype pairs in the CellComposition."
        ),
        derivation=derivation,
        distribution=DataDownload.from_json_str(
            json_str=json.dumps(placeholder_distribution, indent=2),
            name="placeholders.json",
        )
    ).publish(include_rev=True)  # include_rev needed to pin CellComposition derivation rev
    L.info("Default placeholders registered at %s", placeholder_config.get_id())

    # update the MorphologyAssignmentConfig with the new datasets
    with update_entity_distribution(entity=config) as config_data:
        config_data["defaults"] = {
            "topological_synthesis": {
                "@id": canonical_config.get_id(),
                "@type": type(canonical_config).__name__,
            },
            "placeholder_assignment": {
                "@id": placeholder_config.get_id(),
                "@type": type(placeholder_config).__name__,
            }
        }
        L.info(
            "MorphologyAssignmentConfig %s distribution was updated.\n"
            "New defaults:\n%s",
            config.get_id(),
            json.dumps(config_data["defaults"], indent=2),
        )


if __name__ == "__main__":

    # ModelBuildinConfig to update
    config_id = "https://bbp.epfl.ch/data/bbp/mmb-point-neuron-framework-model/d28580b8-9fc8-4b04-8e67-11229b31726c"

    # composition to be linked and used for default configurations
    composition_id = "https://bbp.epfl.ch/neurosciencegraph/data/cellcompositions/54818e46-cf8c-4bd6-9b68-34dffbc8a68c?tag=v1.1.0"

    main(
        config_id=config_id,
        composition_id=composition_id,
    )
