# aliyun-ace-django-helper
helper sources for django aliyun deploy

require install
install nodejs for below tools
npm -g i cssmin
npm install uglify-js -g

uglifyjs/cssmin
in future we might support use less/sass processors

for the cache service
pip install alibaba-python-sdk


#CONTENTS:
PROVIDES usefull settings for deploy into a alibaba folder
deploy/deploy.sh

USAGE
./deploy.sh <target> [source]
deploy to <target> folder, copy all needed sources, collect static files, compress .js and .css files.
auto change {% static %} tag into something like
/static/
to use the static file service from ACE


common
common sources, now only have a connector for djnago to use alibaba OCS service

requirements.txt 
example file

static/admin
files extract from django admin site, copy rights belong to django project
http://djangoproject.com
