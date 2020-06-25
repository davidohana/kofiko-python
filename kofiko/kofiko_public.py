"""
(Ko)de (Fi)rst (Ko)nfiguration
A configuration package with code-first approach for Python.
Copyright (C) 2020 David Ohana @ ibm.com
"""

import importlib
import inspect
import pkgutil

from kofiko.kofiko_internals import *


def config_section(section_name: str = ""):
    """
    Mark a class as a config section. Class will be registered once the containing module is executed.

    :param section_name:
    :return:
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
    config_sections.append(ConfigObject(cls, name))


def register_customization(func, name=""):
    config_customizations.append(ConfigObject(func, name))


def register_module(module, recursive=False):
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
    attr_dict = {}
    for name, val in cls.__dict__.items():
        if name.startswith("__"):
            continue
        if callable(val):
            continue
        attr_dict[name] = val
    return attr_dict


def configure(customization_name=None,
              ini_file_names="",
              env_key_mapper=get_env_key_lookup_options,
              ini_key_mapper=get_ini_lookup_options):
    config_parser = configparser.ConfigParser()

    for customization in config_customizations:
        if customization.name == customization_name:
            customization.obj()

    if ini_file_names:
        config_parser.read(ini_file_names)

    for section in config_sections:
        config_class = section.obj
        section_name = section.name
        options = get_section_as_dict(config_class).keys()

        for option_name in options:
            if Settings.env_override_enabled:
                env_key_lookups = env_key_mapper(section_name, option_name)
                env_val = get_first_env_value(env_key_lookups)
                if env_val:
                    set_attr_from_text(config_class, option_name, env_val)
                    continue

            section_lookups, option_lookups = ini_key_mapper(section_name, option_name)
            ini_val = get_first_ini_value(section_lookups, option_lookups, config_parser)
            if ini_val:
                set_attr_from_text(config_class, option_name, ini_val)
