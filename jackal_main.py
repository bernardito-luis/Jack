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

from map_generator import TreasureMap
from assemble_map import assemble
from info import textinfo


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

    
# =====================================================================================================================
# get a map from db (get a string abbreviation)
def get_map_str_abb():
    map_query = TreasureMap.query(TreasureMap.map_id == 0)
    map_got = map_query.fetch(1)
    # get current map number and quantuty
    cur_map_num = int(map_got[0].info) / 0x10000
    cur_map_quant = int(map_got[0].info) % 0x10000
    
    if cur_map_num == cur_map_quant:
        # move to the begining
        new_pointer = 0x10000+ cur_map_quant
    else:
        # increase pointer
        new_pointer = int(map_got[0].info) + 0x10000
    # move pointer
    map_got[0].info = str(new_pointer)
    map_got[0].put()

    # get that map
    map_query = TreasureMap.query(TreasureMap.map_id == cur_map_num)
    map_got = map_query.fetch(1)
    map_str = map_got[0].info
    
    return map_str
# =====================================================================================================================

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook', guestbook_name)


BUBLE = '0'
class MainPage(webapp2.RequestHandler):
    # pretends to be a debug method (clone of the global function)
    def c_get_map_str_abb(self):
        map_query = TreasureMap.query(TreasureMap.map_id == 0)
        map_got = map_query.fetch(1)
        # get current map number and quantuty
        cur_map_num = int(map_got[0].info) / 0x10000
        self.response.write("You are using map #" + str(cur_map_num) + "<br>")
        cur_map_quant = int(map_got[0].info) % 0x10000
        if cur_map_num == cur_map_quant:
            # move to the begining
            new_pointer = 0x10000+ cur_map_quant
        else:
            # increase pointer
            new_pointer = int(map_got[0].info) + 0x10000
        # move pointer
        map_got[0].info = str(new_pointer)
        map_got[0].put()

        # get that map
        map_query = TreasureMap.query(TreasureMap.map_id == cur_map_num)
        map_got = map_query.fetch(1)
        map_str = map_got[0].info
        
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

        return map_str


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

        # for dbg it is an outstanding string
        json_map = assemble(self.c_get_map_str_abb())
        self.response.write("Earthquake on cell -" + str(json_map.index('small_pics/erq.png')) + "-<br>")
        
        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        # text description for cells
            'json_cell_desc':  json.dumps([textinfo]),
        #creating template variables
            #'json_data':  json.dumps(assemble(get_map_str_abb()))
            'json_data':  json.dumps(json_map),
        }
        #self.response.write(template_values['json_data'])

        self.response.write("Welcome to Jackal balanced<br>")

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

        
class ToMainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/main")


class TestPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('test_page.html')
        self.response.write(template.render())


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
        ('/', ToMainPage),
        ('/test', TestPage),
        ('/main', MainPage),
        ('/sign', Guestbook),
#        ('/cron_tasks/map_generator', MapGenerator),
], debug=True)





# 1330-1002-1242-7054-4175-8247
