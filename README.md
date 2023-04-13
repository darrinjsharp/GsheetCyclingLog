# GsheetCyclingLog

Program to upload daily rides to a Gsheet. This project also tracks the season totals for mile and time ridden.

usage: main.py [-h] --date DATE --route ROUTE --time TIME [--miles MILES]

options:
  -h, --help     show this help message and exit

Required Arguments:
  --date DATE    MM/DD/YYYY
  --route ROUTE  "route description"
  --time TIME    fractional hours, e.g. 2.4 (= 2h 24m)

Optional Arguments:
  --miles MILES  integer miles
