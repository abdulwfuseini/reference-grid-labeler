# -*- coding: utf-8 -*-
"""
Reference Grid Labeler

Builds an atlas-style index grid (columns and rows, each independently
lettered or numbered) over a chosen extent, plus a border-inset label
layer - the classic reference grid used on street atlases and map-book
pages.
"""
from qgis.core import (
    Qgis,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterExtent,
    QgsProcessingParameterCrs,
    QgsProcessingParameterDistance,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterDefinition,
    QgsProcessingException,
    QgsProcessingLayerPostProcessorInterface,
    QgsMessageLog,
    QgsProject,
    QgsCoordinateTransform,
    QgsUnitTypes,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsWkbTypes,
    QgsFillSymbol,
    QgsMarkerSymbol,
    QgsSingleSymbolRenderer,
    QgsPalLayerSettings,
    QgsTextFormat,
    QgsTextBufferSettings,
    QgsVectorLayerSimpleLabeling,
)


def _resolve_label_placement(name):
    """Resolve a label placement enum member across QGIS versions.

    QGIS >= ~3.34 moved this enum under the Qgis namespace. On some builds
    the old QgsPalLayerSettings.<Name> flat alias resolves to the WRONG
    enum (e.g. LabelPredefinedPointPosition instead of LabelPlacement) and
    raises a TypeError when assigned - so prefer the namespaced form
    whenever it's available, and fall back to the older per-class enum on
    QGIS versions that don't have Qgis.LabelPlacement yet.
    """
    try:
        return getattr(Qgis.LabelPlacement, name)
    except AttributeError:
        return getattr(QgsPalLayerSettings, name)


_LABEL_PLACEMENT_OVER_POINT = _resolve_label_placement("OverPoint")

# QGIS has no separate "around centroid" enum member - OverPoint is
# documented as placing labels "over a point, or centroid of a polygon",
# so the same value centers a label on a polygon's centroid too.
_LABEL_PLACEMENT_AROUND_CENTROID = _LABEL_PLACEMENT_OVER_POINT

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor, QFont
from qgis.utils import iface as _iface

from ..label_utils import generate_label_range, generate_labels_from_start
from ..i18n import tr

MAX_CELLS = 10000

# Index 0/1 meaning for the label-type and direction enum parameters below.
_LABEL_TYPES = ("letters", "numbers")


def _refresh_layer(layer):
    """Force the canvas/legend to actually pick up a style or labeling
    change made from a Processing post-processing callback. Setting the
    renderer/labeling alone updates the layer object, but QGIS doesn't
    always redraw the canvas or refresh the legend symbol until something
    else triggers it (e.g. the user clicking the layer) - calling
    triggerRepaint() by itself isn't reliably enough here."""
    layer.triggerRepaint()
    layer.emitStyleChanged()
    if _iface is not None and _iface.mapCanvas() is not None:
        _iface.mapCanvas().refreshAllLayers()


def _build_label_text_format(point_size=10):
    """Shared bold, white-haloed text style for both the grid's centroid
    labels and the border point labels, so they look consistent."""
    text_format = QgsTextFormat()
    font = QFont()
    font.setBold(True)
    font.setPointSize(point_size)
    text_format.setFont(font)
    text_format.setSize(point_size)
    text_format.setColor(QColor(0, 0, 0))

    buffer_settings = QgsTextBufferSettings()
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(1)
    buffer_settings.setColor(QColor(255, 255, 255))
    text_format.setBuffer(buffer_settings)
    return text_format


class _GridStylePostProcessor(QgsProcessingLayerPostProcessorInterface):
    """Styles the grid cell polygon layer as an unfilled, thin-outlined
    layer, so it renders as just a line network over the map - no fill to
    manually turn off afterwards. Optionally also turns on PAL labeling for
    a given field, centered on each polygon's centroid - used for the
    per-cell combined reference (e.g. 'C4'), applied directly on the grid
    layer itself rather than via a separate point feature."""

    _instances = []  # keep processors alive until QGIS is done with them

    def __init__(self, center_label_field=None):
        super().__init__()
        self._center_label_field = center_label_field

    def postProcessLayer(self, layer, context, feedback):
        symbol = QgsFillSymbol.createSimple({
            "color": "0,0,0,0",
            "outline_color": "0,170,220,255",
            "outline_width": "0.3",
            "outline_width_unit": "MM",
        })
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))

        if self._center_label_field:
            settings = QgsPalLayerSettings()
            settings.fieldName = self._center_label_field
            settings.placement = _LABEL_PLACEMENT_AROUND_CENTROID
            settings.setFormat(_build_label_text_format())
            layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
            layer.setLabelsEnabled(True)

        _refresh_layer(layer)

    @classmethod
    def create(cls, center_label_field=None):
        processor = cls(center_label_field)
        cls._instances.append(processor)
        return processor


class _AutoLabelPostProcessor(QgsProcessingLayerPostProcessorInterface):
    """Turns on PAL labeling for the border-label point layer using a
    given field, with a bold, haloed style that's readable straight away.
    The points themselves get a fully transparent marker symbol rather
    than being drawn normally, so they never show up as visible dots - in
    the map canvas, in a print layout, or as a symbol swatch in the Layers
    panel legend - only the text labels show."""

    _instances = []

    def __init__(self, field_name):
        super().__init__()
        self._field_name = field_name

    def postProcessLayer(self, layer, context, feedback):
        settings = QgsPalLayerSettings()
        settings.fieldName = self._field_name
        settings.placement = _LABEL_PLACEMENT_OVER_POINT
        settings.setFormat(_build_label_text_format())

        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        layer.setLabelsEnabled(True)

        # Fully transparent marker (fill and outline alpha both 0). Labeling
        # reads the point geometry regardless of the renderer, so this
        # doesn't affect label placement - it just keeps the point itself
        # from ever being visibly drawn anywhere, including the legend
        # swatch in the Layers panel.
        symbol = QgsMarkerSymbol.createSimple({
            "color": "0,0,0,0",
            "outline_color": "0,0,0,0",
        })
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))

        _refresh_layer(layer)

    @classmethod
    def create(cls, field_name):
        processor = cls(field_name)
        cls._instances.append(processor)
        return processor


class GridLabelerAlgorithm(QgsProcessingAlgorithm):

    GRID_EXTENT = "GRID_EXTENT"
    CRS = "CRS"
    EXTENT_BUFFER = "EXTENT_BUFFER"
    USE_CUSTOM_CELL_SIZE = "USE_CUSTOM_CELL_SIZE"
    CELL_WIDTH = "CELL_WIDTH"
    CELL_HEIGHT = "CELL_HEIGHT"
    EXCLUDE_I = "EXCLUDE_I"
    COLUMN_LABEL_TYPE = "COLUMN_LABEL_TYPE"
    COLUMN_RANGE_FROM = "COLUMN_RANGE_FROM"
    COLUMN_RANGE_TO = "COLUMN_RANGE_TO"
    COLUMN_DIRECTION = "COLUMN_DIRECTION"
    ROW_LABEL_TYPE = "ROW_LABEL_TYPE"
    ROW_RANGE_FROM = "ROW_RANGE_FROM"
    ROW_RANGE_TO = "ROW_RANGE_TO"
    ROW_DIRECTION = "ROW_DIRECTION"
    CELL_LABEL_FORMAT = "CELL_LABEL_FORMAT"
    CENTER_LABELS = "CENTER_LABELS"
    BORDER_SIDES = "BORDER_SIDES"
    LABEL_MARGIN = "LABEL_MARGIN"
    OUTPUT_GRID = "OUTPUT_GRID"
    OUTPUT_LABELS = "OUTPUT_LABELS"

    def createInstance(self):
        return GridLabelerAlgorithm()

    def name(self):
        return "reference_grid_labeler"

    def displayName(self):
        return tr("alg_display_name")

    def group(self):
        # Deliberately empty: with only one algorithm in this provider,
        # nesting it under a "Cartography" subgroup just adds an extra
        # click for no benefit - an empty group makes it show up directly
        # under the "Reference Grid Labeler" provider node instead.
        return ""

    def groupId(self):
        return ""

    def shortHelpString(self):
        return tr("alg_short_help")

    def initAlgorithm(self, config=None):
        # --- grid geometry ---
        self.addParameter(
            QgsProcessingParameterExtent(
                self.GRID_EXTENT, tr("param_grid_extent_label")
            )
        )
        self.addParameter(
            QgsProcessingParameterCrs(
                self.CRS,
                tr("param_crs_label"),
                defaultValue="ProjectCrs",
            )
        )
        extent_buffer_param = QgsProcessingParameterDistance(
            self.EXTENT_BUFFER,
            tr("param_extent_buffer_label"),
            parentParameterName=self.CRS,
            optional=True,
            minValue=0,
            defaultValue=0,
        )
        extent_buffer_param.setDefaultUnit(QgsUnitTypes.DistanceMeters)
        self.addParameter(extent_buffer_param)
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.USE_CUSTOM_CELL_SIZE,
                tr("param_use_custom_cell_size_label"),
                defaultValue=False,
            )
        )
        cell_width_param = QgsProcessingParameterDistance(
            self.CELL_WIDTH,
            tr("param_cell_width_label"),
            parentParameterName=self.CRS,
            optional=True,
            minValue=0,
        )
        cell_width_param.setDefaultUnit(QgsUnitTypes.DistanceMeters)
        self.addParameter(cell_width_param)

        cell_height_param = QgsProcessingParameterDistance(
            self.CELL_HEIGHT,
            tr("param_cell_height_label"),
            parentParameterName=self.CRS,
            optional=True,
            minValue=0,
        )
        cell_height_param.setDefaultUnit(QgsUnitTypes.DistanceMeters)
        self.addParameter(cell_height_param)

        # --- label range ---
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.EXCLUDE_I,
                tr("param_exclude_i_label"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.COLUMN_LABEL_TYPE,
                tr("param_column_label_type_label"),
                options=[tr("opt_letters"), tr("opt_numbers")],
                defaultValue=0,
            )
        )
        column_range_from_param = QgsProcessingParameterString(
            self.COLUMN_RANGE_FROM,
            tr("param_column_range_from_label"),
            defaultValue="A",
        )
        column_range_from_param.setHelp(tr("hint_range_value"))
        self.addParameter(column_range_from_param)
        column_range_to_param = QgsProcessingParameterString(
            self.COLUMN_RANGE_TO,
            tr("param_column_range_to_label"),
            defaultValue="K",
        )
        column_range_to_param.setHelp(tr("hint_range_value"))
        self.addParameter(column_range_to_param)
        self.addParameter(
            QgsProcessingParameterEnum(
                self.COLUMN_DIRECTION,
                tr("param_column_direction_label"),
                options=[tr("opt_left_to_right"), tr("opt_right_to_left")],
                defaultValue=0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.ROW_LABEL_TYPE,
                tr("param_row_label_type_label"),
                options=[tr("opt_letters"), tr("opt_numbers")],
                defaultValue=1,
            )
        )
        row_range_from_param = QgsProcessingParameterString(
            self.ROW_RANGE_FROM,
            tr("param_row_range_from_label"),
            defaultValue="1",
        )
        row_range_from_param.setHelp(tr("hint_range_value"))
        self.addParameter(row_range_from_param)
        row_range_to_param = QgsProcessingParameterString(
            self.ROW_RANGE_TO,
            tr("param_row_range_to_label"),
            defaultValue="10",
        )
        row_range_to_param.setHelp(tr("hint_range_value"))
        self.addParameter(row_range_to_param)
        self.addParameter(
            QgsProcessingParameterEnum(
                self.ROW_DIRECTION,
                tr("param_row_direction_label"),
                options=[tr("opt_top_to_bottom"), tr("opt_bottom_to_top")],
                defaultValue=0,
            )
        )
        cell_label_format_param = QgsProcessingParameterString(
            self.CELL_LABEL_FORMAT,
            tr("param_cell_label_format_label"),
            defaultValue="{col}{row}",
        )
        # Advanced: the default already gives the standard atlas-style
        # reference (e.g. C4); this only matters for anyone matching a
        # custom map-sheet naming convention, so it's tucked under
        # "Advanced Parameters" instead of cluttering the main dialog.
        cell_label_format_param.setFlags(
            cell_label_format_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced
        )
        self.addParameter(cell_label_format_param)

        # --- label placement ---
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.CENTER_LABELS,
                tr("param_center_labels_label"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.BORDER_SIDES,
                tr("param_border_sides_label"),
                options=[
                    tr("opt_side_top"),
                    tr("opt_side_bottom"),
                    tr("opt_side_left"),
                    tr("opt_side_right"),
                ],
                allowMultiple=True,
                defaultValue=[0, 1, 2, 3],
            )
        )
        label_margin_param = QgsProcessingParameterDistance(
            self.LABEL_MARGIN,
            tr("param_label_margin_label"),
            parentParameterName=self.CRS,
            optional=True,
            minValue=0,
        )
        label_margin_param.setDefaultUnit(QgsUnitTypes.DistanceMeters)
        label_margin_param.setHelp(tr("hint_label_margin"))
        self.addParameter(label_margin_param)

        # --- output ---
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_GRID,
                tr("param_output_grid_label"),
                type=QgsProcessing.TypeVectorPolygon,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_LABELS,
                tr("param_output_labels_label"),
                type=QgsProcessing.TypeVectorPoint,
            )
        )

    @staticmethod
    def _guess_source_layer_name(extent, crs, context):
        """Best-effort only: if the resolved extent closely matches a
        loaded layer's own extent (reprojected into the working CRS if
        needed), returns that layer's name - purely informational, to
        help identify which layer an extent likely came from in the log.
        Not exact - multiple layers can share very similar extents - so
        this is reported as a guess, never asserted as fact. Returns None
        on any failure or if nothing matches closely enough; never raises,
        since this is a nice-to-have on top of the always-printed raw
        coordinates above, not something that should ever break a run."""
        try:
            project = context.project() or QgsProject.instance()
            if project is None or extent.isEmpty():
                return None
            tolerance = max(extent.width(), extent.height()) * 0.001
            if tolerance <= 0:
                return None
            for layer in project.mapLayers().values():
                try:
                    layer_extent = layer.extent()
                    layer_crs = layer.crs()
                    if layer_crs.isValid() and crs.isValid() and layer_crs != crs:
                        transform = QgsCoordinateTransform(layer_crs, crs, context.transformContext())
                        layer_extent = transform.transformBoundingBox(layer_extent)
                    if (
                        abs(layer_extent.xMinimum() - extent.xMinimum()) <= tolerance
                        and abs(layer_extent.yMinimum() - extent.yMinimum()) <= tolerance
                        and abs(layer_extent.xMaximum() - extent.xMaximum()) <= tolerance
                        and abs(layer_extent.yMaximum() - extent.yMaximum()) <= tolerance
                    ):
                        return layer.name()
                except Exception as layer_exc:
                    QgsMessageLog.logMessage(
                        "Skipped layer '{}' while guessing source layer name: {}".format(
                            layer.name() if layer is not None else "<unknown>", layer_exc
                        ),
                        "Reference Grid Labeler",
                        Qgis.Info,
                    )
                    continue
        except Exception as guess_exc:
            QgsMessageLog.logMessage(
                "Could not guess source layer name: {}".format(guess_exc),
                "Reference Grid Labeler",
                Qgis.Info,
            )
        return None

    def processAlgorithm(self, parameters, context, feedback):
        # A single explicit working CRS drives three things: the CRS the
        # extent gets reprojected into (parameterAsExtent does this
        # automatically when given a target crs), the CRS distance-unit
        # conversions are made against, and the output layers' CRS.
        crs = self.parameterAsCrs(parameters, self.CRS, context)
        extent = self.parameterAsExtent(parameters, self.GRID_EXTENT, context, crs)

        if extent.isEmpty() or extent.width() <= 0 or extent.height() <= 0:
            raise QgsProcessingException(tr("err_invalid_extent"))

        # Report exactly what extent got used - the native extent field
        # only ever shows raw coordinates, even right after picking
        # "Calculate from layer", which gets confusing across multiple
        # runs/batch rows with different source layers. This can't be
        # fixed in the field itself without a custom widget (which has
        # proven unreliable), so it's reported here instead: printed to
        # the log every run, plus a best-effort guess at which loaded
        # layer it matches, if any.
        feedback.pushInfo(
            tr(
                "info_grid_extent",
                xmin="{:.2f}".format(extent.xMinimum()),
                ymin="{:.2f}".format(extent.yMinimum()),
                xmax="{:.2f}".format(extent.xMaximum()),
                ymax="{:.2f}".format(extent.yMaximum()),
                crs=crs.authid() if crs.isValid() else "?",
                width="{:.2f}".format(extent.width()),
                height="{:.2f}".format(extent.height()),
            )
        )
        source_layer_name = self._guess_source_layer_name(extent, crs, context)
        if source_layer_name:
            feedback.pushInfo(tr("info_grid_extent_layer_guess", name=source_layer_name))

        # Expand the extent outward on all sides before any cell-size math,
        # so the grid built from a layer's extent doesn't hug its features -
        # e.g. picking a layer as the extent source and setting a buffer
        # keeps its geometries from touching/overlapping the grid border.
        extent_buffer = self.parameterAsDouble(parameters, self.EXTENT_BUFFER, context)
        if extent_buffer and extent_buffer > 0:
            extent = extent.buffered(extent_buffer)

        exclude_i = self.parameterAsBoolean(parameters, self.EXCLUDE_I, context)

        column_label_type = _LABEL_TYPES[
            self.parameterAsEnum(parameters, self.COLUMN_LABEL_TYPE, context)
        ]
        column_from = self.parameterAsString(parameters, self.COLUMN_RANGE_FROM, context).strip() or "A"
        column_to = self.parameterAsString(parameters, self.COLUMN_RANGE_TO, context).strip() or column_from
        column_reversed = self.parameterAsEnum(parameters, self.COLUMN_DIRECTION, context) == 1

        row_label_type = _LABEL_TYPES[
            self.parameterAsEnum(parameters, self.ROW_LABEL_TYPE, context)
        ]
        row_from = self.parameterAsString(parameters, self.ROW_RANGE_FROM, context).strip() or "1"
        row_to = self.parameterAsString(parameters, self.ROW_RANGE_TO, context).strip() or row_from
        row_reversed = self.parameterAsEnum(parameters, self.ROW_DIRECTION, context) == 1

        use_custom_cell_size = self.parameterAsBoolean(
            parameters, self.USE_CUSTOM_CELL_SIZE, context
        )
        cell_width = self.parameterAsDouble(parameters, self.CELL_WIDTH, context)
        cell_height = self.parameterAsDouble(parameters, self.CELL_HEIGHT, context)

        if use_custom_cell_size:
            # User-supplied cell size: cell count is derived from the extent,
            # and the extent is extended outward to a whole number of cells.
            # The range "to" fields only set where the label sequence would
            # stop if it were used to derive a count - since the count comes
            # from geometry here instead, only "from" (the starting label)
            # actually matters, and "to" is ignored.
            if not cell_width or not cell_height or cell_width <= 0 or cell_height <= 0:
                raise QgsProcessingException(tr("err_cell_size_required"))
            num_columns = max(1, int(-(-extent.width() // cell_width)))   # ceil
            num_rows = max(1, int(-(-extent.height() // cell_height)))    # ceil
            extent.setXMaximum(extent.xMinimum() + num_columns * cell_width)
            extent.setYMaximum(extent.yMinimum() + num_rows * cell_height)
            try:
                column_labels = generate_labels_from_start(
                    column_label_type, column_from, num_columns, exclude_i
                )
                row_labels = generate_labels_from_start(
                    row_label_type, row_from, num_rows, exclude_i
                )
            except ValueError as exc:
                raise QgsProcessingException(tr("err_invalid_range", detail=str(exc)))
            feedback.pushInfo(tr("info_custom_size_ignores_range"))
        else:
            # Default: the column/row range (From-To) both picks the label
            # sequence and determines the cell count, dividing the given
            # extent evenly - no extent adjustment needed.
            try:
                column_labels, num_columns = generate_label_range(
                    column_label_type, column_from, column_to, exclude_i
                )
                row_labels, num_rows = generate_label_range(
                    row_label_type, row_from, row_to, exclude_i
                )
            except ValueError as exc:
                raise QgsProcessingException(tr("err_invalid_range", detail=str(exc)))
            cell_width = extent.width() / num_columns
            cell_height = extent.height() / num_rows

        # The physical cell grid is always laid out ascending left-to-right
        # (column index 0 = leftmost) and top-to-bottom (row index 0 =
        # topmost). "Reverse" directions are implemented by reversing the
        # LABEL sequence assigned to that fixed physical layout instead of
        # changing the geometry - e.g. "right to left" means the first
        # generated column label ends up on the right-hand column, not that
        # column 0 moves to the right.
        if column_reversed:
            column_labels = list(reversed(column_labels))
        if row_reversed:
            row_labels = list(reversed(row_labels))

        total_cells = num_columns * num_rows
        if total_cells > MAX_CELLS:
            raise QgsProcessingException(
                tr(
                    "err_too_many_cells",
                    count=total_cells,
                    cols=num_columns,
                    rows=num_rows,
                    limit=MAX_CELLS,
                )
            )

        feedback.pushInfo(
            tr("info_grid_size", cols=num_columns, rows=num_rows, count=total_cells)
        )

        center_labels = self.parameterAsBoolean(parameters, self.CENTER_LABELS, context)
        border_sides = set(self.parameterAsEnums(parameters, self.BORDER_SIDES, context))
        border_top = 0 in border_sides
        border_bottom = 1 in border_sides
        border_left = 2 in border_sides
        border_right = 3 in border_sides
        margin = self.parameterAsDouble(parameters, self.LABEL_MARGIN, context)
        if not margin or margin <= 0:
            margin = min(cell_width, cell_height) * 0.08

        cell_label_format = (
            self.parameterAsString(parameters, self.CELL_LABEL_FORMAT, context)
            or "{col}{row}"
        )

        # --- grid cell (polygon) sink ---
        grid_fields = QgsFields()
        grid_fields.append(QgsField("col", QVariant.String))
        grid_fields.append(QgsField("row", QVariant.String))
        grid_fields.append(QgsField("ref", QVariant.String))
        grid_sink, grid_dest_id = self.parameterAsSink(
            parameters, self.OUTPUT_GRID, context, grid_fields,
            QgsWkbTypes.Polygon, crs,
        )
        if grid_sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT_GRID)
            )
        if context.willLoadLayerOnCompletion(grid_dest_id):
            context.layerToLoadOnCompletionDetails(grid_dest_id).setPostProcessor(
                _GridStylePostProcessor.create(
                    center_label_field="ref" if center_labels else None
                )
            )

        # --- label (point) sink ---
        label_fields = QgsFields()
        label_fields.append(QgsField("side", QVariant.String))
        label_fields.append(QgsField("label", QVariant.String))
        label_sink, label_dest_id = self.parameterAsSink(
            parameters, self.OUTPUT_LABELS, context, label_fields,
            QgsWkbTypes.Point, crs,
        )
        if label_sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT_LABELS)
            )
        if context.willLoadLayerOnCompletion(label_dest_id):
            context.layerToLoadOnCompletionDetails(label_dest_id).setPostProcessor(
                _AutoLabelPostProcessor.create(field_name="label")
            )

        x0 = extent.xMinimum()
        y0 = extent.yMinimum()

        total_steps = max(1, num_columns * num_rows)
        step = 0

        for col_idx in range(num_columns):
            if feedback.isCanceled():
                break
            cell_x_min = x0 + col_idx * cell_width
            cell_x_max = cell_x_min + cell_width
            col_label = column_labels[col_idx]
            for row_idx in range(num_rows):
                if feedback.isCanceled():
                    break
                # Row index 0 is always the topmost strip of cells; the
                # ROW_DIRECTION option was already applied above by
                # reversing row_labels, not by moving this geometry.
                cell_y_max = extent.yMaximum() - row_idx * cell_height
                cell_y_min = cell_y_max - cell_height

                row_label = row_labels[row_idx]
                try:
                    ref = cell_label_format.format(col=col_label, row=row_label)
                except (KeyError, IndexError) as exc:
                    raise QgsProcessingException(
                        tr("err_bad_label_format", fmt=cell_label_format, error=str(exc))
                    )

                feat = QgsFeature(grid_fields)
                feat.setGeometry(
                    QgsGeometry.fromPolygonXY([[
                        QgsPointXY(cell_x_min, cell_y_min),
                        QgsPointXY(cell_x_max, cell_y_min),
                        QgsPointXY(cell_x_max, cell_y_max),
                        QgsPointXY(cell_x_min, cell_y_max),
                        QgsPointXY(cell_x_min, cell_y_min),
                    ]])
                )
                feat.setAttributes([col_label, row_label, ref])
                grid_sink.addFeature(feat)

                # Note: the center/combined-reference label (when enabled)
                # is applied directly on the grid polygon layer via PAL
                # labeling in _GridStylePostProcessor, not as a point here -
                # the point/label layer only ever holds the four-side
                # border labels (top/bottom/left/right).

                step += 1
                feedback.setProgress(int(100 * step / total_steps))

        # --- column labels: a strip just inside the top and/or bottom border ---
        if border_top or border_bottom:
            for col_idx in range(num_columns):
                x_center = x0 + (col_idx + 0.5) * cell_width
                if border_top:
                    top_y = extent.yMaximum() - margin
                    _add_label_point(label_sink, label_fields, x_center, top_y, "top", column_labels[col_idx])
                if border_bottom:
                    bottom_y = extent.yMinimum() + margin
                    _add_label_point(label_sink, label_fields, x_center, bottom_y, "bottom", column_labels[col_idx])

        # --- row labels: a strip just inside the left and/or right border ---
        if border_left or border_right:
            for row_idx in range(num_rows):
                y_center = extent.yMaximum() - (row_idx + 0.5) * cell_height
                if border_left:
                    left_x = x0 + margin
                    _add_label_point(label_sink, label_fields, left_x, y_center, "left", row_labels[row_idx])
                if border_right:
                    right_x = extent.xMaximum() - margin
                    _add_label_point(label_sink, label_fields, right_x, y_center, "right", row_labels[row_idx])

        feedback.setProgress(100)

        return {self.OUTPUT_GRID: grid_dest_id, self.OUTPUT_LABELS: label_dest_id}


def _add_label_point(sink, fields, x, y, side, label):
    feat = QgsFeature(fields)
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
    feat.setAttributes([side, label])
    sink.addFeature(feat)
