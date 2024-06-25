import click
import logging

from entity_management.util import get_entity
from .clone import clone_model_building_config


L = logging.getLogger(__name__)


@click.group
def model_building_config():
    pass


@model_building_config.command
@click.option("--name", required=True, type=str)
@click.option("--description", required=False, type=str, default=None)
@click.argument("resource-id", required=True)
def clone(resource_id, name, description):
    new_config = clone_model_building_config(resource_id, name=name, description=description)
    click.echo(
        "Cloned ModelBuildinConfig:\n"
        f"id : {new_config.get_id()}\n"
        f"url: {new_config.get_url()}"
    )


@model_building_config.command
@click.argument("resource-id", required=True)
@click.option("--distribution", "-d", type=str, multiple=True)
def update(resource_id):
    updated_config = update_model_building_config(distributions=distributions)
    click.echo(
        "Updated ModelBuildinConfig:\n"
        f"id : {new_config.get_id()}\n"
        f"url: {new_config.get_url()}"
    )

