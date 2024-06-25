import click
import json
import logging
import tempfile
from pathlib import Path

from entity_management.util import get_entity
from entity_management.config import CellCompositionConfig
from entity_management.core import DataDownload

L = logging.getLogger(__name__)


ROOT_KEY = "http://api.brain-map.org/api/v2/data/Structure/997"


@click.group
def cell_composition_config():
    pass


@cell_composition_config.command
@click.option("--new-id", required=True)
@click.argument("resource-id", required=True)
def update_base_cell_composition_id(resource_id, new_id):

    config = get_entity(resource_id, cls=CellCompositionConfig)

    with tempfile.TemporaryDirectory() as tdir:

        filepath = Path(config.distribution.download(path=tdir))

        data = json.loads(filepath.read_bytes())
        data[ROOT_KEY]["inputs"][0]["id"] = new_id

        filepath.write_text(json.dumps(data, indent=2))

        new_distribution = DataDownload.from_file(filepath) 

        config = config.evolve(distribution=new_distribution)
        config.publish()

        click.echo(
            click.style(
                f"CellCompositionConfig {resource_id} base_cell_composition updated to {new_id}",
                fg="green",
            )
        )
