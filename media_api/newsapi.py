# -*- coding: utf-8 -*-

import json
from APIXtractors.extractor import Extractor
import requests


class NewsAPIxtractor(Extractor):

    def __init__(self, fname='data/No_name'):
        Extractor.__init__(self, fname)
        self.media = self.load_media_lst()
        self.key = self.load_key()
        self.url_base = 'https://newsapi.org/v1/articles?source={}&sortBy=top&apiKey=' + self.key
        self.all_fname = 'data/all_top.txt'
        self.selected_fname = 'data/selected_top.txt'
        self.txt_all = None
        self.txt_selected = None
        self.selected_media = ["the-wall-street-journal",
                               "the-economist",
                               "bloomberg"]

    def load_key(self, key=None):
        try:
            with open('newsapi_key.txt', 'r') as my_key:
                return my_key.read()
        except IOError:
            if key:
                with open('newsapi_key.txt', 'wb') as fhandler:
                    fhandler.write(key)
                with open('newsapi_key.txt', 'r') as my_key:
                    return my_key.read()
            else:
                print "GIVE ME NORMAL NEWSAPI KEY!"
                return

    def load_media_lst(self):
        with open('media.json') as fhandler:
            return json.load(fhandler)

    def walk_through(self):
        self.txt_all = open(self.all_fname, 'wb')
        self.txt_selected = open(self.selected_fname, 'wb')
        for entry in self.media:
            print entry, entry in self.selected_media
            api_url = self.url_base.format(entry)
            print api_url
            self.collect_data(api_url, entry)
        self.txt_all.close()
        self.txt_selected.close()
        print 'DONE'

    def collect_data(self, url, src):
        response = requests.get(url).json()
        source = (response['source'] + u'\n').encode('utf-8')
        self.txt_all.write(source)
        if src in self.selected_media:
            self.txt_selected.write(source)
        articles = response['articles']
        for article in articles:
            url = (article.get('url', u'No url') + u'\n').encode('utf-8')
            title = (article.get('title', u'No title') + u'\n').encode('utf-8')
            try:
                description = (article.get('description', u'No description') + u'\n\n').encode('utf-8')
            except TypeError:
                description = 'No description\n\n'
            self.txt_all.write(url)
            self.txt_all.write(title)
            self.txt_all.write(description)
            if src in self.selected_media:
                self.txt_selected.write(url)
                self.txt_selected.write(title)
                self.txt_selected.write(description)

if __name__ == '__main__':
    surfer = NewsAPIxtractor()
    surfer.walk_through()
    # data = open('media.json')
    # fh = json.load(data)
    # print len(fh)
    # data.close()