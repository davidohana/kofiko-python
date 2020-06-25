import json

import examples.config.customizations
import kofiko
from examples.config.database_config import DatabaseConfig
from examples.config.general_config import GeneralConfig


def print_obj(desc, obj):
    print("{}:\n{}\n".format(desc, json.dumps(obj, indent=2)))


def main():
    # explicitly register a customization without a decorator
    kofiko.register_customization(examples.config.customizations.dev)

    print_obj("Default", kofiko.get_all_configuration(False))

    overrides = kofiko.configure(customization_name="dev")

    print_obj("Overrides", overrides)
    print_obj("Configured", kofiko.get_all_configuration(True))


if __name__ == '__main__':
    main()
