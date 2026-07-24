# -*- coding: utf-8 -*-
"""
Reference Grid Labeler
Adds a "Reference Grid Labeler" algorithm to the QGIS Processing Toolbox.
"""


def classFactory(iface):  # pylint: disable=invalid-name
    from .plugin import GridLabelerPlugin
    return GridLabelerPlugin(iface)
