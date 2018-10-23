# coding: utf-8

from botty_mcbotface.tasq_runner import bot_routine
from slackbot.dispatcher import Message
from slackbot.bot import respond_to
import urllib.request
import datetime as dt
import re
import pickle
import os
import requests

SPAN = 60 * 60 * 24

@respond_to('RSS')
def daily(message):
    print('I run once initially after a delay, then every 24 hours.')    
    @bot_routine(SPAN, delay=True)
    def rss():
    	# query = "(cat:stat.ML+OR+cat:cs.CV+OR+cs.HC+OR+cs.IR)+AND+((abs:emotion)+OR+(abs:ECG)+OR+(abs:time\ series))"
    	query = "(cat:stat.ML)"
    	# get rss
    	rss = get_rss(query)
    	for _rss in rss:
	    	message.send(_rss)	
    return 

def get_rss(query, max_results=5):
	# url of arXiv API
	# If you want to customize, please change here.
	# detail is shown here, https://arxiv.org/help/api/user-manual
	arxiv_url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=0&max_results=' + str(max_results) + '&sortBy=lastUpdatedDate&sortOrder=descending'
	# Get returned value from arXiv API
	data = requests.get(arxiv_url).text
	# Parse the returned value
	entries = parse(data, "entry")
	rss = []
	for i, entry in enumerate(entries):
		# Parse each entry
		url = parse(entry, "id")[0]
		title = parse(entry, "title")[0]
		date = parse(entry, "published")[0]
		summary = parse(entry, "summary")[0]
		_rss = "\n".join(["=" * 10, "No." + str(i + 1), "Title:  " + title, "Summary: " + summary, "URL: " + url, "Published: " + date])
		rss.append(_rss)
	return rss

def parse(data, tag):

    # parse atom file
    # e.g. Input :<tag>XYZ </tag> -> Output: XYZ

    pattern = "<" + tag + ">([\s\S]*?)<\/" + tag + ">"
    if all:
        obj = re.findall(pattern, data)
    return obj



