<!DOCTYPE HTML>
<html lang="en-US">
<head>
		<title>%(site_title)s &#8211; %(title)s</title>
		<meta charset="UTF-8">
		<meta name="description" content="%(desc)s"/>
		<meta name="viewport" content="width=device-width; initial-scale=1.0">
		<link rel="stylesheet" type="text/css" href="/static/yswd3.css" />
		%(headers)s
</head>

<body>
<div class='main'>
	<div id="header">
		<a style="float:left" href="%(site_prefix)s"><img width='128' height='96' src='/static/yswd.png' alt='logo'/></a>
		<div id="heading">%(site_title)s %(caption)s</div>
		<div style="margin-top: 4px"><span id='headersub'><em>%(site_desc)s</em></span></div>
	</div>
	<div class="menu_container">
		%(menu)s
	</div>
	<br/>
	<div class="content">
