import json

import kofiko


def print_obj(desc, obj):
    print("{}:\n{}\n".format(desc, json.dumps(obj, indent=2)))


# noinspection PyUnresolvedReferences
def main():
    # make sure config classes are loaded and registered before configure()
    import examples.config.database_config
    import examples.config.general_config

    print_obj("Default", kofiko.get_all_configuration(False))

    overrides = kofiko.configure(ini_file_names="../cfg/prod.ini")

    print_obj("Overrides", overrides)
    print_obj("Configured", kofiko.get_all_configuration(True))


if __name__ == '__main__':
    main()
