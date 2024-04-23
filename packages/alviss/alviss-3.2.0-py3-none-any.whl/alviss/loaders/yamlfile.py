__all__ = [
    'YamlFileConfigLoader',
]

from .base import *
import yaml

import logging
log = logging.getLogger(__name__)


class YamlFileConfigLoader(BaseLoader):
    def load_raw(self, raw_data: str, no_resolve: bool = False,
                 no_extend: bool = False, no_includes: bool = False, no_env_load: bool = False,
                 no_fidelius: bool = False):
        self._data = self._load_dict(yaml.safe_load(raw_data))
        self._set_chains()
        if not no_extend:
            self._extend()
        if not no_includes:
            self._includes()
        if not no_resolve:
            self._resolve()
        if not no_fidelius:
            self._fetch_fidelius()

    @property
    def rendered(self) -> str:
        return yaml.dump(self._data)
