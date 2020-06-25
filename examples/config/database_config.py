from kofiko import config_section, config_custom


@config_section
class DatabaseConfig:
    user = "admin"
    password = "changeme"
    endpoints = []
    port = 8001
    db_name = "default"
    query_filter = None
    db_size_limits = {
        "alerts": 50,
        "logs": 500
    }

