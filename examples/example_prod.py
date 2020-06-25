import json

import kofiko
from examples.config.database_config import DatabaseConfig
from examples.config.general_config import GeneralConfig


def print_class(cls, desc):
    print("{} ({}):\n{}".format(cls.__name__, desc, json.dumps(kofiko.get_section_as_dict(cls), indent=2)))


def main():
    print_class(DatabaseConfig, "default")
    print_class(GeneralConfig, "default")

    # all decorated customizations inside this module will be registered
    kofiko.configure(customization_name="prod", ini_file_names="../cfg/prod.ini")

    print_class(DatabaseConfig, "configured")
    print_class(GeneralConfig, "configured")


if __name__ == '__main__':
    main()
