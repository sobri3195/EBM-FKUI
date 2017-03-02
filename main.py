#!/usr/bin/env python
from login import *
from pubmed import Pubmed
from medal import Medal
from crd import CRD
from arden import Arden
from tripdb import TripDB

'''
#print(a.title)
#print(a.journal)
#print(a.abstract)
#print(a.authors)
#print(a.citation)
#print(a.date)

pmid = ["17873119", "21655256"];
for p in pmid: 
	pm = Pubmed(p)
	#print(pm.countWords())
	#print(pm.getSentences())
	pm.interpret()
	#print(pm.toStringAPA())
	#print(a.abstract)
'''

anid = ["12012015431"]
#for a in anid:
#	an = CRD(a)
#	print(an.bibliography)


#TEMP

chapter = "A00-B99"
block = "A00-A09"
link = "adult-comorbidity-evaluation-27-ace-27"

#m = Medal(medal_uid, medal_pass)
#m.algoPage(link)
#m.algoRef("108")
#m.searchAlgo("A15")
#m.crawlEntireAPI()

#tempList = m.medalAjaxAPI("20", "dis")
#print(tempList)

#m.page(link)

#print(m.generateIframe("adult-comorbidity-evaluation-27-ace-27"))
#print(m.searchKeywords("test"))
#print(m.algoRef("adult-comorbidity-evaluation-27-ace-27"))
#m.close()


t = TripDB(tripdb_email, tripdb_pass)
t.search('test')

#a = Arden(2.7)
#a.importMLM("data/test2.json")
#a.exportMLM("data/test2.mlm")
#a.setSlot("logic","test")
#print(a.toString())
#print(a.ArdenML("../xsd/Arden2.7.xsd"))