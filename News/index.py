import sys,os
from markdown import markdown
from mod_python import apache
from glob import glob
from math import ceil
from re import sub
from xml.sax.saxutils import escape
from os.path import dirname,basename,exists
from os.path import join as djoin
sys.path.append (djoin (dirname(__file__),".."))
import lib

def index (req, id=-1, page="0",feed=False):
	if id >= 0:
		try:
			content,title,author = parse_news (str(int(id)),req)
			return lib.respond (req, content, title, "News", title, module_info())
		except:
			return lib.e404 (req,"Could not find matching news!", module_info())

	if feed:
		return generate_feed(req)

	return lib.respond (req, generate_page (int (page), 1), "News", "News", "News", module_info())


def generate_page (page, news_amount_factor, show_nav=True):
	if not type(page) is int: return

	news_per_page = int (lib.get_config ("NewsPerPage") * float (news_amount_factor))

	news = _enum_news()
	pages = int(ceil (len(news) / float(news_per_page)))

	content = "".join ([parse_news (id)[0] for id in news[page*news_per_page:page*news_per_page+news_per_page]])

	page_str = ""
	if show_nav:
		for i in range (pages):
			page_str += '<a class="link %(cls)s" href="?page=%(i)i">%(i)i</a> | ' % {"i":i, "cls": "em" if i == page else ""}

		if page > 0:
			page_str = '<a class="link" href="?page=0"><img width="16" height="16" class="inline" src="/static/first.png" alt="goto first page"/>Newest</a> | <a rel="prev" class="link" href="?page=%(i)i"><img width="16" height="16" class="inline" src="/static/prev.png" alt="goto newer page"/>Newer</a> | ' % {"i": page-1} + page_str
		if page < (pages-1):
			page_str += '<a rel="next" class="link" href="?page=%(i)i">Older<img class="inline" width="16" height="16" src="/static/next.png" alt="goto older page"/></a> | <a class="link" href="?page=%(l)i">Oldest<img class="inline" width="16" height="16" src="/static/last.png" alt="goto last page"/></a>' % {"i": page+1, "l": pages-1}

	return lib.get_template ("news_pages") % {"pages": page_str, "content": content}


def parse_news (id,req=None):
	if not type (id) is str: return

	newstpl = lib.get_template ("news")
	filename = lib.valid_dir (djoin (dirname(__file__),basename(id)))
	if exists (filename+".news"):
		filename += ".news"
		mode = "plain"
	elif exists (filename+".md"):
		filename += ".md"
		mode = "markdown"
	else:
		raise Exception ();

	time = lib.get_time_for_file (filename)
	with open (filename) as newsfile:
		author = lib.escape (newsfile.readline().replace("\n",""))
		headline = lib.escape (newsfile.readline().replace("\n",""))
		newscontent = lib.escape ("\n".join (newsfile.readlines()))

	if mode is "markdown":
		newscontent = markdown (newscontent)

	return (newstpl % {"headline":headline,"author":author,"date":time,"id":id,"content":newscontent,"uri":lib.ljoin ("News","?id="+id)}, headline,author)


def _enum_news (req=None):
	if req: return
	newsfiles = [basename (file).split(".")[0] for file in glob (djoin (dirname(__file__),"*.md")) + glob (djoin (dirname(__file__),"*.news"))]
	return sorted(newsfiles, lambda a,b: cmp(int(a.split(".")[0]), int(b.split(".")[0])), reverse=True)


def generate_feed (req):
	prefix = lib.absolute_prefix()
	news = _enum_news ()
	feed = ""
	lastmodified = ""
	for id in news:
		filename = lib.valid_dir (djoin (dirname(__file__),basename(id)))
		filename = filename+".md" if exists (filename+".md") else filename+".news"
		if id == news[0]: lastmodified = lib.get_time_for_file (filename,True)
		content, headline, author = parse_news(id)
		content = sub ('style=".*?"', "", escape(content))
		uri = djoin (lib.get_config ("CanonicalName"),prefix,"News","?id="+id)
		feed += lib.get_template ("feedentry") % {"uri":uri,"title":headline, "mtime":lib.get_time_for_file (filename,True), "content": content, "author": author}
	req.content_type = "application/atom+xml; charset=UTF-8"
	return lib.get_template ("feed") % {"uri": djoin (lib.get_config ("CanonicalName"),prefix), "self":  djoin (lib.get_config ("CanonicalName"),prefix,"News","?feed=true"), "mtime": lastmodified, "content": feed}


def feeduri (req=None):
	if req: return
	return '<link href="%s/?feed=true" type="application/atom+xml" rel="alternate" title="ATOM News Feed" />' % lib.ljoin ("News")


def module_info (req=None):
	if req: return
	return {"order":1, "name": "News","headers": feeduri()}

def homepage_widget (req=None):
	if req: return
	return {"title": "News", "content": generate_page (0,0.3,False)}
