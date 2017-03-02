import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar

import re

from urllib.request import urlopen, HTTPError

class TripDB(object):

	def __init__(self, email, pw):
		url = "http://www.tripdatabase.com"
		login_url = "http://www.tripdatabase.com/account/login"

		emailField    = "email"
		passwordField = "password"


		self.cookie = http.cookiejar.CookieJar()

		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))

		login_data  = urllib.parse.urlencode({emailField : email, passwordField : pw})
		binary_data = login_data.encode('ASCII')

		self.opener.open(login_url, binary_data)
		resp        = self.opener.open(url)
		self.page   = resp.read().decode('utf-8')

		#print(self.page)
		print("Logged in!") if self.page.find("Logout") != -1 else print("Login failed")


	# Search
	def search(self, terms):
		base = "http://www.tripdatabase.com/search"
		url = "http://www.tripdatabase.com/search?categoryid=&criteria=" + terms

		page = self.opener.open(url).read().decode('utf-8')

		count = self.substring(page,'<span id="resultcount">','</span> result')
		print(count + " results found")

	def PICOSearch(self, population, comparison, intervention, outcome):
		url = "http://www.tripdatabase.com/search/wizard"

	def advancedSearch(self, all, any, exact, exclude):
		url = "http://www.tripdatabase.com/search/advanced"

		input_all = "All"
		allSearchType = "AllSearchType"

		input_any = "Any"
		anySearchType = "AnySearchType"

		input_phrase = "Phrase"
		phraseSearchType = "PhraseSearchType"

		input_not = "Not"
		notSearchType = "NotSearchType"

		fromDate = "FromDate"
		toDate = "ToDate"

	# Get Latest
	def latest(self):
		url = "http://www.tripdatabase.com/latest"


	# Auxiliary
	def substring(self, string, start, end):
		try:
			substring = re.findall(start+"(.+?)"+end+"+?", string)
			return substring[0]
		except Exception as e:
			print("Error: " + str(e))
			return ""