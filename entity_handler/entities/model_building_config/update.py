from entity_management.core import DataDownload

L = logging.getLogger(__name__)

def update_model_building_config(obj, distributions):

    if isinstance(obj, str):
        obj = get_entity(obj, cls=ModelBuildingConfig)

    for change_string, change in changes.items():

        config_name, config_path = change_string.split(":", 1)
        sub_config = getattr(obj.configs, config_name)
        new_sub_config = subconfig.evolve(distribution=_create_distribution(path))
        new_sub_config.publish()

        L.info(
            f"Updated {config_name} distribution:\n"
            f"from: {sub_config.distribution.contentUrl}\n"
            f"to  : {new_sub_config.distribution.contentUrl}\n"
        )


def _create_distribution(path):
    return DataDownload.from_file(
        file_like=str(path),
        name=Path(path).name,
        content_type="application/json"
    )
