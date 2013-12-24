import sys
from mod_python import apache
from subprocess import Popen, PIPE
from os.path import dirname,basename,exists
from os.path import join as djoin
from markdown import markdown
sys.path.append (djoin (dirname(__file__),".."))
import lib,traceback

def index (req, repo=None, version="0.0.0", OS="None"):
	if not repo:
		repolist = ""
		desc = "Download " + " ".join ([repo["name"] for repo in lib.get_config ("Repositories","Downloads")])
		for repo in lib.get_config ("Repositories","Downloads"):
			try:
				repolist += _snippet_for_repo (None, repo)
			except Exception as e:
				apache.log_error (str(e))
		return lib.respond (req, "<div class='news'>"+repolist+"<br/><br/></div>", "Downloads", "Downloads", desc, module_info ())
	else:
		repository = None
		for entry in lib.get_config ("Repositories","Downloads"):
			if entry["repo"] == repo:
				repository = entry
				break
		else:
			return lib.e404 (req, "Could not find a matching repository.", module_info())
		try:
			ver = _latest_ver (repo=repository)
		except Exception as e:
			apache.log_error (traceback.format_exc())
			return lib.e404 (req, "Repository corrupt or wrong configuration, please contact the administrator.", module_info())
		if version == ver:
			return lib.respond (req, "You're already running the lastest version of %s." % repository["name"], "Downloads", "Downloads", "Updater", module_info())
		else:
			return lib.respond (req, _snippet_for_repo (repo=repository),"Downloads", "Downloads", "Download %s" % repository["name"], module_info())

def _snippet_for_repo (req=None,repo=None):
	if req or not repo: return

	version = _latest_ver (req,repo)
	retval = "<h3>%s</h3>Latest version: <strong>%s</strong><br/>" % (repo["name"],version)
	retval += "<a href='%s'>Download source code</a><br/>" % (lib.get_config ("SnapshotDownloadURI","Downloads") % {"SitePrefix":lib.get_config("SitePrefix"),"repo":repo["repo"],"version":version})
	if repo["win32"]:
		retval += "<a href='%s'>Download Windows installer</a>"% (lib.get_config ("win32URI","Downloads") % {"SitePrefix":lib.get_config("SitePrefix"),"repo":repo["repo"],"version":version})
	return retval

def _latest_ver (req=None,repo=None):
	if req or not repo: return
	git_dir = djoin (lib.get_config ("RepoPath","Downloads"),repo["repo"])
	return Popen (["git", "--git-dir="+git_dir, "show-ref"],stdout=PIPE).communicate()[0].split("\n")[-2].split("/")[-1]

def module_info (req=None,active=None):
	if req: return
	return {"order": 3, "name": "Downloads"}
