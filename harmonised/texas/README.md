# Ember Sync harmonised fire record: Texas

NASA Space Apps Challenge 2026 · Harmonization of MODIS and VIIRS Hot Spots

Source: NASA FIRMS active fire detections (MODIS C6.1 Terra and Aqua; VIIRS 375 m S-NPP, NOAA-20, NOAA-21),
from the FIRMS archive download for the US state of Texas. Standard-processing archive plus near-real-time data
for the latest months, Nov 2000 to Nov 14, 2026: 1,455,087 detections.

Our home state. Texas burns most from January to May, when dry grass and strong winds meet. Agricultural burning
is common, so statewide totals are dominated by many small fires; single large wildfires stand out best in a
smaller area. In the Panhandle (101.7°W to 99.95°W, 35.3°N to 36.55°N) the app ranks 25 Feb to 8 Mar 2024 first
(the Smokehouse Creek Fire, the largest wildfire in Texas history; February 2024 was 68 times a usual February there)
and March 2006 second (the East Amarillo Complex, the record it broke). Statewide, the record year is 2011.

The method is the same as for California (see the main README in `harmonised/README.md`).
Default settings: nominal and high confidence, static sources excluded, common-fire floor 10 MW.

## Files
- `ember_texas_daily_grid_0.1deg.csv`: harmonised hotspots and fire power per 0.1° cell (about 10 km) per day, with
  each satellite's raw detection count. Columns as in the California grid.
- `ember_texas_daily_region.csv`: every day for the whole state (harmonised and as detected).
- `ember_texas_monthly_region.csv`: monthly totals with the median and average of the same calendar month and the ratio to the median.
- `calibration_factors.csv`: factor per satellite, pass and calendar month.
- `satellite_outages.csv`: 57 outage periods found and excluded.

The grid sums match the app's whole-state record to within 0.05 hotspots per day.

## The instrument step
When VIIRS S-NPP joined in 2012 the yearly count jumped +403% against MODIS Aqua alone; harmonised, +16%.
That is larger than in the other regions (within ±6%): the record year 2011 falls just before VIIRS, and big
wildfires and small farm fires do not scale between the two instruments in quite the same way. In the
Panhandle alone the step is +1%.

## Limitations
Hotspots are fires seen at overpass time, not burned area; clouds and smoke hide fires; agricultural burning is
counted; before July 2002 only MODIS Terra observed. The Smokehouse Creek Fire also burned into Oklahoma, which
is outside this download.
