# coding=utf-8

import xml
from app import app
from flask import current_app

# sitemap for baidu spyder
# <?xml version="1.0" encoding="UTF-8"?>
# <urlset>
# <url>
# <loc>网页地址</loc>
# <lastmod>2010-01-01</lastmod>
# <changefreq>daily</changefreq>
# <priority>1.0</priority>
# </url>
# </urlset>
# http://flask.pocoo.org/snippets/108/

with app.app_context():
    print app.url_map
    for rule in app.url_map.iter_rules():
        print rule.methods, rule.rule