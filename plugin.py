# -*- coding: utf-8 -*-
"""
Main plugin class. Registers a QgsProcessingProvider exposing the
"Reference Grid Labeler" algorithm, and also adds a toolbar button and a
Plugins-menu entry that open the same algorithm's dialog directly, for
people who don't go looking in the Processing Toolbox.


"""
import os

from qgis.core import QgsApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .provider import GridLabelerProvider
from .i18n import tr

ALGORITHM_ID = "reference_grid_labeler:reference_grid_labeler"


class GridLabelerPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None
        self.action = None
        self.menu_name = tr("menu_name")

    def initGui(self):
        self.provider = GridLabelerProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        icon = QIcon(icon_path) if os.path.isfile(icon_path) else QIcon()

        self.action = QAction(icon, tr("action_text"), self.iface.mainWindow())
        self.action.setToolTip(tr("action_tooltip"))
        self.action.triggered.connect(self._run_algorithm)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(self.menu_name, self.action)

    def _run_algorithm(self):
        import processing
        processing.execAlgorithmDialog(ALGORITHM_ID, {})

    def unload(self):
        if self.provider is not None:
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None
        if self.action is not None:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu(self.menu_name, self.action)
            self.action = None
