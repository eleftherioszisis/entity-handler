import click
import json
import logging
import tempfile
from pathlib import Path
from contextlib import contextmanager

from entity_management.util import get_entity
from entity_management.config import CellCompositionConfig
from entity_management.core import DataDownload

from blue_cwl.utils import load_json, write_json

L = logging.getLogger(__name__)


ROOT_KEY = "http://api.brain-map.org/api/v2/data/Structure/997"


@contextmanager
def update_entity_distribution(entity):

    with tempfile.TemporaryDirectory() as tdir:

        filepath = entity.distribution.download(path=tdir)

        data = load_json(filepath)

        yield data

        write_json(data=data, filepath=filepath)

        new_distribution = DataDownload.from_file(filepath)

        entity = entity.evolve(distribution=new_distribution)

        entity.publish()


@contextmanager
def update_entity_distribution_if(entity, predicate=None):

    with tempfile.TemporaryDirectory() as tdir:

        filepath = entity.distribution.download(path=tdir)

        data = load_json(filepath)

        write_update = predicate(data) if predicate else True

        yield data

        if write_update:

            write_json(data=data, filepath=filepath)

            new_distribution = DataDownload.from_file(filepath)

            entity = entity.evolve(distribution=new_distribution)

            entity.publish()
            L.info(f"{type(entity).__nasme__} distribution updated.")
        else:
            L.warning(f"Entity {entity.get_id()} distribution is already up to date.")


def update_cell_composition_id(config, composition_id):

    with update_entity_distribution_if(
        entity=config,
        predicate=lambda data: data[ROOT_KEY]["inputs"][0]["id"] != composition_id,
    ) as data:
        data[ROOT_KEY]["inputs"][0]["id"] = composition_id


@click.group
def cell_composition_config():
    pass


@cell_composition_config.group()
def update():
    pass

@update.command
@click.option("--new-id", required=True)
@click.argument("resource-id", required=True)
def base_cell_composition_id(resource_id, new_id):

    config = get_entity(resource_id, cls=CellCompositionConfig)
    update_cell_composition_id(config, composition_config)

    click.echo(
        click.style(
            f"CellCompositionConfig {resource_id} base_cell_composition updated to {new_id}",
            fg="green",
        )
    )

@update.command
@click.option("--algorithm", required=False, default=None)
@click.option("--version", required=False, default=None)
@click.argument("resource-id", required=True)
def variant_definition(resource_id, algorithm, version):

    if algorithm is None and version is None:
        return

    config = get_entity(resource_id, cls=CellCompositionConfig)

    with update_entity_distribution(config) as data:

        definition = data[ROOT_KEY]["variantDefinition"]

        if algorithm:
            definition["algorithm"] = algorithm

        if version:
            definition["version"] = version


