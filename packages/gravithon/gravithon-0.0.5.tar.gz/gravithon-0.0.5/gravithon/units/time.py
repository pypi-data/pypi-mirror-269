from gravithon.units.prefixes import *

# MKS units
s = sec = second = 1

min = minute = 60 * second
h = hr = hour = 60 * minute
d = day = 24 * hour
# This is 365 days. For astronomical year use gravithon.Earth.orbital_period()
year_of_days = 365 * day

ms = millisecond = milli * second
μs = microsecond = micro * second
ns = nanosecond = nano * second
