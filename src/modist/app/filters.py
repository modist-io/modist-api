# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains data-types and dependency-injetions for common query parameters."""

from enum import Enum
from typing import List
from dataclasses import dataclass

from fastapi import Query, Depends

SORT_DESCENDING_FLAG = "-"
SORT_ASCENDING_FLAG = "+"
PAGINATION_DEFAULT_SIZE = 10
PAGINATION_DEFAULT_LIMIT = 100


class SortDirection(Enum):
    """Enumeration of allowable sort directions."""

    ASCENDING = "asc"
    DESCENDING = "desc"


@dataclass
class Sort(object):
    """Describes a specific query sorting for a field name."""

    field: str
    direction: SortDirection = SortDirection.ASCENDING


@dataclass
class Pagination(object):
    """Describes the pagination indexes that should be used for queries."""

    size: int = PAGINATION_DEFAULT_SIZE
    page: int = 0


@dataclass
class CollectionFilter(object):
    """The common filters utilized for collection resources."""

    pagination: Pagination
    sorts: List[Sort]


def sort_filters(
    sort: List[str] = Query(
        None,
        title="Sort order",
        description="The sorting that should be applied for requested documents",
    )
) -> List[Sort]:
    """Handle the aggregation of provided sort query parameters.

    :param List[str] sort: A list of query sort entries
    :returns: A list of :class:`~.Sort` instances for the given sort entries
    :rtype: List[Sort]
    """

    sorts: List[Sort] = []
    if not sort:
        return sorts

    for entry in sort:
        field = entry.lstrip(SORT_ASCENDING_FLAG + SORT_DESCENDING_FLAG).strip()
        if len(field) <= 0:
            continue

        marked_ascending = entry.startswith(SORT_ASCENDING_FLAG)
        marked_descending = entry.startswith(SORT_DESCENDING_FLAG)
        is_ascending = marked_ascending or not marked_descending

        sorts.append(
            Sort(
                field=field,
                direction=(
                    SortDirection.ASCENDING
                    if is_ascending
                    else SortDirection.DESCENDING
                ),
            )
        )

    return sorts


def pagination_filters(
    size: int = Query(
        default=PAGINATION_DEFAULT_SIZE,
        title="Pagination size",
        description="The number of paginated documents to return per request",
        gt=0,
        le=PAGINATION_DEFAULT_LIMIT,
    ),
    page: int = Query(
        default=0,
        title="Pagiation page",
        description="The page index of paginated documents to fetch",
        ge=0,
    ),
) -> Pagination:
    """Handle the aggregation of provided pagiation query parameters.

    :param int size: The number of results to return per page
    :param int page: The page index of results to return
    :returns: An instance of :class:`~.Pagination` for the given parameters
    :rtype: Pagination
    """

    return Pagination(size=size, page=page)


def collection_filters(
    pagination: Pagination = Depends(pagination_filters),
    sorts: List[Sort] = Depends(sort_filters),
) -> CollectionFilter:
    """Handle the aggregation of common collection filters.

    :returns: An instance of :class:`~.CollectionFilter` containing aggregated common \
        filters for collection queries
    :rtype: CollectionFilter
    """

    return CollectionFilter(pagination=pagination, sorts=sorts)
