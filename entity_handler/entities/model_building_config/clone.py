import attr
import logging
import tempfile
from pathlib import Path
from entity_management.core import DataDownload
from entity_management.config import ModelBuildingConfig
from entity_management.config import Configs

from entity_management.util import get_entity


L = logging.getLogger(__name__)


def clone_model_building_config(obj, name: str, description: str | None = None):

    if isinstance(obj, str):
        obj = get_entity(obj, cls=ModelBuildingConfig)

    if name == obj.name:
        raise ValueError("Clone name must be different than the original.")

    new_configs = _clone_sub_configs(obj.configs)

    new_model_building_config = obj.evolve(
        configs=new_configs,
        name=name,
        description=description or obj.description,
    )
    new_model_building_config._force_attr("_id", None)

    return new_model_building_config.publish()


def _clone_sub_configs(configs):
    new_configs = {}
    for config_attr in attr.fields(attr.fields(ModelBuildingConfig).configs.type):
        if sub_config := getattr(configs, config_attr.name):
            new_configs[config_attr.name] = _clone_sub_config(sub_config)
    return configs.evolve(**new_configs)


def _clone_sub_config(sub_config):
    distribution = _clone_distribution(sub_config.distribution)
    new_sub_config = sub_config.evolve(distribution=distribution)
    new_sub_config._force_attr("_id", None)
    new_sub_config = new_sub_config.publish()
    L.info(
        f"Cloned {type(sub_config).__name__}:\n"
        f" from: {sub_config.get_id()}\n"
        f" to  : {new_sub_config.get_id()}"
    )
    return new_sub_config


def _clone_distribution(distribution):

    filepath = distribution.get_location_path()

    if Path(filepath).exists():
        new_distribution = DataDownload.from_file(
            file_like=filepath,
            name=distribution.name,
            content_type=distribution.encodingFormat,
        )
    else:
        with tempfile.TemporaryDirectory() as tdir:
            filepath = distribution.download(path=tdir)
            new_distribution = DataDownload.from_file(
                file_like=filepath,
                name=distribution.name,
                content_type=distribution.encodingFormat,
            )

    L.info(
        "Cloned distribution:\n"
        f"from: {distribution.contentUrl}\n"
        f"to  : {new_distribution.contentUrl}"
    )
    return new_distribution
