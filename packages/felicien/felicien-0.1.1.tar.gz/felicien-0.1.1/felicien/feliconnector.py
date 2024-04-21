#!/usr/bin/env python
# -*- coding: utf8 -*-

import validators
import requests
from felicien.felits import FeliTS

REQUESTS_OPTIONS = {
    "auth": tuple,
    "verify": (bool, str),
    "cert": (tuple, str),
}
TSDB_TYPES = ["prometheus", "victoriametrics"]
API_TSDB_HEALTH = {
    "prometheus": "api/v1/status/tsdb",
    "victoriametrics": "api/v1/status/tsdb",
}
API_TSDB_QUERY = {
    "prometheus": "api/v1/query",
    "victoriametrics": "prometheus/api/v1/query",
}


class FeliConnector:
    """A connector to a TSDB such as Prometheus or VictoriaMetrics

    This is an abstraction class to communicate with a Prometheus API'
    compatible TSDB, via HTTP.
    see official documentation:
    https://prometheus.io/docs/prometheus/latest/querying/api/
    https://docs.victoriametrics.com/url-examples/

    Attributes:
        base_url: the URL of the TSDB
        tsdb: the type of TSDB: prometheus, victoriametrics
        _options: the requests options, such as auth or (m)TLS
    """

    def __init__(
        self, url: str = None, tsdb: str = "prometheus", options: dict = {}
    ) -> None:
        """Initializes the instance based the access to a TSDB

        Args:
            url (str, optional): Base URL of the TSDB.
                Defaults to None.
            tsdb (str, optional): Type of TSDB. Can be "prometheus",
                "victoriametrics".
                Defaults to "prometheus"
            options (dict, optional): Options to use with requests, such as
                auth, TLS verification, client certificate, ...

        Raises:
            ValueError if the url is not valid
            ValueError if tsdb is not a valid type
            ConnectionError if TSDB API is not reachable
            KeyError if a option passed to requests is invalid
        """
        if url is None or not validators.url(url):
            raise ValueError("'url' is not a valid URL")

        self.base_url = url

        if tsdb not in TSDB_TYPES:
            raise ValueError(
                f"invalid tsdb type. Options: {', '.join(TSDB_TYPES)}"
            )
        self.tsdb = tsdb

        self._options = dict()
        if options:
            for k, v in options.items():
                if k in REQUESTS_OPTIONS.keys() and isinstance(
                    v, REQUESTS_OPTIONS[k]
                ):
                    self._options[k] = v
                else:
                    raise KeyError(f"{k} is an invalid option for requests")

        # test connection to the TSDB
        r = requests.get(
            f"{self.base_url}/{API_TSDB_HEALTH[self.tsdb]}", **self._options
        )
        if not (r.status_code == 200 and r.json().get("status") == "success"):
            raise ConnectionError(f"unable to reach TSDB API: {r.status_code}")

    def __repr__(self) -> str:
        return f"FeliConnector([{self.tsdb}]{{{self.base_url}}})"

    def get_timeserie(self, metric: str = None) -> FeliTS:
        """Retrieve a timeserie from the TSDB

        Args:
            metric (str, optional): metric of the timeserie, expressed in
                PromQL. Defaults to None.

        Returns:
            FeliTS: Timeserie of the metric

        Raises:
            ConnectionError if query status code is not HTTP/200
            OverflowError if the result is more than one timeserie
            ValueError if the result is empty
            TypeError if the result is not a vector (range or instant)
        """
        payload = {"query": metric}

        r = requests.get(
            f"{self.base_url}/{API_TSDB_QUERY[self.tsdb]}",
            **self._options,
            params=payload,
        )
        if not (r.status_code == 200 and r.json().get("status") == "success"):
            raise ConnectionError(f"unable to get timeserie: {r.status_code}")

        # connection is successful
        if len(r.json().get("data", {}).get("result")) > 1:
            raise OverflowError("query returns more than one timeserie")
        elif len(r.json().get("data", {}).get("result")) == 0:
            raise ValueError("query returned no timeserie")

        # result length is correct
        if r.json().get("data", {}).get("resultType") in [
            "matrix",
            "vector",
        ]:
            return FeliTS(
                from_prom=r.json().get("data", {}).get("result", [])[0]
            )
        else:
            raise TypeError(
                "query result can be only range vectors or instant vectors"
            )
