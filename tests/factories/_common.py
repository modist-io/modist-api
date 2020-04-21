# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains common namespaced imports required by factories."""

# NOTE: Although this remapping could potentially be done within the factory files
# themselves, we keep this reference in a namespaced common module so that we don't
# conflict with the names provided by the base (test) module (test.__init__)

from .. import SQLALCHEMY_SESSION
