from kofiko import config_section


@config_section
class GeneralConfig:
    weights = [1.1, 2.2]
    bool_to_str = {
        True: "Yes",
        False: "No"
    }
