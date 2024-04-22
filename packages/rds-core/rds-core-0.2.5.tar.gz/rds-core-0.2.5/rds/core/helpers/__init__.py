"""
Documentar.
"""

from typing import Any
import logging
import json
import importlib
from datetime import datetime
from os import getenv
from opensearchpy.helpers.search import Search
from opensearchpy.helpers.response import Response

logger = logging.getLogger(__name__)


def str2bool(v):
    TRUE_STRS = ("true", "verdade", "yes", "sim", "t", "v", "y", "s", "1")
    FALSE_STRS = ("false", "falso", "no", "nao", "não", "f", "n", "0")

    if isinstance(v, bool):
        return v

    if v is None or (isinstance(v, str) and v.strip() == ""):
        return None

    if isinstance(v, int) and v in (1, 0):
        return v == 1

    if isinstance(v, str) and v.strip().lower() in TRUE_STRS + FALSE_STRS:
        return v.lower() in TRUE_STRS

    raise ValueError("Boolean value expected.")


def env(name, default=None, wrapped=False):
    result = getenv(name, default)
    if wrapped and isinstance(result, str) and result[0:1] == "'" and result[-1:] == "'":
        return result[1:-1]
    return result


def env_as_list(name, default="", delimiter=",", wrapped=False):
    result = env(name, default, wrapped)
    if result is None:
        return None
    if type(result) == str:
        if result.strip() == "" and default.strip() == "":
            return []
        return result.split(delimiter)
    if type(result) in (list, tuple):
        return list(result)
    raise TypeError("env_as_list requires str, list or tuple as default")


def env_as_list_of_maps(name, key, default="", delimiter=",", wrapped=False):
    return [{key: x} for x in env_as_list(name, default, delimiter, wrapped)]


def env_as_bool(name, default=None, wrapped=False):
    return str2bool(env(name, default, wrapped))


def env_from_json(key, default="", wrapped=False):
    result = env(key, default, wrapped)
    return json.loads(result) if result is not None else result


def env_as_int(key, default=None, wrapped=False):
    result = env(key, default, wrapped)
    return int(result) if result is not None else result


def env_as_float(key, default=None, wrapped=False):
    result = env(key, default, wrapped)
    return float(result) if result is not None else result


def get_class(full_class_name: str) -> Any:
    module_name, class_name = full_class_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)


def instantiate_class(full_class_name: str, *args: list, **kwargs: dict[str, Any]) -> Any:
    Klass = get_class(full_class_name)
    return Klass(*args, **kwargs)


def get_variable_by_pathname(full_class_name: str) -> Any:
    module_name, class_name = full_class_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)


def get_dict_by_pathname(obj: dict, ref: str) -> Any:
    """
    Use MongoDB style 'something.by.dot' syntax to retrieve objects from Python dicts.

    Usage:
       >>> x = {"top": {"middle" : {"nested": "value"}}}
       >>> q = 'top.middle.nested'
       >>> get_dict_by_pathname(x,q)
       "value"

    Credit: https://gist.github.com/mittenchops/5664038
    """
    val = obj
    tmp = ref
    ref = tmp.replace(".XX", "[0]")
    if tmp != ref:
        logger.warning("Warning: replaced '.XX' with [0]-th index")
    for key in ref.split("."):
        idstart = key.find("[")
        embedslist = 1 if idstart > 0 else 0
        if embedslist:
            idx = int(key[idstart + 1 : key.find("]")])
            kyx = key[:idstart]
            try:
                val = val[kyx][idx]
            except IndexError:
                logger.warning(f"Index: x['{kyx}'][{idx}] does not exist.")
                raise
        else:
            val = val.get(key, None) if val is not None else None
    return val


class Color:
    ENDC = "\033[0m"

    def r(text: str) -> str:
        """Returns a *red* string"""
        return f"\033[91m{text}{Color.ENDC}"

    def b(text: str) -> str:
        """Returns a *blue* string"""
        return f"\033[94m{text}{Color.ENDC}"

    def g(text: str) -> str:
        """Returns a *green* string"""
        return f"\033[92m{text}{Color.ENDC}"

    def c(text: str) -> str:
        """Returns a *cyan* string"""
        return f"\033[96m{text}{Color.ENDC}"

    def m(text: str) -> str:
        """Returns a *magenta* string"""
        return f"\033[95m{text}{Color.ENDC}"

    def y(text: str) -> str:
        """Returns a *yellow* string"""
        return f"\033[93m{text}{Color.ENDC}"

    def s(text: str) -> str:
        """Returns a *strong* string"""
        return f"\033[1m{text}{Color.ENDC}"

    def u(text: str) -> str:
        """Returns a *underlined* string"""
        return f"\033[4m{text}{Color.ENDC}"


class TEMPERATURE:
    COLD = "COLD"
    WARN = "WARN"
    HOT = "HOT"


class DATASOURCE:
    RDS = "RDS"
    RNDS = "RNDS/DATASUS"
    REST = "REST/CNES/DATASUS"
    SOAP = "SOAP/CNES/DATASUS"


# |	     | COLD | WARN | HOT |
# | ---- | ---- | ---- | --- |
# | RDS  |  x   |  x   |     |
# | RNDS |      |      |  x  |
# | REST |      |      |  x  |
# | SOAP |      |      |  x  |


def coldfy(obj: dict | list | Search | Response, datasource: str | None = "RDS") -> dict | list:
    if isinstance(obj, dict):
        obj["@timestamp"] = obj.get("@timestamp", datetime.now())
        obj["@temperature"] = obj.get("@temperature", TEMPERATURE.COLD)
        if datasource:
            obj["@datasource"] = obj.get("@datasource", datasource)
        return obj

    if isinstance(obj, list):
        return [coldfy(h["_source"].to_dict(), datasource) for h in obj if isinstance(h, dict)]

    if isinstance(obj, Response):
        return [coldfy(h["_source"].to_dict(), datasource) for h in obj["hits"]["hits"]]

    if isinstance(obj, Search):
        return [coldfy(h["_source"].to_dict(), datasource) for h in obj.execute()["hits"]["hits"]]

    return obj
