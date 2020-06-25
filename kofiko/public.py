"""
(Ko)de (Fi)rst (Ko)nfiguration
A configuration package with code-first approach for Python.
Copyright (C) 2020 David Ohana @ ibm.com
License: Apache-2.0
"""
import copy
import importlib
import inspect
import pkgutil

from kofiko.internal import *


def config_section(section_name: str = ""):
    """
    Mark a class as a config section. Class will be registered once the containing module is executed.
    Make sure module with decorated class is loaded by importing it before calling :func:`kofiko.configure`.

    :param section_name: name of the section that will be used for lookups in ini/env. Class name is used when empty.
    """
    # allow decorators without arguments, first arg is the class
    if inspect.isclass(section_name):
        cls = section_name
        config_sections.append(ConfigObject(cls))
        return cls

    # decorator with argument
    def inner_decorator(_cls):
        config_sections.append(ConfigObject(_cls, section_name))
        return _cls

    return inner_decorator


def config_custom(customization_name=""):
    """
    Mark a function as a customization. Function will be registered once the containing module is executed.
    Customization function is called if :func:`kofiko.configure` is called with the same customization name.
    Multiple functions can be registered for the same customization name (they all will be executed)
    Make sure module with decorated class is loaded by importing it before calling :func:`kofiko.configure`.

    :param customization_name: name of the customization. Function name is used when empty.
    """
    # allow decorators without arguments, first arg is the function
    if callable(customization_name):
        func = customization_name
        config_customizations.append(ConfigObject(func))
        return func

    def inner_decorator(_func):
        config_customizations.append(ConfigObject(_func, customization_name))
        return _func

    return inner_decorator


def register_section(cls, name=""):
    """
    Explicitly register a configuration class as a section if you are unable to use `config_section` decorator.
    """
    config_sections.append(ConfigObject(cls, name))


def register_customization(func, name=""):
    """
    Explicitly register a customization function if you are unable to use `config_custom` decorator.
    """
    config_customizations.append(ConfigObject(func, name))


def register_module(module, recursive=False):
    """
    Ensure module is loaded, so that decorators inside that module are activated.
    :param module:
    :param recursive: load also sub-modules.
    """
    if not recursive:
        # do nothing, thus function just makes sure that the module is loaded
        # before init() is called, to force registration of inner config objects
        return

    package_name = module.__name__
    return {
        name: importlib.import_module(package_name + '.' + name)
        for loader, name, is_pkg in pkgutil.walk_packages(module.__path__)
    }


def get_section_as_dict(cls):
    """
    Convert public static attributes of the called class into kay-value elements in a dictionary.
    """
    attr_dict = {}
    for name, val in cls.__dict__.items():
        if name.startswith("__"):
            continue
        if callable(val):
            continue
        attr_dict[name] = val
    return attr_dict


def get_all_configuration(flat=False):
    """
    returns a dictionary of all known configuration options and their values
    :param flat: wheter to return 1-level dictionary in the format option.section=value, or 2-level dictionary.
    """
    all_config = {}
    for section in config_sections:
        config_class = section.obj
        options = get_section_as_dict(config_class)
        if not flat:
            all_config[section.name] = copy.deepcopy(options)
            continue
        for option_name, option_val in options.items():
            all_config[section.name + "." + option_name] = option_val

    return all_config


def configure(customization_name=None,
              ini_file_names="",
              env_key_mapper=get_env_key_lookup_options,
              ini_key_mapper=get_ini_lookup_options):
    """
    Override default values of static attributes in registered configuration classes (sections).
    Override Order: customization function -> ini file -> env. var (first match wins)

    :param customization_name: All registered customization functions with the specified name will be executed (optional)
    :param ini_file_names: A single .ini filename or a list of file-names (optional)
    :param env_key_mapper: Function with strategy to lookup overrides in environment vars.
    Returns a list of lookup env-var key. Change if you wish to use a custom strategy.
    :param ini_key_mapper: Function with strategy to lookup overrides in ini files.
    Returns two lists of lookup sections and lookup options.

    :returns all options which were modified from their default value, in a dict of dict format.
    """
    config_parser = configparser.ConfigParser()

    default_config = get_all_configuration()

    for customization in config_customizations:
        if customization.name == customization_name:
            customization.obj()

    if ini_file_names:
        config_parser.read(ini_file_names)

    for section_name in config_sections:
        config_class = section_name.obj
        section_name = section_name.name
        options = get_section_as_dict(config_class).keys()

        for option_name in options:

            def perform_override():
                if Settings.env_override_enabled:
                    env_key_lookups = env_key_mapper(section_name, option_name)
                    env_val = get_first_env_value(env_key_lookups)
                    if env_val:
                        return set_attr_from_text(config_class, option_name, env_val)

                if len(ini_file_names) > 0:
                    section_lookups, option_lookups = ini_key_mapper(section_name, option_name)
                    ini_val = get_first_ini_value(section_lookups, option_lookups, config_parser)
                    if ini_val:
                        return set_attr_from_text(config_class, option_name, ini_val)

                return None

            perform_override()

    overrides = get_all_configuration()
    for section_name, option_dict in default_config.items():
        for option_name, option_val in option_dict.items():
            if overrides[section_name][option_name] == default_config[section_name][option_name]:
                del overrides[section_name][option_name]
        if len(overrides[section_name]) == 0:
            del overrides[section_name]

    return overrides
