'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	Arden Object Class
	arden.py

	Important! The Arden object can only handle single medical logic modules (MLMs).

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import re
import json
import xml.dom.minidom

class Arden(object):

	''' Constructor '''

	def __init__(self, version):
		self.mlm = {
			"maintenance":{
				"title":"",
				"mlmname":"",
				"arden":"",
				"version":"",
				"institution":"",
				"author":"",
				"specialist":"",
				"date":"",
				"validation":""
			},
			"library":{
				"purpose":"",
				"explanation":"",
				"keywords":"",
				"citations":"",
				"links":""
			},
			"knowledge":{
				"type":"",
				"data":"",
				"evoke":"",
				"logic":"",
				"action":""
			},
			"resources":{
				"default":"",
				"language":[]
			}
		}

		#self.categories  = list(self.mlm.keys())
		#self.slots_maint = list(self.mlm[ "maintenance" ].keys())
		#self.slots_lib   = list(self.mlm[ "library"     ].keys())
		#self.slots_knowl = list(self.mlm[ "knowledge"   ].keys())
		#self.slots_res   = list(self.mlm[ "resources"   ].keys())

		self.cat_order   = ["maintenance","library","knowledge","resources"]
		self.maint_order = ["title","mlmname","arden","version","institution","author","specialist","date","validation"]
		self.lib_order   = ["purpose","explanation","keywords","citations","links"]
		self.knowl_order = ["type","data","evoke","logic","action"]
		self.res_order   = ["default","language"]

		self.keywords = ["if","elseif","else","endif","then","conclude","true","false","return","while"]

		# Get number of languages
		self.numLangs = len(self.mlm["resources"]["language"])




	''' Import and export methods '''

	# Import medical logic module (MLM) in .json, .mlm, or .xml files (work on .json and .xml)
	def importMLM(self, path):
		f = open(path, 'r')
		mlm = f.read()

		p_split = path.split('.')
		ext = p_split[-1]

		if ext == "mlm":

			for c in list(self.mlm.keys()):
				slots = list(self.mlm[c].keys())

				for s in slots:
					_s = s + ":"
					if s != "language":
						start    = mlm.index(_s) + len(_s)
						end      = mlm[start:].index(";;") + start
						slotbody = mlm[ start : end ].strip()
						self.mlm[c][s] = slotbody
					elif s == "language":
						slotbody = [ x.strip()[x.index("language:") + len("language:") - 1:] for x in mlm.split(";;") if "language:" in x ]
						self.mlm[c][s].extend(slotbody)
					else:
						pass
						print("Error: Field Error")
		elif ext == "json":
			# Implies there's only one JSON object
			with open(path) as f:
				for line in f:
					jsonMLM = json.loads(line) #assumes JSON object is in one line
			for c in list(self.mlm.keys()):
				slots = list(self.mlm[c].keys())
				for s in slots:
					if s != "language":
						self.mlm[c][s] = jsonMLM[c][s]
					elif s == "language":
						self.mlm[c][s].extend(jsonMLM[c][s])
					else:
						pass
						print("Error: Field Error")
		elif ext == "xml":
			pass

		f.close()

	# Export mlm in .json, .mlm, or .xml files
	def exportMLM(self, path, schema=None):
		f = open(path, 'w')
		p = path.split('.')

		if   "xml"  in p: f.write( self.ArdenML(schema) )
		elif "json" in p: f.write( self.ArdenJSON()     )
		elif "mlm"  in p: f.write( self.ArdenSyntax()   )
		else:             f.write( self.ArdenSyntax()   )

		f.close()


	''' Get MLM in Arden Syntax, ArdenML, ArdenJSON, or IFrame '''

	def ArdenSyntax(self):
		return self.toString()

	def ArdenJSON(self):
		return json.dumps(self.mlm) # Order does not matter

	# Badly hacked; works but needs improvement
	def ArdenML(self, schema):
		multiple_tags = ["keywords","language"]

		xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ArdenMLs xsi:noNamespaceSchemaLocation=\"" + schema + "\" xmlns:fo=\"http://www.w3.org/1999/XSL/Format\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n <ArdenML>\n"

		for c in self.cat_order:
			xml += "  <"  + self.arden_capitalize(c) + ">\n"

			slots = self.getSlots(c)

			for s in slots:
				xml += "   <"  + self.arden_capitalize(s) + ">"

				if s != "language":
					slotbody = self.mlm[c][s]
					if slotbody != "":
						if ";" not in slotbody:
							xml += slotbody
						else:
							if ";" in slotbody:
								if s in multiple_tags: slotbody = self.ardenml_partition(slotbody, s)
								else:                  slotbody = self.ardenml_partition(slotbody)
								xml += slotbody
							else:
								xml += "\n    "  + slotbody + "\n"
								xml += "   "
				elif s == "language":
					for slotbody in self.mlm[c][s]:
						slotbody = [s.strip() for s in slotbody.split(":")]
						msg = re.findall("\"(.*?)\"",slotbody[1])
						xml += "\n    <Message>"  + msg[0] + "</Message>"
						xml += "   "
					xml.strip()
					xml += "\n   "

				xml += "</" + self.arden_capitalize(s) + ">\n"

			xml += "  </" + self.arden_capitalize(c) + ">\n"

		xml += " </ArdenML>\n</ArdenMLs>"
		return xml



	''' Custom mutator methods '''

	# Inputs subcat which is a string or dictionary (particularly for language)
	def setSlot(self, name, slotbody):
		for c in self.cat_order:
			if name in self.mlm[c]:
				self.mlm[c][name] = slotbody

	# Inputs a category with is a dictionary (of subcategories)
	def setCategory(self, name, slots):
		self.mlm[name] = slots




	''' Auxiliary methods '''

	# Prints Arden object as a prettified string
	def toString(self):
		string = ""

		for c in self.cat_order:
			string += c + ":\n"

			slots = self.getSlots(c)

			for s in slots:
				if s != "language":
					slot = self.mlm[c][s]
					string += " " + s + ": " + slot + ";;\n"
				elif s == "language":
					for i in range(self.numLangs):
						string += " " + s + ": " + self.mlm[c][s][i] + ";;\n"
		string += "end:"
		return string

	def getSlots(self, c):
		if   c == "maintenance": slots = self.maint_order
		elif c == "library":     slots = self.lib_order
		elif c == "knowledge":   slots = self.knowl_order
		elif c == "resources":   slots = self.res_order

		try:
			return slots
		except Exception as e:
			print("Error: Category not found. " + str(e))

	# Partition for ArdenML; create inner XML
	# Badly hacked; works but needs improvement
	def ardenml_partition(self, slotbody, slot=None):
		# Necessary Lists and Variables
		#keywords = ["if","elseif","else","endif","then","conclude","true","false"]

		xml = ""
		sp  = "    "
		slotbody = [s.strip() for s in slotbody.split(";")]

		if slot != None:
			for s in slotbody[:-1]:
				xml += s + "</" + self.arden_capitalize(slot) + ">\n" + sp + "<" + self.arden_capitalize(slot) + ">"
			xml += slotbody[-1]
		else:
			xml += "\n"
			slotbody = slotbody[:-1] # Because of .split(";"), the last element is always empty
			for s in slotbody:
				string_list = self.string_partition(s)
				sXML        = self.toXML(string_list, sp)
				xml += sXML + "\n" # temp
			xml += "\n" + sp

		try:
			return xml
		except Exception as e:
			print("Error: Invalid slotbody. " + str(e))

	# Will input a string; if from ardenml_partition, then it will be a computational "phrase"
	def string_partition(self, string):
		words  = []
		attr   = ["var", "otype"]
		otype  = ["list", "string","number","boolean"]
		string = string.replace("\n","")

		# Find comments
		if "/*" in string:
			str_list = string.split("*/")
			for sl in str_list:
				if "/*" in sl:
					sl = sl.replace("/*","").strip()
					words.append("<!-- " + sl + " -->")
				elif ":=" in sl:
					asgn = { "Assignment":{"Identifier":{"var":"","otype":""},"Assigned":{}}}
					sl = [ x.strip() for x in sl.split(":=")]
					asgn_var = sl[0]
					asgn_val = sl[1]
					asgn["Assignment"]["Identifier"]["var"]   = asgn_var
					asgn["Assignment"]["Identifier"]["otype"] = self.stringIsType(asgn_val)

					sType = asgn["Assignment"]["Identifier"]["otype"]
					val_list = ("Value",)

					if sType == "list": # is list
						asgn["Assignment"]["Assigned"]["List"] = []
						if "=" and not "(" and not ")" in asgn_val:
							pass
						elif "(" and ")" in asgn_val:
							asgn_val_lists = re.findall(r"\(.*?\)", asgn_val)
							for avl in asgn_val_lists:
								print(asgn_val_lists)
								asgn_val_split = asgn_val.split(",").strip()
								for av in asgn_val_split:
									asgn["Assignment"]["Assigned"]["List"].append(val_list)
					else:
						val_list += (sType, asgn_val)
						asgn["Assignment"]["Assigned"]["Value"] = val_list
					words.append(dict(asgn))

		return words

	# Recursively converts dictionary, tuple, or list to XML
	def toXML(self, words, sp="", xml="", cat=""):
		attr   = ["var", "otype"]
		otype  = ["list", "string","number","boolean"]
		try:
			wType = type(words)

			if wType == list: 
				for w in words:
					if type(w) == str: # for comments
						xml += sp + w + "\n"
					elif type(w) == dict: # for dictionaries in lists
						keys = w.keys()
						for k in keys:
							wk = w[k]
							xml += sp + "<" + self.arden_capitalize(k) + ">"
							if type(wk) == str:
								xml += wk
							else: # for dictionary, list, or tuple inside dictionary
								xml += "\n" + sp + " " + self.toXML(wk, sp + " ", xml) + "\n"
							xml += sp + "</" + self.arden_capitalize(k) + ">"
			elif wType == dict:
				keys = words.keys()
				for k in keys:
					wk = words[k]
					xml += sp + "<" + self.arden_capitalize(k) + ">\n"
					if type(wk) == dict: # for dictionary inside dictionary
						xml += self.toXML(wk, sp + " ", xml)
					xml += sp + "</" + self.arden_capitalize(k) + ">\n"
			elif wType == tuple:
				xml += sp + "<" + self.arden_capitalize(words[0]) + ">\n"
				#if
				xml += sp + "</" + self.arden_capitalize(words[0]) + ">\n"
			else:
				return words
			#
			#for i, w in enumerate(words):
			#	xml += sp + "<" + self.arden_capitalize(w) + ">"
			#	xml += sp + "</" + self.arden_capitalize(w) + ">"
			print(xml)
			return xml
		except Exception as e:
			print("Error: in dictionary, list, or tuple. " + str(e))
			return "" # None?

	def stringIsType(self, string):
		if   "=" in string or "(" and ")" in string: return "list"
		elif string.isdigit(): return "number"
		elif string.capitalize() == "True" or string.capitalize() == "False": return "boolean"
		else: return "string"

	def arden_capitalize(self, tag):
		if tag == "mlmname":
			tag = "MLMName"
		else:
			tag =  tag.capitalize()
		return tag