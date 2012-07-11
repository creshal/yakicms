import sys,os
from markdown import markdown
from glob import glob
from xml.sax.saxutils import escape
from os.path import dirname,basename,exists
from os.path import join as djoin
sys.path.append (dirname(__file__))
import lib

def index (req):
	response = ""
	for file in _enum_files ():
		with open (file) as snippet:
			response += markdown (lib.escape ("\n".join (snippet.readlines())))
	for entry in lib._entries ("homepage_widget"):
		response += "<a href='%s'>"% (djoin (lib.get_config ("SitePrefix"),entry[0]))+"<h3>%(title)s</h3></a><div>%(content)s</div>" % entry[1]
	return lib.respond (req, response, "","", lib.get_config ("SiteDesc"), None)
	#TODO: Show all snippets from _mainpage. Then show all module excerpts

def _enum_files (req=None):
	if req: return
	files = glob (djoin (dirname(__file__),"_mainpage","*.md"))
	return sorted(files, lambda a,b: cmp(int(a.split(".")[0]), int(b.split(".")[0])))

