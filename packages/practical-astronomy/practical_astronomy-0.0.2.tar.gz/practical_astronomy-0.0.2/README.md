# practical-astronomy-python

Algorithms from "[Practical Astronomy with your Calculator or Spreadsheet](https://www.amazon.com/Practical-Astronomy-your-Calculator-Spreadsheet/dp/1108436072)" by Peter Duffett-Smith, implemented in Python 3.  API documentation is published [here](https://jfcarr-astronomy.github.io/practical-astronomy-python/).

If you're interested in this topic, please buy the book!  It provides far more detail and context.

## CLI

Work is started on a command-line interface, but only the date/time functions are implemented, so far.  Results are formatted as JSON.

Invoke as `./pa-cli.py -h` to see all of the options:

```
$ ./pa-cli.py -h

usage: pa-cli.py [-h] [--cd CD] [--ct CT] [--dh DH] [--gd GD] [--gl GL] [--gst GST] [--lst LST] [--jd JD] [--ut UT] [--year YEAR] [--dst] [--st] [--zc ZC] [--doe] [--cd_to_dn] [--gd_to_jd] [--jd_to_gd] [--ct_to_dh] [--dh_to_ct] [--lct_to_ut] [--ut_to_lct] [--ut_to_gst] [--gst_to_ut] [--gst_to_lst] [--lst_to_gst]

Practical Astronomy CLI.

optional arguments:
  -h, --help    show this help message and exit

Actions:
  --doe         Calculate date of Easter, for a given year.
  --cd_to_dn    Convert civil date to day number.
  --gd_to_jd    Convert Greenwich date to Julian date.
  --jd_to_gd    Convert Julian date to Greenwich date.
  --ct_to_dh    Convert civil time to decimal hours.
  --dh_to_ct    Convert decimal hours to civil time.
  --lct_to_ut   Convert local civil time to universal time.
  --ut_to_lct   Convert universal time to local civil time.
  --ut_to_gst   Convert universal time to Greenwich sidereal time.
  --gst_to_ut   Convert Greenwich sidereal time to universal time.
  --gst_to_lst  Convert Greenwich sidereal time to local sidereal time.
  --lst_to_gst  Convert local sidereal time to Greenwich sidereal time.

Inputs (used by Actions):
  --cd CD       Civil date. Input format: 'mm/dd/yyyy'
  --ct CT       Civil time. Input format: 'hh:mm:ss'
  --dh DH       Decimal hours. Input format: floating point number, e.g., 18.52416667
  --gd GD       Greenwich date. Input format: 'mm/dd/yyyy'. Fractional day is allowed, e.g., '6/19.75/2009'
  --gl GL       Geographical longitude. Input format: (+/-)##.##, e.g., -64.00
  --gst GST     Greenwich sidereal time. Input format: 'hh:mm:ss'
  --lst LST     Local sidereal time. Input format: 'hh:mm:ss'
  --jd JD       Julian date. Input format: floating point number, e.g., 2455002.25
  --ut UT       Universal time. Input format: 'hh:mm:ss'
  --year YEAR   Calendar year, e.g. 2019.

Inputs (time zone management):
  --dst         Observe daylight savings time.
  --st          Observe standard time (default)
  --zc ZC       Offset, in hours, for time zone correction.

```

### Example

Convert universal time to Greenwich sidereal time:

```
$./pa-cli.py --ut_to_gst --ut "14:36:51.67" --gd "4/22/1980"

{"greenwichSiderealTimeHours": 4, "greenwichSiderealTimeMinutes": 40, "greenwichSiderealTimeSeconds": 5.23}
```

## Unit Tests

Unit test run can be invoked via the Make utility:

```
make all
```

## Library Functions

### Date/Time

Type | Description
-----|------------
Calculate | Date of Easter
Convert | Civil Date to Day Number
Convert | Greenwich Date <-> Julian Date
Convert | Julian Date to Day-of-Week
Extract | Day, Month, and Year parts of Julian Date
Convert | Civil Time <-> Decimal Hours
Extract | Hour, Minutes, and Seconds parts of Decimal Hours
Convert | Local Civil Time <-> Universal Time
Convert | Universal Time <-> Greenwich Sidereal Time
Convert | Greenwich Sidereal Time <-> Local Sidereal Time

### Coordinates

Type | Description
-----|------------
Convert | Angle <-> Decimal Degrees
Convert | Right Ascension <-> Hour Angle
Convert | Equatorial Coordinates <-> Horizon Coordinates
Calculate | Obliquity of the Ecliptic
Convert | Ecliptic Coordinates <-> Equatorial Coordinates
Convert | Equatorial Coordinates <-> Galactic Coordinates
Calculate | Angle between two objects
Calculate | Rising and Setting times for an object
Calculate | Precession (corrected coordinates between two epochs)
Calculate | Nutation (in ecliptic longitude and obliquity) for a Greenwich date
Calculate | Effects of aberration for ecliptic coordinates
Calculate | RA and Declination values, corrected for atmospheric refraction and geocentric parallax
Calculate | Heliographic coordinates
Calculate | Carrington rotation number
Calculate | Selenographic (lunar) coordinates (sub-Earth and sub-Solar)

### The Sun

Type | Description
-----|------------
Calculate | Approximate and precise positions of the Sun
Calculate | Sun's distance and angular size
Calculate | Local sunrise and sunset
Calculate | Morning and evening twilight
Calculate | Equation of time
Calculate | Solar elongation

### Planets

Type | Description
-----|------------
Calculate | Approximate and precise position of planet
Calculate | Visual aspects of planet (distance, angular diameter, phase, light time, position angle of bright limb, and apparent magnitude)
Calculate | Position of comet (elliptical and parabolic)
Calculate | Binary star orbit data

### The Moon

Type | Description
-----|------------
Calculate | Approximate and precise position of Moon
Calculate | Moon phase and position angle of bright limb
Calculate | Times of new Moon and full Moon
Calculate | Moon's distance, angular diameter, and horizontal parallax
Calculate | Local moonrise and moonset

### Eclipses

Type | Description
-----|------------
Calculate | Lunar eclipse occurrence and circumstances
Calculate | Solar eclipse occurrence and circumstances
