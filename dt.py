from datetime import date, datetime
import time

def begin_date(ts):
	begindate = datetime.utcfromtimestamp(ts)
	return ts - begindate.hour*3600 - begindate.minute*60 - begindate.second

def date_time(ts_date, ts_time):
	return ts_date + ts_time

def htime(ts):
	return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def time_to_sec(strTime):
	ftr = [3600,60,1]
	return sum([a*b for a,b in zip(ftr, map(int,strTime.split(':')))])

def sec_to_time(sec):
	return '' + "{:0>2d}".format(sec / 3600) + ':' + "{:0>2d}".format(sec%3600/60)