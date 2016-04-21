#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'YiHan'
SITENAME = u'Yi\'s Blog  -  Do. Or do not. There is no try'
SITEURL = 'http://www.yilaguan.cc'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'

PLUGIN_PATHS = ['/u01/blog/plugins/pelican-plugins']
#PLUGINS = ['sitemap','disqus_static']
PLUGINS = ['sitemap']
SITEMAP = {
    'format': 'txt',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    }
}

KEYWORD = 'EBS，运维，开发, 生活随想, Oracle, Python'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
 ('rhettinger','https://rhettinger.wordpress.com/'),
('小明明','http://www.dongwm.com/'),
('keakon的涂鸦馆','http://www.keakon.net/'),
('织网','http://zheng-ji.info/'),

       
        )
# Social widget
SOCIAL = (('github 个人页','http://cooleasyhan.github.io'),
          )

DEFAULT_PAGINATION = 10

STATIC_PATHS = ['images', 'pdfs','robots.txt']

##########for buleidea##############


THEME = 'pelican-octopress-theme'

# Blogroll
LINKS 

# Social widget
SOCIAL

GITHUB_URL = 'https://github.com/cooleasyhan/'



MENUITEMS = (('Home', '/'),('Archives','/archives.html'))
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True


GITHUB_USER = 'cooleasyhan'


DISQUS_SITENAME = u'yilaguan'
#DISQUS_SECRET_KEY = u'82DN6UNrf8VQ4tsZDIJuChCPzskjpaWS4Ltx7PurqJsrqbT7raifLrzPPNSfLC4i'
#DISQUS_PUBLIC_KEY = u'YkTOi7B19v3mvkwFHi0zvpYu4A3vC1g0ZFusNPIXWKFxvG2r22fCNTxxGG2kgrai'



ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
