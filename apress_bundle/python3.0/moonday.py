#! /usr/bin/env python

"""
Weekday and Moonphase calculator

Target System: GNU/Linux
Interface: Command-line
Functional Requirements: Given a numerical date of the form yyyy-mm-dd,
 work out what day of the week it is and what phase the moon would be in.
Test values: '1957-01-01', '1995-01-01', '1999-01-24',
			 '2008-09-15', '2011-10-20'
Expected results: Tues new (1), Sun new (1), Sun waxing half (5),
 Mon full (14), Thurs waning half (17)
 (Numbers in parentheses are expected golden or metonic_year values)
Limitations: This only works for dates using the Gregorian calendar
	i.e. > 1752 in Britain & British colonies,
		> 1582 in western Europe & European colonies,
		> 1867 in Russia, > 1873 in Japan and > 1949 in China
"""
__version__ = 0.1
__maintainer__ = "maintainer@website.com"
__status__ = "Prototype"

# set up constant data.
# These can all be tuples as we won't need to modify them.
days_per_month = (31,28,31,30,31,30,31,31,30,31,30,31)
day_names = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
			'Saturday', 'Sunday')
month_names = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 
			'Sept', 'Oct', 'Nov', 'Dec')
moon_phases = ('new', 'waxing crescent', 'waxing half', 'waxing gibbous',
			'full', 'waning gibbous', 'waning half', 'waning crescent')
test_dates = ('1957-01-01', '1995-01-01', '1999-01-24',
			 '2008-09-15', '2011-10-20')
expected = ('Tues new (1)', 'Sun new (1)', 'Sun waxing half (5)',
 			'Mon full (14)', 'Thurs waning half (17)')
moon_cycle = 29.53

print() 
for di, date in enumerate(test_dates):
	# Reset day_of_year counter.
	day_of_year = 0
	
	# Split date into month, day and year parts.
	year, month, day = date.split("-",2)
	month = int(month)
	day = int(day)
	year = int(year)

	# check values are sane
	if month < 1 or month >= 13:
		print("warning: month out of range:", month)
	if day < 1 or day > 31:
		print("warning: day out of range:", day)
	
	# Calculate what century it is
	century = (year / 100) + 1
	
	# Work out what day of the year it is
	for days in days_per_month[:int(month -1)]:
		day_of_year += days
	day_of_year += int(day)	
	
	# Check values are still sane.
	if day_of_year < 1 or day_of_year > 365:
		print("warning: day_of_year", day_of_year)
		
	# work out The age of the moon at Jan 1st
	# using the Epact formula, which is used to calculate Easter.
	metonic_year = (year % 19) + 1
	gregorian_adj = (3 * century) / 4 - 12
	clavian_adj = (8 * century + 5) / 5 - 5 - gregorian_adj
	moon_age = (11 * metonic_year + 20 + clavian_adj) % 30
	if moon_age == 24:
		moon_age += 1
	elif moon_age == 25 and gregorian_adj > 11:
		moon_age +=1
	else:
		pass
	# Add the number of days passed in the year
	# and modulo by the length of moon_cycle
	# to get the number of days into the cycle.
	moon_day = (moon_age + day_of_year + 5) % moon_cycle
	# Validate moon_day
	if moon_day < 1 or moon_day > 29:
		print("warning: moon_day out of range:", moon_day)
	# Figure out what phase the moon is in
	phase = moon_day / 4
	
	# calculate weekday using Zeller's algorithm
	# Rearrange the year to run from Mar - Feb
	# moving Jan / Feb into previous year
	year_mod = (14 - month) / 12
	mod_year = year - year_mod
	mod_month = month + ( 12 * year_mod) - 2
	
	days_in_year = int(mod_year * 1.25)
	days_in_month = ((31 * mod_month) / 12)
	
	weekday = (day + days_in_year - (mod_year / 100) + (mod_year / 400)
					 + days_in_month) % 7

	# Print out the result
	print(day_names[int(weekday -1)], month_names[int(month -1)], int(day), end=' ') 
	print('-', moon_phases[int(phase)], 'moon (', int(metonic_year), ')')
	print('\t[x:', expected[di], ':x]')
print() 
 

