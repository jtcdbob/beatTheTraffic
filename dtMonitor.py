from datetime import datetime
import googlemaps
import os
import sys
import pprint
import time

gmaps = googlemaps.Client(key='AIzaSyAFVgSBQxBxCbnh-IAnnSDLTANUnOi86Tg')

# Request directions via public transit
HOME = "1793 Battersea Ct., San Jose, CA"
WORK = "285 Hamilton Ave, Palo Alto, CA"
MODE = 'driving'
MIN_TO_SEC = 60
TITLE = 'Light Traffic'

# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

# Get current travel time
def getTime(now, isHome):
    if isHome:
        start = HOME;
        end = WORK;
    else:
        start = WORK;
        end = HOME;
    directions_result = gmaps.directions(start, end, MODE, departure_time=now)
    time = directions_result[0]['legs'][0]['duration_in_traffic']['value']
    return time

# Log the data
def logTime(msg):
    print os.path.dirname(os.path.abspath(__file__))
    with open('/Users/bob/Desktop/test.txt', 'a') as file:
        file.write(msg);
        print('Logging done');

def main():
    pp = pprint.PrettyPrinter(depth=6)
    time_print_format = '{:%Y-%m-%d %H:%M:%S}';
    limit_in_min = 36
    start_home_time = 7
    end_home_time = 11
    start_work_time = 16
    end_work_time = 20


    while True:
        try:
            now = datetime.now()
            if (now.hour >= start_home_time) and (now.hour <= end_home_time):
                isHome = True;
            elif (now.hour >= start_work_time) and (now.hour <= end_work_time):
                isHome = False;
            else:
                pp.pprint(now.hour)
                pp.pprint('{0}: No need to travel, check in 20 minutes.'.format(time_print_format.format(now)))
                time.sleep(20 * MIN_TO_SEC) # Recheck in 2 minutes
                continue;
            driving_time = getTime(now, isHome)
            current_time = time_print_format.format(now)
            wait_time = 2
            if driving_time < limit_in_min * MIN_TO_SEC:
                subtitle = '@{0}'.format(str(current_time))
                msg = 'Current driving time to {0} is {1} minutes.'.format('work' if isHome else 'home'
                    , driving_time / 60)
                notify(TITLE, subtitle, msg)
                wait_time = 10
            pp.pprint('{0}: The driving time to {1} is {2} minutes. Check again in {3} minutes.'.format(str(current_time), 'work' if isHome else 'home', str(driving_time / MIN_TO_SEC), wait_time))
            logTime('{0}: The driving time to {1} is {2} minutes. Check again in {3} minutes.'.format(str(current_time), 'work' if isHome else 'home', str(driving_time / MIN_TO_SEC), wait_time))
            time.sleep(wait_time * MIN_TO_SEC) # Check in 2 minutes
        except KeyboardInterrupt:
            sys.exit()

if __name__ == '__main__':
    main()
