# Figure data digitization

Use this procedure when a DataSet value or time series appears only in a plot.
The output is an estimate reconstructed from pixels, not a value reported in a
table. Keep the rendered source image and the exported data together.

## Preferred tool

[WebPlotDigitizer](https://automeris.io/WebPlotDigitizer/) is an optional
computer-vision-assisted tool. It can run in the hosted web application or as a
local desktop build. The Skill does not bundle it or require an account. A
different digitizer is acceptable when it provides equivalent calibration and
export metadata.

## Calibration procedure

1. Render the PDF page at 300-600 DPI. Use the original page, not a cropped
   screenshot, when the caption or legend is needed to identify a series.
2. Load the page or a lossless crop into the digitizer and choose the correct
   plot type: 2D X-Y, bar, scatter, date/time, log X/Y, polar, or another
   explicitly supported type.
3. Calibrate at least two points per linear axis. Use four points when both axes
   are independent. For log axes, mark values on the logarithmic scale and
   record that the axis is logarithmic. Do not treat a log axis as linear.
4. Extract each series separately. Automatic colour extraction may propose
   points, but manually remove legend samples, grid lines, error bars, and
   unrelated series. Use manual clicks when automatic segmentation is
   ambiguous.
5. Export CSV or JSON and inspect a representative set of points against the
   rendered figure. Normalize a CSV export into an auditable series file:

   ```text
   python3 /path/to/simpo-create-dataset/scripts/import_digitized_series.py \
     figure-4b.csv \
     --output figure-4b-S_NH.json --figure "Fig. 4b" --series "S_NH" \
     --x-name "time" --x-unit "d" --y-name "S_NH" --y-unit "mg/L" \
     --uncertainty "approximately one marker width"
   ```

   Resolve `/path/to/simpo-create-dataset` to the installed DataSet Skill
   directory. This helper is shared with `simpo-create-dataset`; the Project
   Skill does not maintain a separate copy.

   Preserve the tool project file when it stores calibration and extraction
   settings.

## Required audit fields

For each imported series, record:

- paper file, page number, figure/panel label, and caption;
- series label and the legend evidence used to identify it;
- x/y names, units, axis type (`linear` or `log`), and the calibration points
  in pixel and data coordinates;
- digitizer name and version or URL, extraction mode, and export filename;
- number of points, any removed points, interpolation or sorting rule, and the
  estimated reading uncertainty;
- whether the values map to `Measured`, `Inflow`, or `Flow`, and the SIMPO
  symbol/name chosen.

Do not interpolate between points unless the user explicitly requests it. Do
not turn a non-detect, blank, or censored value into zero. Retain the original
point order and timestamps where the source provides them.

## Quality gates

Reject or flag a series when any of these is true:

- axis endpoints or tick values cannot be read;
- the figure is too low-resolution to distinguish the markers or lines;
- multiple series overlap and cannot be assigned confidently;
- the legend is absent or a panel label is ambiguous;
- the plot uses a transformation that the selected digitizer cannot represent.

For a flagged series, keep it in the evidence map as unresolved and ask the
user whether to provide a better figure, supplementary table, or an approved
approximation. A visually plausible curve is not sufficient evidence.

## DataSet mapping

- Time or observation curves at a tank or sampling point normally become a
  `Measured` block.
- Influent or dosing curves become an `Inflow` block only when the source gives
  the influent identity and target basis.
- Hydraulic curves become a `Flow` block only when the flow unit and stream
  identity are established.

Keep digitized estimates separate from directly reported table values in the
Markdown audit passed to `simpo create-dataset`.
