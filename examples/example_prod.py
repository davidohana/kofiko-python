import json

import examples.config
import kofiko


def print_obj(desc, obj):
    print("{}:\n{}\n".format(desc, json.dumps(obj, indent=2)))


def main():
    # all decorated sections and customizations inside this module will be registered
    kofiko.register_module(examples.config, True)

    print_obj("Default", kofiko.get_all_configuration(False))

    overrides = kofiko.configure(customization_name="prod", ini_file_names="../cfg/prod.ini")

    print_obj("Overrides", overrides)
    print_obj("Configured", kofiko.get_all_configuration(True))


if __name__ == '__main__':
    main()
