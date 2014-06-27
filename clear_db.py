import webapp2
from google.appengine.ext import ndb
from map_generator import TreasureMap

class ClearDB(webapp2.RequestHandler):
    def get(self):

        # all_records = ndb.gql("SELECT * FROM TreasureMap")
        # all_records = all_records.fetch(500)
        # ndb.delete(all_records)
        # key = ndb.Key('Map', 'Map')
        # print key
        # maps = key.get()
        # print maps
        # maps.key.delete()
        ndb.delete_multi(TreasureMap.query().iter(keys_only=True))

        # for record in all_records:
            # record.delete()
    
application3 = webapp2.WSGIApplication([
        ('/other_tasks/clear_db', ClearDB),
], debug=True)
