## kofiko - Code-First Configuration approach for Python 

### Overview

*kofiko* = (Ko)de-(Fi)rst (Ko)nfiguration

![](docs/kofiko-python.png)

Define application configuration as Python classes:

```python
@config_section
class GeneralConfig:
    env = "default"
    port = 8001
    weights = [1.1, 2.2]
    bool_to_str = {
        True: "Yes",
        False: "No"
    }
```

Override default values from either (or both):
1. Customization functions
   ```python
    @config_custom
    def prod():
        GeneralConfig.env = "prod"
        GeneralConfig.port = 8080
    ```

1. `.INI` files:
    ```ini
    [GENERAL]
    bool_to_str = No:Nyet
    WEIGHTS = 3,4,5.1
    ```

1. Environment variables:  
   ```
   myapp_GENERAL_ENV=prod 
   myapp_general_bool_to_str=True:si
   ```

Call `configure()` to activate:
```python
kofiko.configure()
```

And use static members of configured classes directly from your code.
```python
print(GeneralConfig.env)            # prod
print(GeneralConfig.bool_to_str)    # {True: 'Si', False: 'Nyet'}
```

No external dependencies. 

### How Kofiko works:

* Configuration should be defined as classes with static attributes. 
  Each class is considered as a configuration **section**, each class is a configuration 
  **option**.
* Once `kofiko.configure()` is called, kofiko will override the default values defined
  for each attribute from values in the following order: (1) registered customization functions
  (2) provided `.INI` files (3) env. vars (the first override found takes place)
* Kofiko will automatically derive the type of configuration options from their default values. 
  This also works for lists and dicts.
* Kofiko supports the following types: `string`, `int`, `float`, `bool`, `list`, `dict`.   
* Lookup for configuration in env. vars is expecting the following format by default: 
  `prefix_section_option` (prefix can be omitted).
* Lookup for configuration in ini files and env. vars is NOT case sensitive by default.  
* Configuration classes can reside everywhere in your code. They should be registered 
  using the `@config_section` decorator or explicitly with a call to `kofiko.register_section()`
* If you use decorators, you should make sure that the modules that contain configuration classes and customization functions are loaded, before the call to `kofiko.configure()`. 
  You can do that by performing `import` on those modules or calling `kofiko.register_module()`.
* You can modify values in `kofiko.Settings` before `configure()` to control Kofiko's 
  behavior, e.g. env. var lookup prefix; lookup case-sensitivity; whether dicts should be appended or replaced; separators for parsing lists and dicts and more.
* Specific terms like "Config", "Settings", can be omitted from the names of sections when overriding those in .ini or env. vars. For example: `DatabaseConfig.port` attribute 
  can be overridden from `database_port` env var.
* `kofiko.configure()` returns a dict of all values modified by overrides. Might be useful to log this.

### to-do:

* Packaging to pip
* Command-Line arguments layer
  
### License: 
Apache-2.0

### Contributing 

Our project welcomes external contributions. Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for further details.
