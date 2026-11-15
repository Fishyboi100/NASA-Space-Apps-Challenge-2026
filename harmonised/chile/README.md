# Ember harmonised fire record: Chile, mainland

NASA Space Apps Challenge 2026 · Harmonization of MODIS and VIIRS Hot Spots

Source: NASA FIRMS active fire detections (MODIS C6.1 Terra and Aqua; VIIRS 375 m S-NPP, NOAA-20, NOAA-21),
the FIRMS country file for Chile, keeping longitudes east of 76°W (Easter Island and the Juan Fernández Islands left out). Standard-processing archive plus near-real-time data for the latest months, Nov 2000 to Nov 2026.
Southern Hemisphere: the fire year runs from the quiet southern winter, and the main season peaks from January to March.

The method is the same as for California (see the main README in `harmonised/README.md`): satellite outages
excluded, static industrial sources removed, every satellite calibrated to MODIS Aqua per day/night pass and
calendar month on days both observed the region, then the satellites observing each day averaged.
Default settings: nominal and high confidence, static sources excluded, common-fire floor 10 MW.

## Files
- `ember_chile_daily_grid_0.1deg.csv`: harmonised hotspots and fire power per 0.1° cell (about 10 km) per day, with
  each satellite's raw detection count. Columns as in the California grid.
- `ember_chile_daily_region.csv`: every day for the whole region (harmonised and as detected).
- `ember_chile_monthly_region.csv`: monthly totals with the median and average of the same calendar month and the ratio to the median.
- `calibration_factors.csv`: factor per satellite, pass and calendar month.
- `satellite_outages.csv`: 59 outage periods found and excluded.

The grid sums match the app's whole-region record to within 0.04 hotspots per day.

## Months furthest above their usual level (among the busier months)
| Month | Harmonised hotspots | × median of that month |
|---|---|---|
| 2017-01 | 5,399 | 25.1× |
| 2023-02 | 4,859 | 19.2× |
| 2014-01 | 917 | 4.3× |
| 2022-12 | 502 | 4.0× |
| 2015-02 | 900 | 3.5× |
| 2022-02 | 845 | 3.3× |

## Limitations
Hotspots are fires seen at overpass time, not burned area; clouds and smoke hide fires; before July 2002
only MODIS Terra observed, so those months have no cross-check between satellites.
