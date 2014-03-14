import random
import webapp2

from google.appengine.ext import webapp
from google.appengine.ext.webapp2.util import run_wsgi_app


class MapGenerator(webapp2.RequestHandler):
    def get(self):
        pass
        
application2 = webapp2.WSGIApplcation([
        ('/cron_tasks/map_generator', MapGenerator),
], debug=True)
# if __name__ == '__main__':
    # run_wsgi_app(application)
        