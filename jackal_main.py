# -*- coding: utf-8 -*-
import fix_path

import os
import urllib
import cgi
import json

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

# cron
from cron_tasks.map_generator import map_generator


DEFAULT_GUESTBOOK_NAME = 'not_default_guestbook'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook', guestbook_name)


class MainPage(webapp2.RequestHandler):
    def get(self):
    
#        self.response.write(json.dumps(['pics/1.jpg','pics/2.jpg'])
        
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        #creating template variables
            'json_data':  json.dumps(
                ['small_pics/wat.png', 'small_pics/trp.png', 'small_pics/em1.png', 'small_pics/fob.png', 'small_pics/pln.png', 'small_pics/msb.png', 'small_pics/esr.png', 'small_pics/ice.png', 'small_pics/3mc.png', 'small_pics/mfs.png', 'small_pics/wat.png', 'small_pics/msb.png', 'small_pics/3mc.png', 'small_pics/em1.png', 'small_pics/mtd.png', 'small_pics/cav.png', 'small_pics/frt.png', 'small_pics/2cc.png', 'small_pics/em1.png', 'small_pics/mss.png', 'small_pics/trp.png', 'small_pics/jng.png', 'small_pics/cnn.png', 'small_pics/4mc.png', 'small_pics/crd.png', 'small_pics/frt.png', 'small_pics/mds.png', 'small_pics/em1.png', 'small_pics/4cc.png', 'small_pics/mss.png', 'small_pics/ice.png', 'small_pics/mlk.png', 'small_pics/erq.png', 'small_pics/em1.png', 'small_pics/3mc.png', 'small_pics/crd.png', 'small_pics/drg.png', 'small_pics/crb.png', 'small_pics/1br.png', 'small_pics/trp.png', 'small_pics/3br.png', 'small_pics/1cc.png', 'small_pics/cnn.png', 'small_pics/ice.png', 'small_pics/mds.png', 'small_pics/mdb.png', 'small_pics/gnb.png', 'small_pics/jng.png', 'small_pics/msb.png', 'small_pics/3cc.png', 'small_pics/2cc.png', 'small_pics/crd.png', 'small_pics/ice.png', 'small_pics/mss.png', 'small_pics/pst.png', 'small_pics/em1.png', 'small_pics/crd.png', 'small_pics/1br.png', 'small_pics/fob.png', 'small_pics/4cc.png', 'small_pics/5cc.png', 'small_pics/cav.png', 'small_pics/mtd.png', 'small_pics/phs.png', 'small_pics/em1.png', 'small_pics/mfs.png', 'small_pics/cav.png', 'small_pics/3cc.png', 'small_pics/mfd.png', 'small_pics/5mc.png', 'small_pics/2mc.png', 'small_pics/2cc.png', 'small_pics/frd.png', 'small_pics/2cc.png', 'small_pics/mtd.png', 'small_pics/mfs.png', 'small_pics/1cc.png', 'small_pics/2cc.png', 'small_pics/em1.png', 'small_pics/mds.png', 'small_pics/ice.png', 'small_pics/em1.png', 'small_pics/ice.png', 'small_pics/em1.png', 'small_pics/em1.png', 'small_pics/bgn.png', 'small_pics/1cc.png', 'small_pics/3mc.png', 'small_pics/2br.png', 'small_pics/em1.png', 'small_pics/drg.png', 'small_pics/em1.png', 'small_pics/em1.png', 'small_pics/3gn.png', 'small_pics/3cc.png', 'small_pics/esr.png', 'small_pics/mfd.png', 'small_pics/1cc.png', 'small_pics/1br.png', 'small_pics/2mc.png', 'small_pics/em1.png', 'small_pics/jng.png', 'small_pics/em1.png', 'small_pics/4mc.png', 'small_pics/2mc.png', 'small_pics/em1.png', 'small_pics/em1.png', 'small_pics/2mc.png', 'small_pics/mdb.png', 'small_pics/esr.png', 'small_pics/wat.png', 'small_pics/mdb.png', 'small_pics/cav.png', 'small_pics/2mc.png', 'small_pics/esr.png', 'small_pics/mfd.png', 'small_pics/mlk.png', 'small_pics/ftu.png', 'small_pics/1cc.png', 'small_pics/2br.png', 'small_pics/wat.png']
            )
        }
        #self.response.write(template_values['json_data'])
        self.response.write("Welcome to Jackal balanced\n")

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Image(webapp2.RequestHandler):
    def get(self):
        greeting = db.get(self.request.get('img_id'))
        if greeting.avatar:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(greeting.avatar)
        else:
            self.response.out.write('No image')


class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')

        #greeting.put()
        self.redirect('/?' + urllib.urlencode(
            {'guestbook_name': guestbook_name}))


application = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/sign', Guestbook),
#        ('/cron_tasks/map_generator', MapGenerator),
], debug=True)