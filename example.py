#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2014 University of Dundee & Open Microscopy Environment.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import numpy
import features

# Note the OMERO client variable must exists (for instance run this script
# from inside `bin/omero shell --login`)

# 10 features within this featureset, each feature is a fixed-width vector
# (but each feature can be a different width)
featureset_name = 'Test Featureset'
feature_names = ['x%04d' % n for n in xrange(10)]
feature_widths = range(1, 11)

manager = features.OmeroTablesFeatureStore.FeatureTableManager(
    client.getSession())

# Create a new featureset (name must be unique within this group)
manager.create(featureset_name, feature_names, feature_widths)

# Retrieve an existing featureset
fs = manager.get(featureset_name)

# Store some features associated with an image. This will automatically create
# an annotation on the image linking it to the underlying table file
imageid = 3889L

values = tuple(numpy.random.rand(n) for n in feature_widths)
fs.store_by_image(imageid, values)

# Retrieve the features
r = fs.fetch_by_image(imageid)
# If multiple matching rows are found this will throw an exception, pass
# last=True to return just the last matching row
r = fs.fetch_by_image(imageid, last=True)

# Feature metadata (currently just Image/Roi IDs):
print '\n'.join('%s=%s' % kv for kv in zip(r.infonames, r.infovalues))

# Feature names and values
print '\n'.join('%s=%s' % kv for kv in zip(r.names, r.values))

# Delete the entire featureset and annotations (may be very slow)
fs.delete()

# Close all tables
manager.close()
