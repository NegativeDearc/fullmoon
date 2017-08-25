# coding=utf-8

import xml
from app import app
from flask import current_app

# 百度Sitemap协议支持三种格式：文本格式、xml格式、Sitemap索引格式,可以根据自己情况来选择任意一种格式组织sitemap。具体格式说明及示例如下：

# 1.第一种格式样例：txt文本格式
# 在一个txt文本列明需要向百度提交的链接地址，将txt文本文件通过站长平台进行提交    
# http://www.example.com/repaste/101562698_5230191316.html
# http://www.example.com/repaste/101586283_5230215075.html
# http://www.example.com/repaste/101639435_5230310576.html  

# 此文本文件需要遵循以下指南：
# · 文本文件每行都必须有一个网址。网址中不能有换行。
# · 不应包含网址列表以外的任何信息。
# · 您必须书写完整的网址，包括 http。
# · 每个文本文件最多可包含 50,000 个网址，并且应小于10MB（10,485,760字节）。如果网站所包含的网址超过 50,000 个，则可将列表分割成多个文本文件，然后分别添加每个文件。
# · 文本文件需使用 UTF-8 编码或GBK编码。  


# 2.第二种格式样例：xml格式
# 单个xml数据格式如下：
# <?xml version="1.0" encoding="utf-8"?>
# <!-- XML文件需以utf-8编码-->
# <urlset>
# <!--必填标签-->
#     <url>
#         <!--必填标签,这是具体某一个链接的定义入口，每一条数据都要用<url>和</url>包含在里面，这是必须的 -->
#         <loc>http://www.yoursite.com/yoursite.html</loc>
#         <!--必填,URL链接地址,长度不得超过256字节-->
#         <lastmod>2009-12-14</lastmod>
#         <!--可以不提交该标签,用来指定该链接的最后更新时间-->
#         <changefreq>daily</changefreq>
#         <!--可以不提交该标签,用这个标签告诉此链接可能会出现的更新频率 -->
#         <priority>0.8</priority>
#         <!--可以不提交该标签,用来指定此链接相对于其他链接的优先权比值，此值定于0.0-1.0之间-->
#     </url>
#     <url>
#         <loc>http://www.yoursite.com/yoursite2.html</loc>
#         <lastmod>2010-05-01</lastmod>
#         <changefreq>daily</changefreq>
#         <priority>0.8</priority>
#     </url>
# </urlset>
# 上述Sitemap向百度提交了一个url:http://www.yoursite.com/yoursite.html 


# 若有多条url，按照上述格式重复<url></url>之间的片断，列明所有url地址，打包到一个xml文件，向站长平台进行提交。


# 3.第三种格式样例：Sitemap索引格式
# 如需提交大量sitemap文件，则可将其列在sitemap索引文件中，然后将该索引文件提交。您无需分别提交每个文件。
# <?xml version="1.0" encoding="utf-8"?>
# <!-- XML文件需以utf-8编码-->
# <sitemapindex>
# <!--必填，以 <sitemapindex> 开始标记作为开始，以 </sitemapindex> 结束标记作为结束-->
#     <sitemap>
#         <!--必填，以<sitemap>标签提交一个子sitemap文件-->
#                     <loc>http://example.com/ext/xmlsitemap/add/201201/index_20120106.xml</loc>

#         <!--必填，识别sitemap的位置-->
#         <lastmod>2009-12-14</lastmod>
#         <!--选填，识别相对sitemap文件的修改时间-->
#     </sitemap>
#     <!--必填，标签闭合-->
# </sitemapindex>
# <!--必填，标签闭合-->

# 有多个Sitemap，按上述格式重复<sitemap></sitemap>之间的片断，列明所有Sitemap地址，向站长平台进行提交。
# http://flask.pocoo.org/snippets/108/
# todo:1 export article to .html/.md from database 2. generate sitemap.xml automatically

with app.app_context():
    print app.url_map
    for rule in app.url_map.iter_rules():
        print rule.methods, rule.rule