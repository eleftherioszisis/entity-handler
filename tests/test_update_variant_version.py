from copy import deepcopy
from model_building_config import update_variant_distribution as test_module


def test_update_variant_version__cell_composition(cell_composition_config_distribution_dict):

    res = test_module.update_variant_version(cell_composition_config_distribution_dict, "v1-tst")

    res_version = res['http://api.brain-map.org/api/v2/data/Structure/997']["variantDefinition"]["version"]
    assert res_version == "v1-tst"
