import configparser
import os
import typing

from kofiko.settings import Settings


class ConfigObject:
    """
    Holds a registered section (class) or customization (function)
    """

    def __init__(self, obj, name=""):
        self.obj = obj
        if not name:
            name = obj.__name__
        self.name = name


"""
Registered config sections. Each section is represented by a Python Class where config options are represented by
the static attributes of that class.
"""
config_sections: typing.List[ConfigObject] = []

"""
Registered config customizations. Each customization is a function that overrides default values of the various config 
sections.
"""
config_customizations: typing.List[ConfigObject] = []


def get_first_env_value(keys: list):
    vals = map(lambda key: os.getenv(key), keys)
    for val in vals:
        if val is not None:
            return val
    return None


def get_first_ini_value(section_lookups: list, option_lookups: list, config_parser: configparser.ConfigParser):
    for opt in option_lookups:
        for sec in section_lookups:
            val = config_parser.get(sec, opt, fallback=None)
            if val is not None:
                return val
    return None


def convert_to_boolean(value):
    if value.lower() not in configparser.ConfigParser.BOOLEAN_STATES:
        raise ValueError('Not a boolean: %s' % value)
    return configparser.ConfigParser.BOOLEAN_STATES[value.lower()]


def convert_to_list(value: str, orig_list: list):
    str_elements = value.split(Settings.list_separator)
    if len(orig_list) == 0:
        return str_elements
    first_elem = orig_list[0]
    typed_elements = [text_to_typed_value(str_element, first_elem, True) for str_element in str_elements]
    return typed_elements


def convert_to_dict(value: str, orig_dict: dict):
    pairs = value.split(Settings.list_separator)
    list_of_key_val = [p.split(Settings.key_val_separator, maxsplit=2) for p in pairs]
    list_of_tuples = []
    for key_val in list_of_key_val:
        if len(key_val) == 1:
            raise ValueError("Invalid key/value pair: " + str(key_val))
        list_of_tuples.append((key_val[0], key_val[1]))

    if len(orig_dict) == 0:
        return dict(list_of_tuples)

    first_orig_key = next(iter(orig_dict.keys()))
    first_orig_val = next(iter(orig_dict.values()))
    list_of_typed_tuples = []
    for str_key, str_val in list_of_tuples:
        typed_key = text_to_typed_value(str_key, first_orig_key, True)
        typed_val = text_to_typed_value(str_val, first_orig_val, True)
        list_of_typed_tuples.append((typed_key, typed_val))

    if not Settings.append_to_dicts:
        return dict(list_of_typed_tuples)

    for t in list_of_typed_tuples:
        orig_dict[t[0]] = t[1]
    return orig_dict


def text_to_typed_value(text_value: str, orig_value, fallback_to_str=True):
    if isinstance(orig_value, str):
        return text_value
    if orig_value is None:
        return text_value
    if isinstance(orig_value, bool):
        return convert_to_boolean(text_value)
    if isinstance(orig_value, int):
        return int(text_value)
    if isinstance(orig_value, float):
        return float(text_value)
    if isinstance(orig_value, list):
        return convert_to_list(text_value, orig_value)
    if isinstance(orig_value, dict):
        return convert_to_dict(text_value, orig_value)

    if fallback_to_str:
        return text_value
    return None


def set_attr_from_text(cls, attr_name: str, str_value: str):
    attr_value = getattr(cls, attr_name)
    typed_value = text_to_typed_value(str_value, attr_value)
    if typed_value is not None:
        setattr(cls, attr_name, typed_value)
        return typed_value


def get_env_key(section: str, option: str):
    tokens = []
    if Settings.env_prefix:
        tokens.append(Settings.env_prefix)
    tokens.append(section)
    tokens.append(option)
    return Settings.env_section_option_separator.join(tokens)


def get_case_lookups(term: str):
    lookups = []
    if Settings.case_mapping_allow_original:
        lookups.append(term)
    if Settings.case_mapping_allow_upper:
        lookups.append(term.upper())
    if Settings.case_mapping_allow_lower:
        lookups.append(term.lower())

    return lookups


def get_ini_lookup_options(section: str, option: str):
    section_lookups = []
    section_lookups.extend(get_case_lookups(section))

    section_without_tokens = section
    for token in Settings.section_lookup_delete_tokens:
        section_without_tokens = section_without_tokens.replace(token, "")
    if section_without_tokens != section:
        section_lookups.extend(get_case_lookups(section_without_tokens))

    option_lookups = []
    option_lookups.extend(get_case_lookups(option))

    return section_lookups, option_lookups


def get_env_key_lookup_options(section: str, option: str):
    section_lookups, option_lookups = get_ini_lookup_options(section, option)
    env_key_lookups = []
    for section_lookup in section_lookups:
        for option_lookup in option_lookups:
            env_key_lookups.append(get_env_key(section_lookup, option_lookup))

    return env_key_lookups
