import urllib.request
import urllib.error
import re

from urllib.request import urlopen, HTTPError
#from lxml import html

class CRD(object):

	'''
		A class for University of York's Centre for Reviews and Dissemination

		Attributes:
		* DARE (Database of abstracts of reviews of effects) database
		* Cochrane database?
	'''

	def __init__(self, an):
		self.base = "http://www.crd.york.ac.uk/CRDWeb/"

		aUrl = self.base + "ShowRecord.asp?AccessionNumber=" + an

		sUrl = self.base + "ResultsPage.asp" # Use to all recently added articles

		self.page         = self.crdCleanser( self.getPage(aUrl) )
		self.title        = self.substring(self.page, "<title>", "</title>")
		self.authors      = self.substring(self.page, "docAuthor\">", "</td>")
		self.bibliography = self.substring(self.page, "Bibliographic details</div><div class='docText'>","</div>")

		tempBegin1 = "</div><div class='docText'><p>"
		tempEnd1   = "</p></div></div><div class='docTotal'><div class='docCaption'>"
		self.crdSummary       = self.substring(self.page, "CRD summary" + tempBegin1, tempEnd1 + "Authors' objectives")
		self.authorObjectives = self.substring(self.page, "Authors' objectives" + tempBegin1, tempEnd1 + "Searching")
		self.searching       = self.substring(self.page, "Searching" + tempBegin1, tempEnd1 + "Study selection")
		self.studySelection  = self.substring(self.page, "Study selection" + tempBegin1, tempEnd1 + "Assessment of study quality")
		self.assessment      = self.substring(self.page, "Assessment of study quality" + tempBegin1, tempEnd1 + "Data extraction")
		self.dataExtraction  = self.substring(self.page, "Data extraction" + tempBegin1, tempEnd1 + "Methods of synthesis")
		self.methods         = self.substring(self.page, "Methods of synthesis" + tempBegin1, tempEnd1 + "Results of the review")
		self.results         = self.substring(self.page, "Results of the review" + tempBegin1, tempEnd1 + "Authors' conclusions")
		self.CRDCommentary   = self.substring(self.page, "Authors' conclusions" + tempBegin1, tempEnd1 + "CRD commentary")
		self.implications    = self.substring(self.page, "CRD commentary" + tempBegin1, tempEnd1 + "Implications of the review for practice and research")
		self.PubMedID        = self.substring(self.page, "PubMedID" + tempBegin1, tempEnd1 + "DOI")


	def getPage(self, link):
		page = urlopen(link).read().decode('utf-8')
		return page

	def substring(self, string, start, end):
		try:
			substring = re.findall(start+"(.+?)"+end+"+?", string)
			return substring[0]
		except Exception as e:
			print("Error: " + str(e))
			return ""

	def crdCleanser(self, page):
		page = page.replace("  ","")
		page = page.replace("\n","")
		return page