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
import csv

SPAN = 60 * 60 * 12

@respond_to('RSS')
def daily(message):
	# print("telling RSS")
	@bot_routine(SPAN, delay=True)
	def rss():
		# print("getting RSS..")
		# query = "(cat:stat.ML+OR+cat:cs.CV+OR+cs.HC+OR+cs.IR)+AND+((abs:emotion)+OR+(abs:ECG)+OR+(abs:time\ series))"
		query = "((cat:stat.ML)+OR+(cat:cs.CV)+OR+(cat:cs.LG)+OR+(cat:cs.SD))"
		# get rss
		rss = get_rss(query)
		sent_flag = False
		# read csv
		f = open('log.csv', 'r', encoding='UTF-8')
		csv_data = csv.reader(f)
		for _rss in rss:
			# csvに載ってないrssをメッセージで送信
			if not find(_rss[2], csv_data):
				sent_flag = True
				rss_message = create_message(_rss)
				message.send(rss_message)
		f.close()
		if sent_flag:		# write csv
			f = open('log.csv', 'w', newline='')
			csvWriter = csv.writer(f)
			for _rss in rss:
				csvWriter.writerow([_rss[2]])
			f.close()
	return 

def get_rss(query, max_results=5):
	# url of arXiv API
	# If you want to customize, please change here.
	# detail is shown here, https://arxiv.org/help/api/user-manual
	# arxiv_url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=0&max_results=' + str(max_results) + '&sortBy=lastUpdatedDate&sortOrder=descending'
	arxiv_url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=0&max_results=' + str(max_results) + '&sortBy=submittedDate&sortOrder=descending'
	# Get returned value from arXiv API
	data = requests.get(arxiv_url).text
	# Parse the returned value
	entries = parse(data, "entry")
	rss = []
	for i, entry in enumerate(entries):
		# Parse each entry
		# write in csv file
		_ = ()
		title = parse(entry, "title")[0]
		summary = parse(entry, "summary")[0]
		url = parse(entry, "id")[0]
		date = parse(entry, "published")[0]
		_ = _ + (title, summary, url, date,)
		rss.append(_)
	return rss

def find(id, csv_data):
	for row in csv_data:
		if row:
			if id == row[0]:
				return True
	return False

def create_message(rss):
	message = "\n".join(["=" * 10, "Title: " + rss[0], "Summary: " + rss[1], "URL: " + rss[2], "Published: " + rss[3]])
	return message

def parse(data, tag):

    # parse atom file
    # e.g. Input :<tag>XYZ </tag> -> Output: XYZ

    pattern = "<" + tag + ">([\s\S]*?)<\/" + tag + ">"
    if all:
        obj = re.findall(pattern, data)
    return obj



