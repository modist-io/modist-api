# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from cachetools import LRUCache, cached

from ..db import Database
from ..env import instance as env

db_instance_cache = LRUCache(maxsize=1)


@cached(cache=db_instance_cache)
def get_db() -> Database:
    """Fetch the global application's database instance.

    :return: The initialized database instance.
    :rtype: Database
    """

    return Database(url=env.database.url, echo=env.database.echo)
