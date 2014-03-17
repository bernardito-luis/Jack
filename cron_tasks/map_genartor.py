import webapp2


def map_key(map_name='Map'):
    """Constructs a Datastore key for a map entity with map_name."""
    return ndb.Key('Map', map_name)

    
class TreasureMap(ndb.Model):
    map_id = ndb.IntegerProperty()
    info = ndb.IntegerProperty()
    
    def add_map(self):
        qry = TreasureMap.query(TreasureMap.map_id == 0)
        if qry/0xFFFF == 0:
            qry.info += 1
            self.put()


class MapGenerator(webapp2.RequestHandler):
    def get(self):
        map = TreasureMap(parent=map_key())
        qry = TreasureMap.query(TreasureMap.map_id == 0)
        if qry:
            map.map_id = qry.info + 1
            map.info = 0xACE
        else:
            map.map_id = 0
            map.info = 0
        map.add_map()
        
# application2 = webapp2.WSGIApplication([
        # ('/cron_tasks/map_generator', MapGenerator),
# ], debug=True)

# if __name__ == '__main__':
    # run_wsgi_app(application)
        