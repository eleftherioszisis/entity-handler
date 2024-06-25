import json
import click
import logging
import tempfile
from pathlib import Path

from entity_management import config
from entity_management.util import get_entity
from entity_management.core import DataDownload
from cwl_registry.variant import Variant
from cwl_registry.utils import write_yaml

from entity_handler.entities.variant.cli import variant
from entity_handler.entities.model_building_config.cli import model_building_config, cell_composition_config


@click.group("entity-handler")
@click.option(
    "-v", "--verbose", count=True, default=1, help="-v for INFO, -vv for DEBUG"
)
def app(verbose):
    """CWL Registry execution tools."""

    level = (logging.WARNING, logging.INFO, logging.DEBUG)[min(verbose, 2)]

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


app.add_command(name="Variant", cmd=variant)
app.add_command(name="ModelBuildingConfig", cmd=model_building_config)
app.add_command(name="CellCompositionConfig", cmd=cell_composition_config)
