from typing import Dict, Any

from dynaconf.utils.boxing import DynaBox
from rds.core.config import settings
from rds.core.helpers import instantiate_class
from rds.core.searchengine.adapters.searchengineadapter import SearchEngineAdapter


class ToManyHits(Exception):
    pass


RDS_HOSTS = "https://api.opensearch.dev.lais.ufrn.br"
RDS_MAIN_HOST = RDS_HOSTS.split(",")[:1]


def get_searchengine_config(clustername: str = "default") -> DynaBox:
    if settings.get("SEARCH_ENGINES", None) and settings.SEARCH_ENGINES.get(clustername, None):
        return settings.SEARCH_ENGINES.get(clustername, None)

    return dict(
        **dict(settings.RDS),
        **dict(
            dialect="OpenSearch",
            hosts=RDS_HOSTS,
            ttl=5,
            starting_retry_interval=1,
            starting_max_retries=60,
        ),
    )


def searchengines(
    clustername: str = "default", username: str | None = None, password: str | None = None
) -> SearchEngineAdapter:
    config = get_searchengine_config(clustername)
    dialect = config.get("dialect", "opensearch")
    if dialect.lower() != "opensearch":
        raise NotImplementedError(f"Dialect {dialect} not implemented yet. Possibles: opensearch.")

    params = {k: v for k, v in config.items() if k not in ("dialect", "hosts", "username", "password")}
    params["http_auth"] = (
        username or config.get("username", None),
        password or config.get("password", None),
    )

    return instantiate_class(
        "rds.core.searchengine.adapters.opensearchadapter.OpenSearchAdapter", cluster_name=clustername, **params
    )


default_se = searchengines("default")
