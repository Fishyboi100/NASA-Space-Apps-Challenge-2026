# Ember harmonised fire record: Greece

NASA Space Apps Challenge 2026 · Harmonization of MODIS and VIIRS Hot Spots

Source: NASA FIRMS active fire detections (MODIS C6.1 Terra and Aqua; VIIRS 375 m S-NPP, NOAA-20, NOAA-21),
the FIRMS country file for Greece, islands included. Standard-processing archive plus near-real-time data for the latest months, Nov 2000 to Nov 2026.
Mediterranean climate: the main season runs from July into autumn.

The method is the same as for California (see the main README in `harmonised/README.md`): satellite outages
excluded, static industrial sources removed, every satellite calibrated to MODIS Aqua per day/night pass and
calendar month on days both observed the region, then the satellites observing each day averaged.
Default settings: nominal and high confidence, static sources excluded, common-fire floor 10 MW.

## Files
- `ember_greece_daily_grid_0.1deg.csv`: harmonised hotspots and fire power per 0.1° cell (about 10 km) per day, with
  each satellite's raw detection count. Columns as in the California grid.
- `ember_greece_daily_region.csv`: every day for the whole region (harmonised and as detected).
- `ember_greece_monthly_region.csv`: monthly totals with the median and average of the same calendar month and the ratio to the median.
- `calibration_factors.csv`: factor per satellite, pass and calendar month.
- `satellite_outages.csv`: 31 outage periods found and excluded.

The grid sums match the app's whole-region record to within 0.04 hotspots per day.

## Months furthest above their usual level (among the busier months)
| Month | Harmonised hotspots | × median of that month |
|---|---|---|
| 2007-08 | 1,570 | 11.9× |
| 2007-06 | 164 | 9.1× |
| 2001-10 | 1,254 | 8.1× |
| 2021-08 | 890 | 6.8× |
| 2023-08 | 855 | 6.5× |
| 2001-09 | 454 | 5.9× |

## Limitations
Hotspots are fires seen at overpass time, not burned area; clouds and smoke hide fires; before July 2002
only MODIS Terra observed, so those months have no cross-check between satellites.
