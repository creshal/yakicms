import sys
from mod_python import apache
from os.path import dirname,basename,exists
from os.path import join as djoin
from markdown import markdown
sys.path.append (djoin (dirname(__file__),".."))
import lib

def index (req,page=None):
	entries = lib.get_config ("Entries","Static")
	pagemeta = None
	for entry in entries:
		if entry["uri"] == page and "src" in entry:
			pagemeta = entry
			break
	else:
		req.headers_out["location"] = lib.get_config ("SitePrefix").encode()
		req.status = apache.HTTP_MOVED_TEMPORARILY
		return

	with open ( lib.valid_dir (djoin (dirname(__file__),pagemeta["src"])) ) as pagefile:
		text = lib.escape ("\n".join (pagefile.readlines()))
	if ".md" in pagemeta["src"]:
		text = markdown (text)
	text = lib.get_template ("static") % {"content": text}

	return lib.respond (req, text, pagemeta["title"],pagemeta["caption"],pagemeta["description"],module_info(active=page))

def generate_entries (req=None,current=None):
	if req: return

	entry_tpl = lib.get_template ("menu")
	retval = ""
	for entry in lib.get_config ("Entries","Static"):
		if "src" in entry: uri = lib.ljoin ("Static","?page="+entry["uri"])
		else:              uri = entry["uri"] if entry["uri_is_relative"] is False else lib.ljoin (entry["uri"])
		retval += entry_tpl % {"icon": entry["icon"], "name": entry["name"], "path": uri, "cls": "em" if current == entry["uri"] else ""}
	return retval

def module_info (req=None,active=None):
	if req: return
	return {"order": 2, "menuentry": generate_entries(current=active), "name": "Static"}
