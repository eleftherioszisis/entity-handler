from copy import deepcopy


def update_variant_version(config_dict, variant_version, variant_algorithm=None):
    """Update config distribution variant version.
    """
    config_dict = deepcopy(config_dict)
    _recursively_update_variant_definition(config_dict, variant_algorithm, variant_version)
    return config_dict


def _recursively_update_variant_definition(data, algorithm, version):

    for key, value in data.items():
        if "variantDefinition" in value:
            if not algorithm or value["variantDefinition"]["algorithm"] == algorithm:
                value["variantDefinition"]["version"] = version
        elif isinstance(key, dict):
            _recursively_update_variant_definition(value, algorithm, version)


    


