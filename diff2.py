    def c_get_map_str_abb(self):
        map_query = TreasureMap.query(TreasureMap.map_id == 0)
        map_got = map_query.fetch(1)
        # get current map number and quantuty
        cur_map_num = int(map_got[0].info) / 0x10000
        self.response.write(str(cur_map_num) + "<br>")
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
