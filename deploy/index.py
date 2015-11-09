import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = '###YOUR_APP_NAME###.settings'  
application = get_wsgi_application()

