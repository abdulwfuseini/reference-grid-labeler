# Reference Grid Labeler - User Guide

## What this tool is for

If you produce street atlases, map books, gazetteers, or any print map that needs a search grid in the margin (the classic "find it at C4" index), this tool builds that grid for you automatically. Instead of drawing grid lines by hand and placing letter/number labels one at a time, you pick an area, run the tool once, and get two finished layers - a grid and its border labels - ready to drop into your map or print layout.

It works just as well for a single map as it does across a whole atlas: run it once per map page, or use QGIS's batch processing (covered below) to generate the grid for many pages or areas in one go.

## Installing the plugin

1. In QGIS, open **Plugins > Manage and Install Plugins > Install from ZIP**.
2. Browse to the `.zip` file and click **Install Plugin**.
3. Once installed, you'll find the tool in three places - use whichever fits your workflow:
   - **Processing Toolbox**, under **Reference Grid Labeler**.
   - A toolbar button (the plugin's icon).
   - **Plugins** menu, under **Reference Grid Labeler**.

All three open the same dialog.

## Quick start

1. Open the tool from any of the three locations above.
2. Under **Grid extent**, choose where the grid should cover - the current map view, a layer's extent, or type coordinates directly.
3. Leave everything else at its defaults for a first try, and click **Run**.
4. Two new layers appear: a grid of cells and a set of border labels. Both come pre-styled - the grid as plain outlines, the labels already switched on - so you can look at the result immediately.

Once you're happy with a basic grid, go through the sections below to adjust letters vs. numbers, direction, spacing, and which sides get labeled.

## Understanding each input

### Grid geometry

**Grid extent** - the area the grid will cover. Click the small dropdown/arrow button next to the field for your options: use the current map view, calculate it from a layer, calculate it from a print layout or a bookmark, draw a rectangle on the map, or type coordinates in directly. This is QGIS's own standard extent picker, the same one used across all Processing tools, so it behaves exactly like you'd expect elsewhere in QGIS.

A practical note: once you pick an option, the field only ever shows raw coordinates (e.g. `388338.80,610073.23,5265158.61,5515628.40 [EPSG:25832]`), not which layer you picked it from. If you're working across several layers with different extents and want to double check what was actually used, check the run log after clicking **Run** - the tool prints the resolved extent, its width and height, and a best-effort guess at which loaded layer it matches (see **Reading the run log** below).

**Working CRS** - the coordinate reference system everything else is calculated in: the extent gets reprojected into this CRS if needed, and it determines which measurement units (metres, feet, degrees, etc.) are offered for the size/spacing fields further down. Defaults to your project's CRS, which is almost always what you want.

**Margin around extent** - expands the extent outward before the grid is built. Leave at 0 for no margin. This is especially useful when your extent comes from a layer: a small margin keeps that layer's own features from touching or overlapping the grid's outer border.

**Use a custom cell size instead** - unchecked by default, meaning you specify an exact number of columns and rows instead (via the ranges below) and the tool works out the cell size to fit. Check this box if you'd rather fix the cell size itself (e.g. "each cell is exactly 1 km") and let the tool work out how many columns/rows fit - the extent is expanded slightly outward so cells divide it evenly.

**Cell width / Cell height** - only used when "Use a custom cell size instead" is checked. Enter a size and pick a unit from the dropdown next to each field (metres, kilometres, feet, degrees, and more). If left blank while the checkbox above is checked, the tool will stop with an error asking you to fill them in - they're only actually required in that mode, so it's safe to leave them blank otherwise.

### Label range

**Exclude letter 'I' from letter sequences** - on by default. Skips the letter I wherever letters are used, since it's easily confused with the number 1 or a lowercase L - standard practice on printed reference grids.

**Column labels / Row labels** - choose Letters or Numbers independently for columns and rows. The classic atlas layout is letters across the top (columns) and numbers down the side (rows), which is why Row labels defaults to Numbers while Column labels defaults to Letters - but you're free to set both the same way if that suits your map better.

**Range - From / Range - To** (one pair for columns, one pair for rows) - plain text fields where you type the first and last label. For letters, type a single letter (e.g. `A` to `K`); columns roll over into double letters automatically past Z (…, X, Y, Z, AA, AB, …). For numbers, type digits (e.g. `1` to `10`). These two fields are always plain text - there's no dropdown restricting what you can type, which is deliberate: it means any custom starting point or range works (including things like `100` to `130`), you're just responsible for typing a value that matches whichever mode (Letters/Numbers) you picked above.

When "Use a custom cell size instead" is checked, only the **From** value matters (it's the starting label) - **To** is ignored, since the number of columns/rows comes from the geometry instead.

**Column direction / Row direction** - which way the sequence runs: left-to-right or right-to-left for columns, top-to-bottom or bottom-to-top for rows.

**Cell label format** (under **Advanced Parameters**, at the bottom of the dialog) - the template for each cell's combined reference, using the placeholders `{col}` and `{row}`. Defaults to `{col}{row}` (giving references like `C4`), but you can reorder or decorate it however you like, e.g. `{row}-{col}` for `4-C`, or `Sheet {col}{row}`. Most users never need to touch this - it's only there for matching an existing map-sheet naming convention.

### Label placement

**Label every grid cell** - off by default. Turn this on to also place a label (the combined reference, e.g. `C4`) at the center of every single cell, in addition to the border labels. Useful if you want to be able to identify a cell directly on the map itself, not just via the border index.

**Border index labels on** - a multi-select field: click it to open a checklist of Top, Bottom, Left, and Right, and check whichever sides you want labeled. All four are checked by default, matching the classic printed-atlas look (column letters along the top and bottom, row numbers down the left and right) - uncheck any sides you don't need, e.g. if the map will be bound and only two edges are ever visible.

**Inset from grid edge** - how far inside the outer border the labels sit. Leave blank and the tool picks a sensible distance automatically based on cell size; enter your own value plus a unit if you want more or less spacing. After the tool runs, you can still fine-tune any individual label's position by hand using the Labels toolbar's "Move Label" tool.

### Output

**Grid layer** - the polygon output: one rectangle per cell, carrying `col`, `row`, and the combined `ref` (e.g. `C4`) as attributes. Comes pre-styled as an outline only, so it reads as plain grid lines. Use the attributes for joins/lookups if you need to link other data to a specific cell.

**Grid labels** - the point output for the border labels (and cell-center labels, if turned on), carrying `side` (top/bottom/left/right/center) and `label` as attributes. Comes with labeling already switched on using the `label` field.

Both default to a temporary layer added to your project; click the **…** button to save either as a permanent file instead (GeoPackage, Shapefile, etc.) if you want to keep the result.

## Reading the run log

Every time you click **Run**, before it builds anything, the tool prints a line to the log (visible in the **Log** tab of the dialog, and afterward in **View > Panels > Log Messages**) reporting the extent it actually resolved: coordinates, CRS, and width × height. If that extent happens to match a currently loaded layer's own extent closely, it also prints that layer's name as a best-effort guess. This is your way to double-check "did it actually use the layer/area I meant?" without the extent field itself needing to show anything more than raw numbers.

## Using batch processing

If you need to generate a grid for many pages, tiles, or study areas in one run instead of opening the dialog repeatedly, use QGIS's built-in batch processing feature - it's not specific to this plugin, but works the same way here as with any other Processing tool:

1. Open the Reference Grid Labeler dialog as usual.
2. Click **Run as Batch Process...** at the bottom of the dialog (or right-click the algorithm in the Processing Toolbox and choose it from there).
3. A table opens with one row per run and one column per parameter. Add as many rows as you need (the **+** button, or paste values from a spreadsheet).
4. Fill in each row - typically you'll vary **Grid extent** (e.g. a different layer or set of coordinates per row) while keeping most other settings the same across all rows; you can also override the label range, direction, or format per row if different pages need different labeling.
5. Set **Grid layer** and **Grid labels** for each row to a real file path rather than a temporary layer (e.g. `C:/atlas/page_01_grid.gpkg`), so each run's output is kept and doesn't overwrite the others. Use a naming pattern that matches your page/tile numbering.
6. Click **Run** at the bottom of the batch table. Each row runs in sequence, and the log for every row - including the resolved-extent message described above - appears in the **Log** panel, so you can review exactly what each run produced afterward.

A couple of things worth knowing about batch mode specifically: since the extent field can't show a layer name live, the run log's resolved-extent message becomes the main way to confirm each row used the right area - it's worth glancing through the log after a big batch run rather than assuming every row picked up what you intended. Also, because output paths are set per row, double-check your naming pattern before running a large batch - it's much easier to catch a typo in row 1 than after 40 rows have already written files.

## Things to watch out for

- **Column/Row range fields accept any text** - they're not restricted to what's "valid" for the current Letters/Numbers choice, so a typo (e.g. leaving a number in a field set to Letters) will produce an unexpected result rather than an error. Double-check these two fields whenever you switch Column/Row labels between Letters and Numbers.
- **Custom cell size mode ignores "To"** - if you've switched on "Use a custom cell size instead," remember that only each range's "From" value is used; the "To" fields are silently ignored in that mode.
- **Very large grids are capped** - the tool refuses to build a grid with more than 10,000 cells (columns × rows), to avoid accidentally generating an unusably huge output from a typo in cell size or range. If you hit this, the error message tells you the column/row count it calculated - a good clue about which input to fix.
- **The extent field only shows numbers** - see "Reading the run log" above; that's the reliable way to confirm what area was actually used, particularly in batch runs.
- **Margin vs. Inset are different things** - "Margin around extent" pads the whole grid outward before it's built (affecting the grid's own size); "Inset from grid edge" only affects how far the border *labels* sit inside the final grid. Don't mix them up if the grid looks right but the labels seem oddly placed, or vice versa.

## Basic troubleshooting

**"Invalid extent" error** - the Grid extent field is empty or resolved to a zero-size area. Make sure you've actually picked a mode (Canvas/Layer/Draw/Manual) and, if typing coordinates manually, that xmin < xmax and ymin < ymax.

**"Cell width and height must be set" error** - you checked "Use a custom cell size instead" but left Cell width or Cell height blank. Either fill both in, or uncheck the box to go back to column/row-count sizing.

**Too many cells error** - see "Very large grids are capped" above; reduce your range or increase your cell size.

**Labels look overlapping or cramped on a very small or very large extent** - try adjusting Inset from grid edge to a value that suits your specific cell size, rather than relying on the automatic default.

## After running: styling for print

Both output layers are already styled and labeled well enough to preview immediately, but for final print production you'll typically want to:

- Adjust the grid layer's line colour/weight to match your map's overall style (it's a simple outline symbol, easy to restyle like any other layer).
- Adjust the label layer's font, size, and colour via **Layer Properties > Labels**, to match your atlas's typography.
- Add both layers to a Print Layout the same way as any other layer - they behave like normal QGIS layers throughout, so print layout atlases, layout map items, and export to PDF all work as expected.
