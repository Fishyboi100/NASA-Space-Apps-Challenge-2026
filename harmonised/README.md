# Ember harmonised hotspot dataset: California, Nov 2000 to Nov 2026

NASA Space Apps Challenge 2026 · *Harmonization of MODIS and VIIRS Hot Spots* · Ember team, Sugar Land, TX

One consistent record of satellite fire hotspots for California (state boundary plus a 15 km buffer),
built from 2,202,586 NASA FIRMS active fire detections from five satellites. MODIS (Terra since
Nov 2000, Aqua since Jul 2002) and VIIRS (S-NPP since Jan 2012, NOAA-20 since Apr 2018, NOAA-21 since
Mar 2023) see fire differently; here every value is on one scale, so the satellite a detection came from
no longer matters.

**Units: MODIS Aqua-equivalent.** A harmonised value of 10 hotspots means "about what MODIS Aqua alone
would have detected". It is not a count of separate fires: one large fire produces many hotspots.

## Files

| File | Rows | What it holds |
|---|---|---|
| `ember_california_daily_grid_0.1deg.csv` | 160,709 | Harmonised hotspots and fire power per day per 0.1° cell (about 10 km); only cell-days with at least one detection |
| `ember_california_daily_statewide.csv` | 9,510 | Every day, whole area: harmonised and as-detected values |
| `ember_california_monthly_statewide.csv` | 313 | Every month, with the median and average of the same calendar month and the ratio to the median |
| `calibration_factors.csv` | 120 | The scale factor applied to each satellite, pass (day/night) and calendar month |
| `satellite_outages.csv` | 42 | Days each satellite was off-line; those days are excluded for that satellite |

## Columns

**Daily grid:** `date` (UTC) · `cell_lat`, `cell_lon` (cell centre, degrees) · `hotspots_harmonised` ·
`frp_mw_harmonised` (fire radiative power from fires of at least 10 MW, MW, summed over passes) ·
`satellites_observing` (satellites whose detections were averaged that day) · `detections_terra`,
`detections_aqua`, `detections_snpp`, `detections_noaa20`, `detections_noaa21` (raw detections, as reported).
A cell-day missing from the file had no detections: its harmonised value is 0.

**Statewide daily:** `date` · `hotspots_harmonised` · `frp_mw_harmonised` · `hotspots_as_detected` and
`frp_mw_as_detected` (all satellites simply added, no correction) · `satellites_observing`.
Summing the grid over cells gives the statewide harmonised values.

**Statewide monthly:** `month` · `days_observed` · `days_in_month` · harmonised and as-detected totals ·
`complete` · `median_same_month`, `average_same_month` (over complete months of every year) · `ratio_to_median`.

## Method

1. **Clean.** Keep detections of nominal or high confidence. Drop fixed heat sources (FIRMS type 1 to 3:
   volcanoes, industry, offshore); in the near-real-time rows, which have no type, drop detections in the
   ~1 km cells the archive marks as fixed sources. Find satellite outages (a satellite reports nothing while
   its partner says it should have seen at least 20 hotspots) and exclude those days for that satellite.
2. **Calibrate.** Scale each satellite to MODIS Aqua (an afternoon sensor with a long record), separately
   for day and night passes and for each calendar month, from the ratio of totals on days both observed
   California. Hotspot factors use all detections; fire power factors use fires of at least 10 MW, which
   both instruments can see. Months with few reference detections lean on the all-year factor.
3. **Combine.** A day's harmonised value is the average of the calibrated satellites observing that day,
   so a fire seen by five satellites is counted once.

## Does it work?

When VIIRS S-NPP arrived in 2012, the as-detected record jumped **+430%** relative to MODIS Aqua alone
(3 years after vs 3 before). The harmonised record moved **−1%**.

Held-out check (factors fitted on even years only, tested on odd-year monthly totals against MODIS Aqua):

| Satellite | Monthly error before | After | Months tested |
|---|---|---|---|
| MODIS Terra | 18% | 16% | 143 |
| VIIRS S-NPP | 618% | 13% | 84 |
| VIIRS NOAA-20 | 614% | 11% | 48 |
| VIIRS NOAA-21 | 642% | 15% | 22 |

Months furthest above their usual level (harmonised hotspots vs the median of the same month):

| Month | Hotspots | Usual | Ratio |
|---|---|---|---|
| 2020-09 | 13,083 | 662 | 19.8× |
| 2008-06 | 2,499 | 154 | 16.2× |
| 2008-07 | 4,442 | 357 | 12.4× |
| 2021-08 | 10,715 | 973 | 11.0× |
| 2017-12 | 1,234 | 121 | 10.2× |

## Limitations

- A hotspot is a hot pixel, not a confirmed wildfire, and its location is the pixel centre.
- Clouds and smoke hide fires; FIRMS hotspot files carry no cloud mask.
- Fire power is a snapshot at overpass time; its calibration is less reliable than the hotspot calibration.
- The latest months come from near-real-time processing, which NASA later replaces with standard processing.
- This is the team's own estimate, not an official NASA product.

## Source and licence

NASA FIRMS (https://firms.modaps.eosdis.nasa.gov/): MODIS Collection 6.1 and VIIRS 375 m Collection 2 active
fire detections, archive download of 2026-11-14 (standard processing, plus near-real-time
for the latest months). NASA data are free to use; please credit NASA FIRMS. Code written with help from
Claude (Anthropic).

## Validation against CAL FIRE acres burned (`calfire_validation.csv`)

Yearly statewide hotspots compared with CAL FIRE's official acres burned in California, all jurisdictions, 2003–2025 (2003–2018: "California Wildfires and Acres for all Jurisdictions"; 2019–2025: the CAL FIRE incident archive page for each year).

| | As detected | Harmonised |
|---|---|---|
| Correlation with acres (log scale) | 0.67 | **0.96** |
| Rank correlation | 0.61 | **0.98** |
| Hotspots per 1,000 acres, 2003–2011 → 2012–2025 | 12.2 → 108.4 (8.9×) | 6.2 → 6.2 (1.00×) |

As detected, the same acre of burning produces about 9 times more hotspots after VIIRS arrived; harmonised, the relation is unchanged, so a change in the record reflects a change in fire.

## Uncertainty

The app also shows the range of totals obtained from each satellite alone after calibration. Statewide, a typical year's range is within ±4% of the harmonised value.

## Other regions: Texas, Chile, Portugal, Greece (`texas/`, `chile/`, `portugal/`, `greece/`)

The same method, with no changes, applied to our home state Texas (FIRMS US state download) and to three more
Mediterranean-climate regions from the FIRMS country files (Chile and Portugal mainland; Greece including the islands). Each folder has the daily 0.1° grid, whole-region
daily and monthly series, calibration factors, satellite outages and its own README.

| Region | Jump when VIIRS S-NPP joined (2012), as detected | Harmonised | Usual peak month | Busiest month on record |
|---|---|---|---|---|
| California | +430% | −1% | Aug | Sep 2020 (19.8× usual) |
| Texas | +403% | +16% | Mar | Apr 2011 (8.3× usual) |
| Chile | +328% | −4% | Mar | Jan 2017 (25.1× usual) |
| Portugal | +251% | −3% | Aug | Aug 2005 (8.9× usual) |
| Greece | +372% | +6% | Oct | Aug 2007 (11.9× usual) |

Jump: the yearly total relative to MODIS Aqua alone, three years after VIIRS joined against three years before.

## Data check
Every detection in the original FIRMS files is in the app's data, verified record by record (date, time, satellite,
day/night, confidence, source type, and position and fire power within the packing precision of under 35 m and 0.01%):
California 2,202,586; Texas 1,455,087; Chile 959,901 (567 Easter Island and Juan Fernández detections left out);
Portugal 273,900 (4,967 Azores and Madeira detections left out); Greece 217,519.
