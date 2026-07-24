# -*- coding: utf-8 -*-
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .algorithms.grid_labels import GridLabelerAlgorithm
from .i18n import tr


class GridLabelerProvider(QgsProcessingProvider):

    def id(self):
        return "reference_grid_labeler"

    def name(self):
        return tr("provider_name")

    def icon(self):
        return QIcon()

    def loadAlgorithms(self):
        self.addAlgorithm(GridLabelerAlgorithm())
