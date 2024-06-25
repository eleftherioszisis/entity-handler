import click
import tempfile
from pathlib import Path

from entity_management.util import get_entity
from cwl_registry.variant import Variant
from cwl_registry.utils import write_yaml

from .update_variant_distribution import update_variant_version

@click.group
def variant():
    pass


@variant.command
@click.argument("resource-id", required=True)
@click.option("--environment", "-e", multiple=True, required=False, default=None)
@click.option("--generator-name", required=False, default=None)
@click.option("--variant-name", required=False, default=None)
@click.option("--version", required=False, default=None)
def clone(resource_id, environment, generator_name, variant_name, version):

    variant = get_entity(resource_id, cls=Variant)
    distribution_dict = variant.get_content()

    if environment:

        new_environment = {}
        for env in environment:
            key, value = env.split(":", 1)

            if key == "modules":
                value = value.split(",")
            new_environment[key] = value

        new_environment["enable-internet"] = True

        distribution_dict["environment"] = new_environment

    with tempfile.TemporaryDirectory() as tdir:

        definition_file = Path(tdir, "definition.cwl")
        write_yaml(data=distribution_dict, filepath=definition_file)

        new_variant = Variant.from_file(
            filepath=definition_file,
            generator_name=generator_name or variant.generator_name,
            variant_name=variant_name or variant.variant_name,
            version=version or variant.version,
        )
        new_variant = new_variant.publish(update=False)

        click.echo(
            f"Cloned {variant.get_id()} -> {new_variant.get_id()}"
            f"With data:\n{new_variant.overview}"
        )


@variant.command
@click.argument("resource-id", required=True)
@click.option("--environment", "-e", multiple=True, required=False, default=None)
@click.option("--generator-name", required=False, default=None)
@click.option("--variant-name", required=False, default=None)
@click.option("--version", required=False, default=None)
def update(resource_id, environment, generator_name, variant_name, version):
    variant = get_entity(resource_id, cls=Variant)
    distribution_dict = variant.get_content()

    if environment:

        new_environment = {}
        for env in environment:
            key, value = env.split(":", 1)

            if key == "modules":
                value = value.split(",")
            new_environment[key] = value

        new_environment["enable-internet"] = True

        distribution_dict["environment"] = new_environment

    with tempfile.TemporaryDirectory() as tdir:

        definition_file = Path(tdir, "definition.cwl")
        write_yaml(data=distribution_dict, filepath=definition_file)

        new_variant = variant.evolve(
            path=definition_file,
            generator_name=generator_name or variant.generator_name,
            variant_name=variant_name or variant.variant_name,
            version=version or variant.version,
        )
        new_variant = new_variant.publish(update=True)

        click.echo(
            f"Updated {variant.get_id()} with data:\n" + new_variant.overview
        )

'''
@update.command("variant-version")
@click.option("--sub-config-name", "-c", multiple=True)
@click.option("--version", "-v", required=False)
@click.argument("resource-id", required=True)
def variant_version(resource_id, sub_config_name, version):

    model_config = get_entity(resource_id, cls=ModelBuildingConfig)
    sub_configs = [getattr(model_config.configs, name) for name in sub_config_name]

    for sub_config in sub_configs:

        sub_config_dict = sub_config.distribution.as_dict()

        new_sub_config_dict = update_variant_version(
            sub_config_dict, variant_algorithm=None, variant_version=version
        )
        distribution = DataDownload.from_json_str(json.dumps(new_sub_config_dict))
        new_sub_config = sub_config.evolve(distribution=distribution)
        new_sub_config.publish()
        click.echo(
            f"ModelBuildingConfig {model_config.get_id()}:\n"
            f"Updated sub-config {sub_config_name} with id {sub_config.get_id()}"
        )
'''
