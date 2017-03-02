#import nltk   
import urllib.request
import urllib.error
import re
from urllib.request import urlopen, HTTPError
#from lxml import html

class Pubmed(object):

	'''
		Evidence Based Medicine - Pubmed
		Created by Muhammad Sobri Maulana, CEH, OSCP

		Attributes:
		* Get Pubmed info using PMID:
		*   - Citation
		*   - Abstract
		*   - Authors
		*   - Journal
		*   - Title
		*   - Date
		* NLP interpretation of abstract
		*
	'''

	def __init__(self, pmid):
		self.pmid = pmid
		self.page = self.page(pmid)
		self.abstract = self.substring(self.page, "<Abstract>", "</Abstract>")
		self.journal = self.substring(self.page, "<Title>", "</Title>")
		self.title = self.substring(self.page, "<ArticleTitle>", "</ArticleTitle>")
		self.authors = self.authors( self.substring(self.page, '<AuthorList CompleteYN="Y">', "</AuthorList") )
		#self.citation = self.citation( self.substring(self.page, "<Journal>", "</Journal") )
		self.citation = self.citation( self.page )
		self.date = self.date( self.substring(self.page, "<PubDate>", "</PubDate>") )


	def interpret(self):
		abstract = self.stripTags(self.abstract)
		sentences = self.getSentences(abstract)
		#print(sentences)

	def getSentences(self, a):
		abstract = a.split(". ")
		if abstract[-1][-1] == ".":
			abstract[-1] = abstract[-1][:-1]
		return abstract

	def countWords(self):
		abstract = self.abstract.split(" ")
		wordList = set(abstract)
		wordCount = [ (abstract.count(x), x) for x in set(abstract) ]
		wordCount.sort(reverse=True)
		words = [ y for x, y in wordCount ]
		return wordCount
		#return words


	def toStringAPA(self):
		apa = ""

		aSize = len(self.authors)

		if aSize == 1:
			apa += self.authors[0]
		elif aSize < 8:
			for author in self.authors[:-1]:
				apa += author + ", "
			apa += "& " + self.authors[aSize-1]
		else:
			for author in self.authors[0:6]:
				apa += author + ", "
			apa += "... " + self.authors[aSize-1]

		apa += " (" + self.date[0:4] + "). "
		apa += self.title
		apa += " " if self.title.endswith(".") else ". "
		apa += self.journal + ". "
		apa += self.citation + "."

		return apa


	def page(self, pmid):
		xml = "?report=xml"
		pmURL = "http://www.ncbi.nlm.nih.gov/pubmed/"
		url = pmURL + pmid + xml
		
		page = self.pmCleanser( urlopen(url).read().decode('utf-8') )

		return page

	def authors(self, info):
		temp = info.split('<Author ValidYN="Y">')
		temp.pop(0)
		authorList = []

		for ele in temp:
			author = ""
			#first = self.substring(ele, "<ForeName>", "</ForeName>")
			first = self.substring(ele, "<Initials>", "</Initials>")
			last = self.substring(ele, "<LastName>", "</LastName>")
			author += last + ", " + first + "."
			authorList.append( author )

		return authorList

	def date(self, info):
		date = ""
		day = ""
		month = ""
		year = ""

		if "<Day>"   in info: day   += self.substring( info, "<Day>",   "</Day>"  )
		if "<Month>" in info: month += self.substring( info, "<Month>", "</Month>") + " "
		if "<Year>"  in info: year  += self.substring( info, "<Year>",  "</Year>" ) + " "

		date += year + month + day

		return date

	def citation(self, info):
		#citation = ""
		volume   = ""
		issue    = ""
		page     = ""

		if "<Volume>"     in info: volume += self.substring(info, "<Volume>", "</Volume>")
		if "<Issue>"      in info: issue  += "(" + self.substring(info, "<Issue>", "</Issue>") + ")"
		if "<MedlinePgn>" in info: page   += ":" + self.substring(info, "<MedlinePgn>", "</MedlinePgn>")

		citation = volume + issue + page
		return citation


	def substring(self, string, start, end):
		substring = re.findall(start+"(.+?)"+end+"+?", string)
		return substring[0]

	def stripTags(self, page):
		p = re.sub("</[^>]*>", " ", page) # Ending tags require a space to keep grammar consistency
		p = re.sub("<[^>]*>", "", p)      # Beginning tag
		p = p.strip()                     # Remove beginning and trailing whitespace
		return p

	def pmCleanser(self, page):
		page = page.replace("&lt;","<")
		page = page.replace("&gt;",">")
		page = page.replace("  ","")
		page = page.replace("\n","")
		return page
