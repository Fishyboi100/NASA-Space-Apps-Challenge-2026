# Ember Sync: burning activity calendar

NASA Space Apps Challenge 2026 · *Harmonization of MODIS and VIIRS Hot Spots* · team from Sugar Land, TX

Ember harmonises two decades of NASA FIRMS active-fire hotspots (MODIS since 2000, VIIRS since 2012)
into one consistent record, so the sensor of origin no longer matters. Pick an area (draw it or type
coordinates) and dates to see a month-by-year burning calendar, how the current month compares with
the historical median and average, unusual periods, and the fire season, then download the hotspots
and summaries as CSV or images.

## Highlights
- **Checked against the ground:** harmonised yearly hotspots match CAL FIRE's official acres burned
  (2003–2025) with a correlation of 0.96, against 0.67 as detected. Hotspots per 1,000 acres stay at 6.2
  before and after VIIRS; as detected they jump 8.9×. (`harmonised/calfire_validation.csv`)
- **Early warning:** this fire season's running total against every past year to the same date, with
  percentile bands and an above/well-above-normal flag. The fire year starts at the quietest month, so it
  works in either hemisphere.
- **Uncertainty shown:** whiskers and ranges give the total each satellite would give on its own after
  calibration (typically within ±4% statewide).
- **Five regions built in:** California, our home state Texas, Chile, Portugal and Greece (three
  continents, Chile's season mirrored), each with a harmonised dataset in `harmonised/<region>/`, plus an
  **Around the world** tab comparing their seasons and instrument jumps.
- **Shareable links:** the address keeps the region, area, dates, view, tab and language
  (e.g. `#calendar&a=-122.2,39.4,-121.2,40.2&d=2018-11-01,2018-11-30` opens Paradise in Nov 2018).
- **Area report:** a printable one-page fire history for any area and dates (print or save as PDF).
- **Languages:** interface labels in English, Spanish, Portuguese and Greek.
- **Accessibility:** a table behind every chart, keyboard navigation, skip link, colour-blind-safe palette.
- **60-second guided tour:** the ▶ button walks through the problem, the fix, the proof and the findings.

## Files
- `index.html`: the overview page (the story, method, proof and five regions), linking to the app
- `methods.html`: the full method, validation, uncertainty and limitations, written as a short paper
- `assets/`: images used by the overview and methods pages
- `app.html`: the whole app (no build step, no server code). Tabs: Calendar, Unusual periods,
  Fire season & trends, Data, How it works; each has its own link (`#calendar`, `#unusual`, `#season`, `#data`, `#method`)
- `harmonised/`: **the harmonised California dataset**: daily 0.1° grid (160,709 cell-days), statewide daily
  and monthly series, calibration factors, satellite outages, and a README with every column and the validation
- `data/<region>.b64.txt`: the original FIRMS detections the app loads (gzip, base64): California 2.2 million,
  Texas 1.46 million, Chile 960,000, Portugal 274,000, Greece 218,000; every record checked against the original
  FIRMS files by `tools/verify_regions.py`
- `tools/prepare_data.py`: rebuilds the California data file from FIRMS CSV downloads; `tools/build_regions.py` the other three

## Run it
Any static web host works, e.g. GitHub Pages: Settings → Pages → Deploy from branch → `main` / root.
Opening `app.html` straight from disk can't load the data file (browsers block it); the app then
shows a simulated sample.

## Any other region
Request MODIS and VIIRS data for any area from the FIRMS archive download tool
(https://firms.modaps.eosdis.nasa.gov/download/), then drop the .zip files FIRMS emails you onto
the app. It unzips them in the browser, finds satellite outages, calibrates and builds the calendar.

## Method (short)
1. Find satellite outages and exclude them; flag fixed industrial heat sources.
2. Count hotspots (and sum fire radiative power) per satellite, day and day/night pass.
3. Scale every satellite to MODIS Aqua, per pass and calendar month, from days both observed the area.
4. Average the calibrated satellites so each fire counts once.
5. Compare months and days with the same period in other years (median, average, robust deviation).

On California data the instrument jump when VIIRS arrived in 2012 goes from +430% (as detected) to
about −1% (harmonised), measured against MODIS Aqua alone. The harmonisation is the team's own
estimate, not an official NASA product.

## Data
NASA FIRMS: MODIS Collection 6.1 and VIIRS 375 m (S-NPP, NOAA-20, NOAA-21) active fire detections.
https://firms.modaps.eosdis.nasa.gov/

Map outlines: Natural Earth 1:50m land and country borders (via the world-atlas package) and US state
borders (US Census, via the us-atlas package); both public domain.

## AI and tools
Code written with help from Claude (Anthropic); the team designed, tested and explained it.
