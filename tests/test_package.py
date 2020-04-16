# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""This moudle exposes some initial package building sanity checks."""


def test_version_importable():
    """Basic sanity check to ensure we can discover the package name and version."""

    from modist import __version__

    assert isinstance(__version__.__name__, str)
    assert isinstance(__version__.__version__, str)
