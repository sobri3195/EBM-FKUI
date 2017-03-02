import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar
import re
import json
import math

from urllib.request import urlopen, HTTPError
from arden import Arden
#from lxml import html

class Medal(object):

	'''
		A class for Medal.org

		Attributes:
		* Medal.org login (required) :(
		* Extract algorithms and information from Medal.org
		* Future medal.org API?
	'''

	def __init__(self, uid, pw):
		url = "http://medal.org"
		login_url = "http://medal.org/login/ajax_login"


		form_name   = "form_login" # class="form_login"
		id_input    = "txt_login_uid" # id="txt_login_uid" name="txt_login_uid"
		pw_input    = "txt_login_password" # id="txt_login_password" name="txt_login_password"
		btn_submit  = "btn_login" # value="LOGIN" name="btn_login" id="btn_login"


		self.cookie = http.cookiejar.CookieJar()

		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))

		login_data  = urllib.parse.urlencode({id_input : uid, pw_input : pw})
		binary_data = login_data.encode('ASCII')

		self.opener.open(login_url, binary_data)
		resp        = self.opener.open(url)
		self.page   = resp.read().decode('utf-8')


		print("Logged in!") if self.page.find("Sign-Out") != -1 else print("Login failed")


	def disease(self, path):
		temp = "foo"
		return json.dumps(temp)

	def semisubcat(self, path):
		temp = "foo"
		return json.dumps(temp)

	def subcat(self, path):
		temp = "foo"
		return json.dumps(temp)

	def algorithm(self, path):
		temp = "foo"
		return json.dumps(temp)


	def generateIframe(self, algo, height="auto", width="auto"):
		height = str(height)
		width = str(width)
		iframe = '<iframe src="http://medal.org/' + algo + '" height="' + height + '" width="' + width + '"></iframe>'
		return iframe


	''' Algorithm searching methods '''

	def searchKeywords(self, terms):
		url = "http://medal.org/common/searched_algos"

		data  = urllib.parse.urlencode({"search_txt" : terms})
		binary_data = data.encode('ASCII')

		temp = self.htmlEntity( self.opener.open(url, binary_data).read().decode('utf-8') )

		if temp.find("0 result") == -1:
			countResults = self.substring(temp, 'pagination_info">', "results    </p>").strip()
			print( countResults + " results found!")
			numPages = math.ceil(int(countResults)/10)

			# Get algorithms on first page (10)
			algoList = self.substring(temp, '<ul id="algo_list">', 'Next</a>')
			algoIds = re.findall("id='(.+?)'>+?",  algoList)

			aiList = []

			for ai in algoIds:
				algo = self.searchAlgo(ai)
				aiList.append(algo)

			return aiList

		else:
			print("No search results found")
			return None


	def searchAlgo(self, algoId):
		#search_url = "http://medal.org/common/searched_algos"
		# Fastest current method
		base = "http://medal.org/"
		algoId = algoId.replace("(","")
		algoId = algoId.replace(")","")
		algoId = algoId.replace(" ","-")
		url = base + algoId
		# Needs to return algoPage
		form, js, rslt = self.algoPage(url)
		algoPage = form + js + rslt
		return algoPage


	def algoPage(self, link):
		base = "http://medal.org/"
		if base not in link:
			url = base + link
		else:
			url = link

		page = self.getPage(url)

		form = self.substring(page, "<!------------- start calculator i/p section  ------------->", "<!------------- end calculator i/p section ------------->")
		
		js = self.substring(page, '<script type="text/javascript" src="http://medal.org/js/jquery.maskedinput.js"></script>', "<!------------- start calculator i/p section  ------------->")

		rslt = self.substring(page, "<!------------- end calculator i/p section ------------->\n", '<div id="reference_tab" class="tab_content" style="overflow:auto;width:auto;padding:18px 18px 0;">')

		return form, js, rslt

	def algoJS(self, algo_id):
		base = "http://medal.org/"
		if base not in link:
			url = base + link
		else:
			url = link

		page = self.getPage(url)

		js = self.substring(page, '<script type="text/javascript" src="http://medal.org/js/jquery.maskedinput.js"></script>', "<!------------- start calculator i/p section  ------------->")

		return js

	def algoForm(self, algo_id):
		base = "http://medal.org/"
		if base not in link:
			url = base + link
		else:
			url = link

		page = self.getPage(url)

		form = self.substring(page, "<!------------- start calculator i/p section  ------------->", "<!------------- end calculator i/p section ------------->")

		return form

	def algoRslt(self, algo_id):
		base = "http://medal.org/"
		if base not in link:
			url = base + link
		else:
			url = link

		page = self.getPage(url)

		rslt = self.substring(page, "<!------------- end calculator i/p section ------------->\n", '<div id="reference_tab" class="tab_content" style="overflow:auto;width:auto;padding:18px 18px 0;">')

		return rslt

	def algoRef(self, algo_id):
		#base = "http://medal.org/"
		#url = base + link
		#resp = self.opener.open(url)
		#page = resp.read().decode('utf-8')

		ref_url = "http://medal.org/common/ajax_get_reference"

		rslt_data  = urllib.parse.urlencode({"algo_id" : algo_id})
		binary_data = rslt_data.encode('ASCII')

		temp = self.htmlEntity( self.opener.open(ref_url, binary_data).read().decode('utf-8') )
		print(temp)


	def crawlEntireAPI(self):
		mHome = self.medalAjaxAPI("", "home")
		# mHome = {'ext':[], 'val':[], 'html':[]}
		# Not sure why cHtml is empty but it doesn't matter

		# Initialize dictionaries
		mDis = {}
		mSub = {}
		mSsc = {}
		mAlg = {}
		
		# For this particular API, "ext" doesn't provide results whereas "val" does
		# Check to ensure the above note isn't a bug
		#for mh in mHome['ext']:
		for mh in mHome['val']:
			mDisTemp = self.medalAjaxAPI(mh, "dis")
			mDis[mh] = mDisTemp['ext'] # Note: val is empty for "dis"
			self.printFile("medalDis.txt", mDis, "json") # Print mDis into file (json format)

			mSscTemp = self.medalAjaxAPI(mh, "ssc")
			mSsc[mh] = mSscTemp['ext']
			self.printFile("medalSsc.txt", mSsc, "json")

			mSubTemp = self.medalAjaxAPI(mh, "subcat")
			mSub[mh] = mSubTemp['ext']
			self.printFile("medalSub.txt", mSub, "json")

			mAlgTemp = self.medalAjaxAPI(mh, "algo")
			mAlg[mh] = mAlgTemp['ext']
			self.printFile("data/medalAlg.txt", mAlg, "json")
			#for md in mDis['ext']:
			#	print(md)


	def medalAjaxAPI(self, urlID, code):
		medal = {}

		base = "http://medal.org"

		url = base

		if code   == "dis":
			url   += "/common/ajax_get_diseases/"           + urlID

		elif code == "ssc":
			url   += "/common/ajax_get_semisubcategories/"  + urlID

		elif code == "subcat":
			url   += "/common/ajax_get_subcategories/"      + urlID

		elif code == "algo":
			url   += "/common/ajax_get_algocategorization/" + urlID

		elif code == "home":
			url   += urlID


		page = self.getPage(url)
		ext, val, html = self.ajaxPage(page, code)

		medal['ext']  = ext
		medal['val']  = val
		medal['html'] = html
		return medal

	def ajaxPage(self, page, code):

		# Default values
		regexURL  = None
		regexVal  = None
		regexHTML = None

		if code == "dis":
			regexURL  = "<div class=\"subcat_num\">(.+?)</div>+?"
			regexVal  = None
			regexHTML = "<div class=\"subcat_desc\">(.+?)</div>+?"

		elif code == "ssc":
			regexURL  = "<div class=\"block_num\">(.+?)</div>+?"
			regexVal  = "value=\"(.+?)\"><a>+?"
			regexHTML = "<div class=\"block_desc\">(.+?)</div>+?"

		elif code == "subcat":
			regexURL  = "<div class=\"cat_num\">(.+?)</div>+?"
			regexVal  = "value=\"(.+?)\"><a>+?"
			regexHTML = "<div class=\"cat_desc\">(.+?)</div>+?"

		elif code == "algo":
			regexURL  = "openCalculatorForAlgo\('(.+?)'\);+?"
			regexVal  = "value=\"(.+?)\" onclick=+?"
			regexHTML = "<a href=\"#\">(.+?)</a>+?"

		elif code == "home":
			regexURL  = "<div class=\"chap_num\">(.+?)</div>+?"
			regexVal  = "value=\"(.+?)\" icdcode+?"
			regexHTML = "<div class=\"chap_desc\">(.+?)</div>+?"

		name = re.findall(regexURL,  page) if regexURL  is not None else []
		val  = re.findall(regexVal,  page) if regexVal  is not None else []
		html = re.findall(regexHTML, page) if regexHTML is not None else []

		return name, val, html


	def close(self):
		resp      = self.opener.open("http://medal.org/login/logout")
		self.page = resp.read().decode('utf-8')
		print("Logged out!") if self.page.find("Sign-in") != -1 else print("Logout failed")


	def getPage(self, link):
		try:
			page = self.opener.open(link).read().decode('utf-8')
			return page
		except UnicodeEncodeError as e:
			print("Error: " + str(e))
			return ""


	def htmlEntity(self, html):
		html = html.replace("&amp;", "&")
		return html

	def substring(self, string, start, end):
		try:
			substring = string[ string.index(start) + len(start) : string.index(end) ]
			return substring
		except Exception as e:
			print("Error: " + str(e))
			return ""

	def printFile(self, path, content, code):
		f = open(path,'w')

		if code == "json": f.write(json.dumps(content))

		f.write("\n")
		f.close()