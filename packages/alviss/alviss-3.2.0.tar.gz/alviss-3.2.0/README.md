# Alviss the all-knowing

Generic Configuration file reader/parser with a bunch of nifty extra 
features, most notably:

- 

JSON & YAML Configuration file reader/parser with built-in fault tolerance and
 ENV variable injecting, structure inheritance, internal referencing and 
secret injection.

## 2.6 Features

* Enabled automatic `fidelius` integration (see: https://gitlab.ccptools.cc/packages/fidelius)


## 2.1 Features

* JSON & YAML config file reading
    * Files can extend base file for easy overriding and customization
    * Files can include multiple other files for better organization and
    structure.
    * Includes/extends can be in a nested structure
* Simple yet powerful internal variable reference parsing
    * Inject values from elsewhere in the config files anywhere
    * Automatic injection of environment variables for values
* Nested fault tolerant fetching of non-existing values
* Quickly nest keys into one with dots
* Easy default value usage
* Password and secret masking
* One line config loading
* ~~Singleton config model~~
* ~~Extendable for multiple singleton configs~~
    * Removed from the basic class in 2.0. Singleton functionality can be
    added by simply extending the `alviss.structs.BaseConfig` on the
    application level and adding the `typeutils.metas.Singleton` as a
    `metaclass`
    * The `alviss.structs.SingletonConfig` sill behaves as the old singleton
    base guy did if people want.


### Singleton reloading/update/set

Reloading (or loading, setting or updating different values) anywhere in code will change them 
globally wherever the same model is referenced.

**Update in one place...**
```python
# Somewhere in the program we decide that reloading the config is in order
from alviss.structs import SingletonConfig

cfg = SingletonConfig()
cfg.load(foo='Foo Too You!', bar='Salad bar vs. Tequila bar!')

# This will be the same config
cfg2 = SingletonConfig()
assert cfg == cfg2
```

**Updated everywhere...**
```python
# Anywhere the config is needed...
from alviss.structs import SingletonConfig

cfg = SingletonConfig()
assert cfg.foo == 'What is a Foo anyway?'
```

## Updating methods

### Loading/Reloading

Calling `BaseConfig.load(**kwargs)` will clear the entire config data map and 
load up the new values given.

```python
from alviss.structs import BaseConfig

# Initial values...
cfg = BaseConfig()
cfg.load(foo='Foo Too You!', bar='Salad bar vs. Tequila bar!')

assert cfg.foo == 'Foo Too You!'
assert cfg.bar == 'Salad bar vs. Tequila bar!'

# ...now we reload...
cfg.load(foo='Foo is not a real word!')

# ...so now there is no `bar` in the config
assert cfg.foo == 'What is a Foo anyway?'
assert not cfg.bar
```

Giving the `BaseConfig` constructor `**kwargs` does the same as calling 
`BaseConfig.load(**kwargs)` and will therefor clear and reload the config values
from the supplied keyword arguments.

```python
from alviss.structs import BaseConfig

# Initial values...
cfg = BaseConfig()
cfg.load(foo='Foo Too You!', bar='Salad bar vs. Tequila bar!')

# This does the same thing
cfg = BaseConfig(foo='Foo Too You!', bar='Salad bar vs. Tequila bar!')
```

### Setting values directly

```python
from alviss.structs import BaseConfig

# Initial values...
cfg = BaseConfig()
cfg.load(foo='Foo Too You!', bar='Salad bar vs. Tequila bar!')

# Updated only the `foo` value, but on a singleton level so it changes everywhere
cfg.foo = 'Nyoo Foo!'
```

### Updating the config

Calling `update(**kwargs)` will update only the given keyword values of the 
config (globally via singleton magic as before) but preserves the existing 
values of the config that did not change (while `load(**kwargs)` wiped the 
config clean first).

```python
from alviss.structs import BaseConfig

# Initial values...
cfg = BaseConfig()
cfg.load(foo='Foo Too You!', bar='Salad bar vs. Tequila bar!')

# Updated only the given values (leaving `bar` unchanged)
cfg.update(foo='Nyoo Foo!', moo='Shoo!')
```

## Extendable for multiple singleton configs or other magic

You can use the `alviss.structs.SingletonConfig` as a base for implementing
 other 
config classes in order to store different singleton instances of different 
configs.

The singleton mechanism supports inheritance so the new Classes will have their 
own singleton instances separate from each other and from `SingletonConfig`.

```python
from alviss.structs import SingletonConfig


class ClientConfig(SingletonConfig):
    pass


class ServerConfig(SingletonConfig):
    pass


client_cfg = ClientConfig(host='localhost')

server_cfg = ServerConfig(host='127.0.0.1')

assert client_cfg != server_cfg
```

## Quick JSON/YAML Config File Loading

User the `alviss.quickloader` to load a `BaseConfig` from the given JSON or
YAML file.

**The `config.json` file...**
```json
{
    "foo": "Foo Too You!",
    "bar": "Salad bar vs. Tequila bar!"
}
```

**Loading from `config.json`...**
```python
from alviss import quickloader

cfg = quickloader.autoload('config.json')

assert cfg.foo == 'Foo Too You!'
```

## Config file extending/including example

Alviss now supports extending base config files and including files via the
 `__extends__` and `__include__` config keys respectively.

### Extending a base file

Using the `__extends__` key you can embed one or more additional config files
wholesale into another. This works from within the nested key hierarchy so
extended files within nested keys/sections will inject the values there.

Values of keys duplicated in both the current file and the extended files
defined in `__extends__` will retain the value from the current file _(i.e. the
current values override those from the extended base files)_.

The `__extends__` key can take either a single string file name or a list of
files.


**The `base.json` file...**
```json
{
    "foo": "Foo Too You!",
    "bar": {
        "first": "Beer",
        "second": "Wine"
    }
}
```

**The `production.json` file...**
```json
{
    "__extends__": "base.json",
    "bar": {
        "second": "Tequila"
    }
}
```

**Loading `base.json` and overriding with `production.json`...**
```python
from alviss import quickloader

# Assume this comes from an environment variable for example
CONFIG_FILE = 'production.json'

# Loading the base config...
cfg = quickloader.autoload(CONFIG_FILE)

assert cfg.foo == 'Foo Too You!'
assert cfg.bar.first == 'Beer'
assert cfg.bar.second == 'Tequila'
```

### Including additional files

Using the `__include__` key you can embed one or more additional config files
wholesale into another. This works from within the nested key hierarchy so
including files within nested keys/sections will inject the values there.

Values of keys duplicated in both the current file and the included files
defined in `__include__` will retain the value from the last included file 
_(i.e. the included values override those from the current one)_.

The `__include__` key can take either a single string file name or a list of
files.

**The `logging.yaml` file...**
```yaml
level: INFO
file: stuff.log
```

**The `db.yaml` file...**
```yaml
database:
  driver: mysql
  name: mydata
```

**The `extra.yaml` file...**
```yaml
bar: Foo
```

**The `app.yaml` file...**
```yaml
foo: Bar
logging:
  # Default level is DEBUG
  level: DEBUG
  __include__: logging.yaml

bar: NotFoo
__include__: 
- db.yaml
- extra.yaml
```

**Loading `app.yaml`...**
```python
from alviss import quickloader

# Loading the config...
cfg = quickloader.autoload('app.yaml')

assert cfg.foo == 'Bar'
assert cfg.logging.level == 'INFO'
assert cfg.database.driver == 'mysql'
assert cfg.bar == 'Foo'
```

## Quickly reference a nested key with a single key string

You can reference a nested key (e.g. for overriding in an include/extension
) by using dots to separate keys in the path.

**The `config.json` file...**
```json
{
  "database": {
    "settings": {
      "connection": {
        "host": "1.2.3.4",
        "port": 1234      
      }   
    }    
  }
}
```

**The `local.json` file...**
```json
{
  "__extends__": "config.json",
  "database.settings.connection.host": "localhost"
}
```

**Loading `local.json`...**
```python
from alviss import quickloader

# Loading the config...
cfg = quickloader.autoload('local.json')

assert cfg.database.settings.connection.host == 'localhost'
```


## Internal variable referencing

You can reference other config value keys from within any values by using 
`${some.other.key}` from any string value, using dots to navigate key nestings.

**The `config.json` file...**
```json
{
  "basics": {
    "env": "prod"
  },
  "db": {
    "name": "my-data-${basics.env}"    
  }
}
```

**Loading `config.json`...**
```python
from alviss import quickloader

# Loading the config...
cfg = quickloader.autoload('config.json')

assert cfg.db.name == 'my-data-prod'
```

## Automatic injection of environment variables for values

You can automatically inject any environment variables set on the system by
using `${__ENV__:SOME_ENV_VAR}` from within any string value.

**The `config.yaml` file...**
```yaml
user: Foo
password: ${__ENV__:MY_PASS}
```

**Loading from `config.yaml`...**
```python
import os

os.environ.update('MY_PASS', 'SuperSecret!')

from alviss import quickloader

# Loading the config...
cfg = quickloader.autoload('config.yaml')

assert cfg.password == 'SuperSecret!'
```

## Nested fault tolerant fetching of non-existing values

Alviss config models will return an `Empty` and/or `EmptyDict`) from 
`typeutils` if asked for a value that was not in the config file read.

This means that you will never get a `KeyError` or other such exceptions when 
looking up config values, even if search multiple nested levels.

```python
from alviss.structs import *

# Load config...
cfg = BaseConfig(foo={'alpha': 42})

assert cfg.foo.alpha == 42
assert not cfg.foo.beta
assert not cfg.bar
assert not cfg.bar.alpha
assert not cfg.a.b.c.d.e.f
```

To check explicitly if a value has not been set (vs. it's value just being an 
empty string for example) you can check if the value `is typeutils.empty.Empty`

```python
from alviss.structs import *  # Includes a reference to `typeutils.empty.Empty`

# Load config...
cfg = BaseConfig(foo={'alpha': 42})

assert cfg.foo.alpha == 42
assert cfg.foo.beta is Empty
assert cfg.bar is Empty
```

## Easy default value usage 

`Empty` object evaluate as `False` in boolean comparisons so you can ensure 
default values with an `or` bitwise operator.

```python
from alviss.structs import *

# Load config...
cfg = BaseConfig(foo='Foo Too You!')

# Get value or default
my_bar = cfg.bar or 'There was no bar'

assert my_bar == 'There was no bar'
```
