<!DOCTYPE HTML>
<html>
<head>
    <title>%(site_title)s &#8211; %(title)s</title>
    <meta name="description" content="%(desc)s"/>
    <link rel="stylesheet" type="text/css" href="/static/yswd2.css" />
    <script src="/static/sorttable.js" type="text/javascript" charset="UTF-8"></script>
    <script src="/static/jquery.js" type="text/javascript" charset="UTF-8"></script>
    <script type="text/javascript" src="/static/jquery.socialshareprivacy.min.js"></script>
    <script type="text/javascript">
      jQuery(document).ready(function($){
        $('.socialshareprivacy').socialSharePrivacy({
          services : {
            facebook : {
              txt_info: 'By enabling this button your data will be transmitted to facebook, even if you don\'t click the Like button afterwards.',
              language: 'en_US',
              action: 'like',
              dummy_img: "/static/socialshareprivacy/images/dummy_facebook.png"
            },
            twitter : {
                txt_info: 'By enabling this button your data will be transmitted to Twitter, even if you don\'t click the Tweet button afterwards',
                dummy_img: "/static/socialshareprivacy/images/dummy_twitter.png"
            },
            gplus : {
              txt_info: 'By enabling this button your data will be transmitted to Google, even if you don\'t +1 afterwards.',
              language: 'en',
              dummy_img: "/static/socialshareprivacy/images/dummy_gplus.png",
              perma_option: "on"
            }
          },
          txt_help: 'By enabling these buttons you enable data transmission to Facebook, Twitter and/or Google and agree to those data being used by them. Note that no data will be transmitted until you enable a button.',
          uri: function (context) {
            return $(context).parents(".news").find ("h3 a").attr("href");
          },
          css_path: "/static/socialshareprivacy/socialshareprivacy.css",
          settings_perma: "Permanently activate buttons."
        });
      });
    </script>
    %(headers)s
</head>

<body>
 <div style="margin:auto;min-width:640px;max-width:80%%">
 <div id="header">
   <a style="float:left" href="%(site_prefix)s"><img src='/static/yswd.png' alt='logo'/></a>
   <div id="heading">%(site_title)s %(caption)s</div>
   <div style="margin-top: 4px"><span id='headersub'><em>%(site_desc)s</em></span></div>
  </div>
<div class="menu_container" style="padding: 4px;margin-top: 4px">
%(menu)s
</div>
<div class="content">
