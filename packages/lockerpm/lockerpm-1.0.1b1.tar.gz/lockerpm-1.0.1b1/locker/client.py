import copy
import logging
import os
import socket
from typing import Dict, Any

from locker.ls_resources import Secret, Environment


LOCKER_LOG = os.environ.get("LOCKER_LOG")


class Locker:
    DEFAULT_OPTIONS = {
        "access_key_id": None,
        "secret_access_key": None,
        "api_base": "https://api.locker.io/locker_secrets",
        "api_version": "v1",
        "proxy": None,
        "log": "error",
        "max_network_retries": 0,
        "skip_cli_lines": 0,
        "headers": {
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
        },
    }

    def __init__(
        self,
        access_key_id: str = None,
        secret_access_key: str = None,
        api_base: str = None,
        api_version: str = None,
        proxy: Any = None,
        log: str = None,
        max_network_retries: int = 0,
        resttime: int = 120,
        fetch: bool = False,
        options: Dict = None,
    ):
        # self.download_binary()
        if options is None:
            options = {}
        if api_base:
            options["api_base"] = api_base
        if api_version:
            options["api_version"] = api_version
        if proxy:
            options["proxy"] = proxy
        log = log or LOCKER_LOG
        if log:
            options["log"] = log
        assert resttime >= -1
        options["resttime"] = resttime
        options["fetch"] = fetch

        if max_network_retries:
            options["max_network_retries"] = max_network_retries
        if access_key_id:
            options["access_key_id"] = access_key_id
        if secret_access_key:
            options["secret_access_key"] = secret_access_key

        self._options: dict[str, Any] = copy.deepcopy(Locker.DEFAULT_OPTIONS)

        # Set Headers
        if "headers" in options:
            headers = copy.copy(options["headers"])
        else:
            headers = {}

        self._options.update(options)
        self._options["headers"].update(headers)

        # Set Logger
        logger = self._set_stream_logger(level=self._options.get('log'))
        self._options["logger"] = logger

        # Rip off trailing slash since all urls depend on that
        assert isinstance(self._options["api_base"], str)
        if self._options["api_base"].endswith("/"):
            self._options["api_base"] = self._options["api_base"][:-1]

        # if access_key_basic_auth:
        #     self._create_access_key_basic_auth(*access_key_basic_auth)

    # ---- This method is DEPRECATED from 0.1.1b1 ------------------- #
    # def _create_access_key_basic_auth(self, access_key_id: str, secret_access_key: str):
    #     self._options["access_key"] = f"{access_key_id}:{secret_access_key}"

    @property
    def access_key_id(self):
        return self._options.get("access_key_id")

    @access_key_id.setter
    def access_key_id(self, access_key_id_value):
        self._options.update({"access_key_id": access_key_id_value})

    @property
    def secret_access_key(self):
        return self._options.get("secret_access_key")

    @secret_access_key.setter
    def secret_access_key(self, secret_access_key_value):
        self._options.update({"secret_access_key": secret_access_key_value})

    @property
    def api_base(self):
        return str(self._options.get("api_base"))

    @api_base.setter
    def api_base(self, api_base_value):
        self._options.update({"api_base": api_base_value})

    @property
    def api_version(self):
        return str(self._options.get("api_version"))

    @property
    def log(self):
        return self._options.get("log")

    @log.setter
    def log(self, log_value):
        self._options.update({"log": log_value})
        logger = self._set_stream_logger(level=log_value)
        self._options["logger"] = logger

    @staticmethod
    def _set_stream_logger(level, name='locker'):
        assert level in ["debug", "info", "warning", "error"], "The log level is not valid"
        level = level.upper()
        format_string = '%(asctime)s {hostname} %(levelname)s %(message)s'.format(**{'hostname': socket.gethostname()})

        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @property
    def resttime(self):
        return self._options.get("resttime")

    @resttime.setter
    def resttime(self, resttime_value):
        self._options.update({"resttime": resttime_value})

    @property
    def fetch(self):
        return self._options.get("fetch")

    @fetch.setter
    def fetch(self, fetch_value):
        self._options.update({"fetch": fetch_value})

    @property
    def skip_cli_lines(self):
        return self._options.get("skip_cli_lines")

    @property
    def headers(self):
        return self._options.get("headers")

    @headers.setter
    def headers(self, custom_headers):
        self._options.update({"headers": custom_headers})

    @property
    def max_network_retries(self):
        return self._options.get("max_network_retries")

    def _translate_options(self, params):
        _params = copy.deepcopy(self._options)
        _params.update(params)
        return _params

    def list(self, **params):
        return Secret.list(**self._translate_options(params))

    def export(self, environment_name=None, output_format="dotenv",  **params):
        return Secret.export(
            environment_name=environment_name, output_format=output_format, **self._translate_options(params)
        )

    def get(self, key, environment_name=None, default_value=None, **params):
        return Secret.get_secret(
            key,
            environment_name=environment_name,
            default_value=default_value,
            **self._translate_options(params)
        )

    def get_secret(self, key, environment_name=None, default_value=None, **params):
        return Secret.get_secret(
            key,
            environment_name=environment_name,
            default_value=default_value,
            **self._translate_options(params)
        )

    def retrieve(self, key, environment_name=None, **params):
        return Secret.retrieve_secret(key, environment_name=environment_name, **self._translate_options(params))

    def create(self, **params):
        return Secret.create(**self._translate_options(params))

    def modify(self, **params):
        return Secret.modify(**self._translate_options(params))

    def list_environments(self, **params):
        return Environment.list(**self._translate_options(params))

    def get_environment(self, name, **params):
        return Environment.get_environment(
            name=name,
            **self._translate_options(params)
        )

    def retrieve_environment(self, name, **params):
        return Environment.retrieve_environment(
            name=name,
            **self._translate_options(params)
        )

    def create_environment(self, **params):
        return Environment.create(**self._translate_options(params))

    def modify_environment(self, **params):
        return Environment.modify(**self._translate_options(params))
