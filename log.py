#!/opt/homebrew/bin/python3

from typing import List
import argparse
import gspread
from datetime import date
import json
import sys

SEASONTIMECELL = "F3"
SEASONMILESCELL = "G3"

DATECOL = "A"
ROUTECOL = "B"
TIMECOL = "C"
MILESCOL = "D"

SHEETNAME = "cycling_log"
YEAR = "2023"

"""
Interactive program to ingest one day's ride data, upload
it to a Gsheet, and calculate season totals for
miles and time.
"""

def get_worksheet():
	"""
	Get the specs for the sheet, which includes all the tabs/
	worksheets, and the individual worksheet.
	"""
	
	gc = gspread.service_account(filename='cycling_log.json')
	sheet = gc.open(SHEETNAME)
	worksheet = sheet.worksheet(YEAR)

	return worksheet


def _get_args(args: List[str]):
	"""
	Parse the input arguments.
	"""

	parser = argparse.ArgumentParser()
	required = parser.add_argument_group("Required Arguments")
	optional = parser.add_argument_group("Optional Arguments")

	required.add_argument(
		"--date",
		help="MM/DD/YYYY",
		required=True,
		type=str, 
	)

	required.add_argument(
		"--route",
		help="\"route description\"",
		required=True,
		type=str, 
	)

	required.add_argument(
		"--time",
		help="fractional hours, e.g. 2.4 (= 2h 24m)",
		required=True,
		type=float, 
	)

	# miles is optional, e.g. in the case of an
	# indoor trainer ride.
	optional.add_argument(
		"--miles",
		help="integer miles",
		required=False,
		type=int, 
	)

	return parser.parse_args(args)


def upload_ride(args, worksheet):
	"""
	Upload a single day's ride to the Google Sheet Worksheet/Tab.
	"""

	print(f"\nUploading Date = {args.date}, Route = {args.route}, Time = {args.time}, Miles = {args.miles}\n")

	# Find the first blank row; cells in this blank row will be updated.
	first_free = len(worksheet.get_all_values())+1
	
	# Update the ride data for a single day.
	worksheet.update_acell(f"{DATECOL}{first_free}", args.date)
	worksheet.update_acell(f"{ROUTECOL}{first_free}", args.route)
	worksheet.update_acell(f"{TIMECOL}{first_free}", args.time)
	worksheet.update_acell(f"{MILESCOL}{first_free}", args.miles)

	return


def season_totals(miles, time, worksheet):
	"""
	Update the season total for miles and time ridden.
	"""

	# If no miles were ridden for a day, the miles variable will
	# be of None type. In this case, do not try and update the total.
	if miles is not None:
		miles = int(worksheet.acell(SEASONMILESCELL).value) + int(miles)
		worksheet.update(SEASONMILESCELL, miles)

	time = float(worksheet.acell(SEASONTIMECELL).value) + float(time)
	worksheet.update(SEASONTIMECELL, time)

	return


def main():
	
	args = _get_args(sys.argv[1:])
	worksheet = get_worksheet()
	upload_ride(args, worksheet)
	season_totals(args.miles, args.time, worksheet)


if __name__=="__main__":
	main()
