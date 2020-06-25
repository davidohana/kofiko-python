class Settings:
    """
    Modify those settings before calling configure() to tweak kofiko's behavior.
    """

    """
    Whether to allow overriding configuration values from environment variables.
    """
    env_override_enabled = True

    """
    The prefix to use when looking up for configuration in environment. Lookup format will 
    be `prefix_section_option` or `section_option` if prefix is empty. 
    """
    env_prefix = ""

    """
    Section-to-option separator for env-var lookup
    """
    env_section_option_separator = "_"

    """
    Separator between list items when parsing text values into typed lists.
    """
    list_separator = ","

    """
    Separator between key and value when parsing text values into typed dicts.
    """
    key_val_separator = ":"

    """
    Whether to create a new dict or add/overwrite config values in default dict.
    """
    append_to_dicts = True

    """
    Keywords to omit when looking up section names in ini/env
    """
    section_lookup_delete_tokens = ["Config", "Settings", "Cfg"]

    """
    Allow lookup of upper-cased section names in ini/env.
    """
    case_mapping_allow_upper = True

    """
    Allow lookup of lower-cased section names in ini/env.
    """
    case_mapping_allow_lower = True

    """
    Allow lookup of exact-case section names in ini/env.
    """
    case_mapping_allow_original = True
