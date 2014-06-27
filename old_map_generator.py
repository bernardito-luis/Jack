# -*- coding: utf-8 -*-

# ..................................................................................................................120
import webapp2
from google.appengine.ext import ndb


from generator_utils import *
# procedures, functions and so on to generate maps
# =====================================================================================================================
# we are going to add them

# they are 8. format is (y,x) though nvm
# cell_neighbors = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]

# def neighbor_is_treasure(island, cell_num):
    # treasure_neigh = False
    # for (coef_y, coef_x) in cell_neighbors:
        # try:
            # if island[cell_num + 11*coef_y + coef_x] in world_treasures:
                # treasure_neigh = True
        # except:
            # pass
        # if treasure_neigh:
            # return True
    # return False

    
world_treasures = ['3gn', '5cc', '4cc', '4cc', '3cc', '3cc', '3cc', '2cc',
                   '2cc', '2cc', '2cc', '2cc', '1cc', '1cc', '1cc', '1cc',
                   '1cc']

world_old_treasures = ['5cc', '4cc', '4cc', '3cc', '3cc', '3cc', '2cc',
                       '2cc', '2cc', '2cc', '2cc', '1cc', '1cc', '1cc', '1cc',
                       '1cc']

# # fill random with treasures
# def add_treasures(island, treasures_list):
    # candidate = 0
    # treasures = treasures_list

    # while treasures:
        # not_a_right_place = True
        # while not_a_right_place:
            # candidate = random.randrange(121)
            # not_a_right_place = (island[candidate] != '_') or (neighbor_is_treasure(island, candidate))

        # # place a treasure
        # island[candidate] = treasures.pop()

# # map_count is used to count successful maps or smth on =\
# def calculate_distances(island_o, possible_maps, treasures):
    # #dbg
    # dists = []
    # island = island_o[:]
    # add_treasures(island, treasures)
    # handicap = [0,0,0,0]
    # treasures_map = []
    # for place in island:
        # if place in world_treasures:
            # # found a chest
            # one_chest = (place, island.index(place))
            # treasures_map.append(one_chest)
            # #print "this", island.index(place), place
            # y = (island.index(place))/11
            # x = island.index(place) - y*11
            # # mark a cell "counted"
            # island[island.index(place)] = 'c'+place
            # dists.append(max(abs(0-y),abs(5-x))+1)
            # dist1 = float(place[0])/(max(abs(0-y),abs(5-x))+1)
            # dist2 = float(place[0])/(max(abs(5-y),abs(10-x))+1)
            # dist3 = float(place[0])/(max(abs(10-y),abs(5-x))+1)
            # dist4 = float(place[0])/(max(abs(5-y),abs(0-x))+1)
            # handicap[0] += dist1
            # handicap[1] += dist2
            # handicap[2] += dist3
            # handicap[3] += dist4


    # #print "!!:", handicap
    # value = max(handicap) - min(handicap)
    # buffer_string = ""
    # if (value) < 0.07:
        # #print 'h', handicap
        # #print 'd', dists
        
        
        # treasures_map = sorted( treasures_map, key=lambda x: x[0])
        # buf = tuple(treasures_map)
        # # all_maps-variable is deprecated
        
        # for elem in treasures_map:
            # buffer_string += str(elem[0])+" "+str(elem[1])+" "
            
        # #print "Success!!", value
    # if buffer_string != "":
        # print "Success!!"
        # possible_maps.append(buffer_string)
        
    
# # prepare template-map        
# def prepare_pseudo():
    # pseudo = []

    # # empty pseudo
    # for i in range(121):
        # pseudo.append('_')

    # # block corners
    # pseudo[0] = 'b'
    # pseudo[10] = 'b'
    # pseudo[11*10] = 'b'
    # pseudo[11*10+10] = 'b'
    
    # return pseudo
# =====================================================================================================================


def map_key(map_name='Map'):
    """Constructs a Datastore key for a map entity with map_name."""
    return ndb.Key('Map', map_name)


class TreasureMap(ndb.Model):
    map_id = ndb.IntegerProperty()
    info = ndb.StringProperty()
    
    # can become deprecated
    def add_map(self):
        map_query = TreasureMap.query(TreasureMap.map_id == 0)
        map_got = map_query.fetch(1)
        if int(map_got[0].info)/0xFFFF == 0:
            self.put()


class OldTreasureMap(ndb.Model):
    map_id = ndb.IntegerProperty()
    info = ndb.StringProperty()
    
    # can become deprecated
    def add_map(self):
        map_query = OldTreasureMap.query(OldTreasureMap.map_id == 0)
        map_got = map_query.fetch(1)
        if int(map_got[0].info)/0xFFFF == 0:
            self.put()


class OldMapGenerator(webapp2.RequestHandler):
    def get(self):
    
        map_query = OldTreasureMap.query(OldTreasureMap.map_id == 0)
        map_got = map_query.fetch(1)
        zero_record_exists = False
        try:
            # increase number of maps (deprecated)
            # map_got[0].info = str( int(map_got[0].info) + 1)
            # map_got[0].put()
            
            # very important print, it generates the exception
            print map_got[0].info
            # set the OK-flag
            zero_record_exists = True
            
            
        except (IndexError):
            # initialize database with a head record
            print "DB initialized"
            map = OldTreasureMap(parent=map_key())
            map.map_id = 0
            # head record info field has the following legend:
            #       [2bytes - pointer to the current map][2bytes - maps quantity]
            # besides it is a string %-)
            map.info = str(0x10000)
            map.put()
            
        if zero_record_exists:
            # maps that already exists
            cur_quantity = int(map_got[0].info) % 0x10000
            self.response.write('>>>>>>>>>>>>>>>>>>>> cur:' + str(cur_quantity))
            # create new map (deprecated)
            # map = TreasureMap(parent=map_key())
            # map.map_id = int(map_got[0].info)
            
            pseudo = prepare_pseudo()

            new_map = 'place new map-string here'
            possible_maps = []
            # 25 000 default
            for i in range(8):
                # print '01010230304'
                calculate_distances(pseudo, possible_maps, world_old_treasures)            

            # add maps if possible
            print possible_maps
            if len(possible_maps) != 0:
                for map_string in possible_maps:
                    # increase == add one map
                    cur_quantity += 1
                    map = OldTreasureMap(parent=map_key())
                    map.map_id = cur_quantity
                    map.info = map_string[:-1]
                    map.put()
                    if cur_quantity == 0xFFFF:
                        return
            
            #print "!!!!!!!!!!!!!!!!!!!!!!!!! map_got[0].info:", map_got[0].info
            map_got[0].info = str((int(map_got[0].info) / 0x10000)*0x10000 + cur_quantity)
            map_got[0].put()
            
            
application22 = webapp2.WSGIApplication([
        ('/cron_tasks/old_map_generator', OldMapGenerator),
], debug=True)

# if __name__ == '__main__':
    # run_wsgi_app(application2)
        