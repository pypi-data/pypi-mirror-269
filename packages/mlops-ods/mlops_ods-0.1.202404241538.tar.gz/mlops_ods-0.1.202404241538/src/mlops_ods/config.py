import yaml
from pkg_resources import resource_filename


def load_config_yaml():
    """
    Load config from yaml file

    :return: dict config
    """
    with open(resource_filename(__name__, "config.yaml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
