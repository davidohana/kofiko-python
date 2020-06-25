import json

import examples.config.customizations
import kofiko
from examples.config.database_config import DatabaseConfig
from examples.config.general_config import GeneralConfig


def print_class(cls, desc):
    print("{} ({}):\n{}".format(cls.__name__, desc, json.dumps(kofiko.get_section_as_dict(cls), indent=2)))


def main():
    print_class(DatabaseConfig, "default")
    print_class(GeneralConfig, "default")

    # explicitly register a customization without a decorator
    kofiko.register_customization(examples.config.customizations.dev)
    kofiko.configure(customization_name="dev")

    print_class(DatabaseConfig, "configured")
    print_class(GeneralConfig, "configured")


if __name__ == '__main__':
    main()
