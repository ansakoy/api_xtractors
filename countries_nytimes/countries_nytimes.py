# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import requests
import time

from APIXtractors.extractor import Extractor

# FIELDS
YEAR = 'year'
COUNTRY = 'country'
NUM_OCCURRENCES = 'num occurrences'


class NewYorkTimes(Extractor):

    def __init__(self, fname='data/nyt_countries', key=None):
        Extractor.__init__(self, fname)
        self.csv_output = fname
        self.csv_writer = None
        try:
            # If text file with API key already exists, load the key
            self.key = self.get_key()
        except IOError:
            # If there is no file with API key
            if key:
                # Write the given key to text file and then load it
                self.write_api_key_to_file(key)
                self.key = self.get_key()
            else:
                # If there is no file and no key provided, announce it
                print 'GIVE ME AN ADEQUATE KEY!'
                return
        self.reference = self.load_countries()
        self.url_base = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?' \
                        'q={}&facet_field=source&facet_filter=true&begin_date={}0101&end_date={}1231&api-key={}'

    def load_countries(self):
        # Load requests for countries from JSON file
        with open('countries_nyt_requests.json') as reference:
            return json.load(reference)

    def write_api_key_to_file(self, key):
        # Write API key to a text file for further use
        with open('nyt_api_key.txt', 'wb') as handler:
            handler.write(key)

    def get_key(self):
        # Get API key from text file
        with open('nyt_api_key.txt', 'r') as handler:
            return handler.read()

    def collect_data(self, begin_year, end_year):
        # Collect data from NY Times API for a given period
        csv_headers = [YEAR, COUNTRY, NUM_OCCURRENCES]
        self.filename += str(begin_year) + '-' + str(end_year)
        self.start_csv(csv_headers)
        for year in xrange(begin_year, end_year + 1):
            print year
            for country in self.reference:
                query = self.url_base.format(self.reference[country],
                                             year,
                                             year,
                                             self.key)
                try:
                    req = requests.get(query).json()
                    source = req.get('response', {}).get('facets', {}).get('source', {}).get('terms')
                    if source:
                        for entry in source:
                            if entry['term'] == 'The New York Times':
                                data = {YEAR: year,
                                        COUNTRY: country,
                                        NUM_OCCURRENCES: entry['count']}
                                self.to_csv(csv_headers, data)
                except Exception as e:
                    print e
                    print query
                time.sleep(1)

        self.stop_csv()
        print 'DONE'


if __name__ == '__main__':
    # pass
    nyt = NewYorkTimes()
    nyt.collect_data(2017, 2017)