from datetime import datetime
import googlemaps
import os
import sys
import pprint
import time

class Clock:
	MIN_TO_SEC = 60;
	TIME_FORMAT = '{:%Y-%m-%d %H:%M:%S}';
	now = None;
	def __init__(self):
		self.now = datetime.now()
	def get(self):
		self.now = datetime.now()
		return self.now
	def show(self):
		print(self.TIME_FORMAT.format(self.now));

class Prophet:
	clock = Clock()
	googlemap = None
	def __init__(self):
		self.googlemap = googlemaps.Client(key='AIzaSyAFVgSBQxBxCbnh-IAnnSDLTANUnOi86Tg')

	def consult(self, traveler):
		self.clock.show()
		directions_result = self.googlemap.directions(traveler.home, traveler.work, traveler.mode, departure_time=self.clock.get())
		time_in_sec = directions_result[0]['legs'][0]['duration_in_traffic']['value']
		return {'time':self.clock.now,
				'duration':time_in_sec/self.clock.MIN_TO_SEC}


class Traveler:
	home = None;
	work = None;
	mode = None;
	info = None;
	def __init__(self, info):
		self.home = info['home'];
		self.work = info['work'];
		self.mode = info['mode'];
		self.info = info;





def main():
	p = Prophet();

	p1_info = { 'home':'1793 Battersea Ct., San Jose, CA',
				'work':'285 Hamilton Ave, Palo Alto, CA',
				'mode':'driving',
				'limit' : 36,
				'start_home':7,
				'end_home':11,
				'start_work':16,
				'end_work':20};
	t = Traveler(p1_info)
	print p.consult(t);
#-------------------------------
if __name__ == "__main__":
    main()