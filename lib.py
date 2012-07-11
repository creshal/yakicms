import os,time,datetime,stat,imp
import json
try:
	from mod_python import apache
except:
	print ("You're not supposed to run this directly.")

def get_config (key=None,confdir=""):
	try:
		with open (valid_dir(os.path.join (confdir,"config.json"))) as conffile:
			config = json.load (conffile)
			return config[key] if key else config
	except:
		raise IOError("Config file %s (validated from %s) not found or corrupt!" % (valid_dir(os.path.join (confdir,"config.json")), confdir) )


def valid_dir (path):
	workingdir = get_workingdir()
	if not path.startswith("/"): path = os.path.join (workingdir, path)
	if os.path.commonprefix ([workingdir, os.path.abspath (path)]) == workingdir: return path
	else:
		raise IOError("Invalid file include path: %s, expected %s to be below %s" %(path,os.path.commonprefix ([workingdir, os.path.realpath (path)]),workingdir))


def get_workingdir ():
	return os.path.abspath(os.path.dirname(__file__))


def get_time_for_file (file, is_rfc3339=False):
	file = valid_dir(file)
	mtime = time.gmtime (os.stat(file)[stat.ST_MTIME])
	if is_rfc3339:
		rtime = time.strftime("%Y-%m-%dT%H:%M:%S%z", mtime)
		return rtime[:-2]+":"+rtime[-2:]
	return time.strftime("%d. %b %Y, %H:%M UTC", mtime)


def get_rfc3339_time ():
	rtime = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.gmtime())
	return rtime[:-2]+":"+rtime[-2:]


def get_time_delta (file):
	return str (datetime.timedelta (seconds = int (time.time() - (os.stat(valid_dir(file))[stat.ST_MTIME]))))


def get_template (filename):
	path = valid_dir (os.path.join (get_workingdir(),"_templates",filename+".tpl"))
	with open (path) as tplfile:
		template = "".join (tplfile.readlines())
	return template


def _generate_headers ():
	headers = ""
	for name, entry in _entries():
		if "styles" in entry:
			for style in entry["styles"]:
				headers += ('<link rel="stylesheet" type="text/css" href="%s" />' % style)
		if "script" in entry:
			for script in entry["scripts"]:
				headers += ('<script src="%s" type="text/javascript" charset="UTF-8"></script>' % script)
		if "headers" in entry:
			for header in entry["headers"]:
				headers += header
	return headers


def _entries (attr="module_info"):
	candidates = os.listdir (get_workingdir())
	for entry in candidates:
		entrydir = os.path.join (get_workingdir(), entry)
		entryfile = os.path.join (entrydir,"index.py")
		if os.path.isdir(entrydir) and entry[0] != "_" and os.path.isfile(entryfile):
			with open (entryfile) as entry_f:
				Entry = imp.load_module (entry, entry_f,entryfile,('.py','U',1))
			if not hasattr (Entry, attr): continue
			entry_info = getattr (Entry, attr) ()
			yield entry, entry_info


def _generate_menu (current):
	menuitems = []
	entry_tpl = get_template ("menu")

	for entry, entry_info in _entries():
		if current and entry_info["name"] == current["name"]:
			entry_info = current
		iconfile = os.path.join ("/",entry,"menuicon.png")
		if "menuentry" in entry_info:
			menuitems.append ((entry_info["order"],entry_info["menuentry"]))
		else:
			cls = "em" if current and entry_info["name"] == current["name"] else ""
			menuitems.append ((entry_info["order"], entry_tpl % {"icon": ljoin (iconfile), "name": entry_info["name"] if "name" in entry_info else entry, "cls": cls, "path": ljoin (entry)}))

	menu = '<div class="menu %(cls)s"><a class="breadcrumb" href="%(site_prefix)s"><img class="inline" src="/static/home.png" alt="home"/>Home</a></div>' % {"site_prefix":get_config("SitePrefix"), "cls": "" if current else "em"}
	for item in sorted (menuitems, key=lambda item: item[0]):
		menu += item[1]

	return menu


def generate_header (title, caption, description, current_module):
	return get_template("header") % {"title": escape (title, False) ,"caption": escape (caption, False) ,"desc": escape (description, False) ,"site_title":get_config("SiteTitle"),"site_desc": get_config("SiteDesc"),"menu": _generate_menu(current_module),"site_prefix": get_config("SitePrefix"),"headers":_generate_headers()}


def generate_footer ():
	return get_template ("footer")


def index (req):
	return ""


def respond (req, content, title, caption, description, current_module):
	req.content_type = "text/html; charset=UTF-8"
	return "%s%s%s" %(generate_header (title, caption, description, current_module), escape (content),generate_footer())


def e404 (req, message, current_module):
	req.status = apache.HTTP_NOT_FOUND
	return respond (req, message, "Not found", "Not found", "Not found", current_module)


def escape (text, allow_html=True, encoding="utf-8"):
	if not type (text) in (str,unicode): return

	text = text.decode (encoding)

	if not allow_html:
		escape_table = {"&": "&amp;", '"': "&quot;", "'": "&apos;", ">": "&gt;", "<": "&lt;"}
		text = "".join (escape_table.get (c,c) for c in text)

	return text.encode ("ascii","xmlcharrefreplace")

def ljoin (*uri):
	uri = os.path.join (get_config("SitePrefix"), *uri)
	return uri
