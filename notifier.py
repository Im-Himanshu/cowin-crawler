# Author: deepak patil
import logging
import traceback
import requests
import time

from tabulate import tabulate
from time import sleep
from datetime import datetime
from IPython.display import clear_output
import webbrowser

class Crawler:
    # base url
    base = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=265&date="

    def __init__(self):
        log.debug("__inside__")

    def start_process(self, date):
        """
        function the data from cowin
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
        result = requests.get("{0}{1}".format(self.base, date), headers=headers)
        if (result.status_code == 200):
            return self.churn(result.json())
        else:
            log.error("Got {} response..".format(result.status_code))
            return []

    def churn(self, data):
        output = []
        for field in data['centers']:
            for session in field['sessions']:
                min_age_limit = session['min_age_limit']
                dose1 = session['available_capacity_dose1']
                if min_age_limit<25 and session['vaccine'] !='COVISHIELD':
                    record = [field['name'],
                              session['available_capacity_dose1'],
                              session['vaccine'],
                              session['min_age_limit'],
                              "{}, {}".format(field['block_name'], field['address'][:15])]
                    output.append(record)
                    if dose1 > 0:
                        #https://selfregistration.cowin.gov.in/appointmentwebbrowser.open_new('https://selfregistration.cowin.gov.in/')
                        webbrowser.open_new('https://selfregistration.cowin.gov.in/appointment')
                        f.write(datetime.today().strftime('%d-%B-%Y %H:%M:%S')+ "Session available : go to the co-win site, now")
                        f.write(tabulate(output, headers=['Name', 'Capacity', 'Vaccine','min_age_limit', 'Address']))
                        print("Session available : go to the co-win site, now")
        return output


def execute(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            traceback.print_exc()
            log.critical("Problem while executing repetitive task.")
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay


def run():
    logging.info("fetching data form cowin for {0}....".format(datetime.today().strftime('%d-%B-%Y %H:%M:%S')))
    date = datetime.today().strftime('%d-%m-%Y')
    output = task.start_process(date)
    if len(output) > 0:
        clear_output(wait=True)
        log.info(tabulate(output, headers=['Name', 'Capacity', 'Vaccine','min_age_limit', 'Address']))
    else:
        log.warning("Not available...")


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
log = logging.getLogger('__name__')
task = Crawler()
logging.info('initialising crawler....')
f = open("loggs.txt", "a")
execute(1, run)