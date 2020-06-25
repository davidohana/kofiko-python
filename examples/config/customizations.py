from examples.config.database_config import DatabaseConfig
from examples.config.general_config import GeneralConfig
from kofiko import config_custom


# use decorator without argument will register customization with func name
@config_custom
def prod():
    DatabaseConfig.port = 8003
    DatabaseConfig.user = "prod_user"
    DatabaseConfig.db_name = "db_prod"
    DatabaseConfig.db_size_limits["logs"] = 120


@config_custom("staging")
def customization_staging():
    DatabaseConfig.port = 8002
    DatabaseConfig.user = "stag_user"
    DatabaseConfig.db_name = "db_staging"
    DatabaseConfig.db_size_limits["logs"] = 100


# if you cannot add decorator, you should call kofiko.RegisterCustomization()
def dev():
    DatabaseConfig.port = 8004
    DatabaseConfig.user = "dev_user"
    DatabaseConfig.db_name = "db_dev"
    GeneralConfig.weights = [100]
