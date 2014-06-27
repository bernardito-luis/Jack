# =====================================================================================================================
import random
# we are going to add them
# they are 8. format is (y,x) though nvm
cell_neighbors = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]

def neighbor_is_treasure(island, cell_num):
    # some chance to skip this case
    if random.randrange(10) < 1:
        return False
    treasure_neigh = False
    for (coef_y, coef_x) in cell_neighbors:
        try:
            if island[cell_num + 11*coef_y + coef_x] in world_treasures:
                treasure_neigh = True
        except:
            pass
        if treasure_neigh:
            return True
    return False

    

# fill random with treasures
def add_treasures(island, treasures_list):
    candidate = 0
    treasures = treasures_list[:]
    # print treasures

    while treasures:
        not_a_right_place = True
        while not_a_right_place:
            candidate = random.randrange(121)
            not_a_right_place = (island[candidate] != '_') or (neighbor_is_treasure(island, candidate))

        # place a treasure
        island[candidate] = treasures.pop()
        
    return island

# map_count is used to count successful maps or smth on =\
def calculate_distances(island_o, possible_maps, treasures):
    #dbg
    dists = []
    island = island_o[:]
    island = add_treasures(island, treasures)
    # print island
    handicap = [0,0,0,0]
    treasures_map = []
    #print '~'*80
    for place in island:
        if place in treasures:
            # found a chest
            one_chest = (place, island.index(place))
            treasures_map.append(one_chest)
            #print "this", island.index(place), place
            y = (island.index(place))/11
            x = island.index(place) - y*11
            # mark a cell "counted"
            island[island.index(place)] = 'c'+place
            dists.append(max(abs(0-y),abs(5-x))+1)
            #print place[0]
            dist1 = float(place[0])/(max(abs(0-y),abs(5-x))+1)
            dist2 = float(place[0])/(max(abs(5-y),abs(10-x))+1)
            dist3 = float(place[0])/(max(abs(10-y),abs(5-x))+1)
            dist4 = float(place[0])/(max(abs(5-y),abs(0-x))+1)
            handicap[0] += dist1
            handicap[1] += dist2
            handicap[2] += dist3
            handicap[3] += dist4

    #print '~'*80


    # print "!!:", handicap
    value = max(handicap) - min(handicap)
    buffer_string = ""
    if (value) < 0.07:
        #print 'h', handicap
        #print 'd', dists
        
        
        treasures_map = sorted( treasures_map, key=lambda x: x[0])
        buf = tuple(treasures_map)
        # all_maps-variable is deprecated
        
        for elem in treasures_map:
            buffer_string += str(elem[0])+" "+str(elem[1])+" "
            
        #print "Success!!", value
    if buffer_string != "":
        print "Success!!"
        possible_maps.append(buffer_string)
        
    
# prepare template-map        
def prepare_pseudo():
    pseudo = []

    # empty pseudo
    for i in range(121):
        pseudo.append('_')

    # block corners
    pseudo[0] = 'b'
    pseudo[10] = 'b'
    pseudo[11*10] = 'b'
    pseudo[11*10+10] = 'b'
    
    return pseudo
# =====================================================================================================================


# world_treasures = ['3gn', '5cc', '4cc', '4cc', '3cc', '3cc', '3cc', '2cc',
                   # '2cc', '2cc', '2cc', '2cc', '1cc', '1cc', '1cc', '1cc',
                   # '1cc']

# world_old_treasures = ['5cc', '4cc', '4cc', '3cc', '3cc', '3cc', '2cc',
                       # '2cc', '2cc', '2cc', '2cc', '1cc', '1cc', '1cc', '1cc',
                       # '1cc']
