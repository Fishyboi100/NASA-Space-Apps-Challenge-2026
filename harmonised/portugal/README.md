# Ember harmonised fire record: Portugal, mainland

NASA Space Apps Challenge 2026 · Harmonization of MODIS and VIIRS Hot Spots

Source: NASA FIRMS active fire detections (MODIS C6.1 Terra and Aqua; VIIRS 375 m S-NPP, NOAA-20, NOAA-21),
the FIRMS country file for Portugal, keeping mainland Portugal (the Azores and Madeira left out). Standard-processing archive plus near-real-time data for the latest months, Nov 2000 to Nov 2026.
Mediterranean climate: the main season peaks in August, with extreme years in 2003, 2005, 2017 and 2025.

The method is the same as for California (see the main README in `harmonised/README.md`): satellite outages
excluded, static industrial sources removed, every satellite calibrated to MODIS Aqua per day/night pass and
calendar month on days both observed the region, then the satellites observing each day averaged.
Default settings: nominal and high confidence, static sources excluded, common-fire floor 10 MW.

## Files
- `ember_portugal_daily_grid_0.1deg.csv`: harmonised hotspots and fire power per 0.1° cell (about 10 km) per day, with
  each satellite's raw detection count. Columns as in the California grid.
- `ember_portugal_daily_region.csv`: every day for the whole region (harmonised and as detected).
- `ember_portugal_monthly_region.csv`: monthly totals with the median and average of the same calendar month and the ratio to the median.
- `calibration_factors.csv`: factor per satellite, pass and calendar month.
- `satellite_outages.csv`: 32 outage periods found and excluded.

The grid sums match the app's whole-region record to within 0.04 hotspots per day.

## Months furthest above their usual level (among the busier months)
| Month | Harmonised hotspots | × median of that month |
|---|---|---|
| 2007-11 | 385 | 18.9× |
| 2017-06 | 265 | 17.5× |
| 2017-10 | 929 | 16.6× |
| 2024-09 | 1,360 | 16.0× |
| 2022-01 | 144 | 12.7× |
| 2011-10 | 707 | 12.6× |

## Limitations
Hotspots are fires seen at overpass time, not burned area; clouds and smoke hide fires; before July 2002
only MODIS Terra observed, so those months have no cross-check between satellites.
