# -*- coding: utf-8 -*-

# Wariors of the night! Assemble!
from random import shuffle

# 3 symbols is a cell code number after is a quantity of a cell

map_legend = {
    'emp18': u'Пустое поле. Попрыгайте на полянке, порадуйтесь солнышку =)',

    'mss03': u'Передвижение по стрелке прямо',
    'mds03': u'Передвижение по стрелке диагонально',
    'msb03': u'Передвижение по стрелке прямо, выбор из 2х',
    'mdb03': u'Передвижение по стрелке диагонально, выбор из 2х',
    'mtd03': u'Передвижение по стрелке, выбор из 3х',
    'mfd03': u'Передвижение по стрелке диагонально, выбор из 4х',
    'mfs03': u'Передвижение по стрелке прямо, выбор из 4х',
    'mlk02': u'Ход конем!',
    'ice06': u'Лёд',
    'cav04': u'Пещера',
    'pln01': u'Самолет!',
    'cnn02': u'Пушка',
    'fob02': u'Воздушный шар',

    '2mc05': u'Клетка, по которой надо топать 2 хода, если только не..',
    '3mc04': u'Клетка, по которой надо топать 3 хода, если только не..',
    '4mc02': u'Клетка, по которой надо топать 4 хода, если только не..',
    '5mc01': u'Клетка, по которой надо топать 5 хода, если только не..',

    '5cc': 'Сuундук с пятью золотыми!!!',
    '4cc': 'Сuундук с четырьмя золотыми!!',
    '3cc': 'Сuундук с тремя золотыми!',
    '2cc': 'Сuундук с двумя золотыми',
    '1cc': 'Сuундук с одним золотым',
    'sgn': 'Сuокровища испанского галеона! Скорее тащи!!!',

    '1br03': u'1 бутылка рома',
    '2br02': u'2 бутылочки рома',
    '3br01': u'3 прекрасных бутылочки рома',

    'trp03': u'Ловушка!',
    'crd04': u'Крокодил!',
    'gnb01': u'Людоед!!',
    'frt02': u'Форт =)',
    'ftu01': u'Форт с аборигеночкой ;)',
    'crb01': u'Каррамба!',
    'phs01': u'Маяк',
    'bgn01': u'К Вам присоединятеся Бен Ган',
    'pst01': u'К Вам присоединятеся священник',
    'frd01': u'К Вам присоединятеся Пятница, это ведь лучше чем понедельник?)',
    'esr04': u'Ром, тот, что нельзя забрать с собой',
    'erq01': u'Землетрясение!',
    'jng03': u'Джунгли -_-',
    'drg02': u'Конопля %-)',

}

# cur_map defines where the treasures are. meanwhile it is a string like '1cc 7 1cc 19 1cc 48 1cc 71 ...'
def assemble(cur_map):
    # split the treasures-string make list
    cur_map_list = cur_map.split(' ')
    
    # other cells to be added
    cells_to_add = []
    for k in map_legend.keys():
        # exclude treasures
        if (k == 'sgn') or (k[1]+k[2] == 'cc'):
            continue
        for i in range(int(k[-2]+k[-1])):
            cells_to_add.append(k)

    shuffle(cells_to_add)


    # create empty island
    island = []
    for i in range(121):
        island.append('_')

    # block corners
    island[0] = 'wlu.png'
    island[10] = 'wru.png'
    island[11*10] = 'wld.png'
    island[11*10+10] = 'wrd.png'

    # place gold
    buf = '~_^'
    even = True
    for i in cur_map_list:
        if even:
            buf = i
            even = False
        else:
            # check if the cell is really empty
            if island[int(i)] == '_':
                island[int(i)] = buf
            else:
                print 'An error occurred. Attempt to fill not an empty field'
                break
            even = True



    # place other
    # bad decision?
    for i in range(121):
        if island[i] == '_':
            island[i] = cells_to_add.pop()
            
    # generate json-suit list
    json_list = []    
    for cell in island:
        if cell[:3] == "emp":
            json_list.append('small_pics/em1.png')
            continue
            
        json_list.append('small_pics/'+cell[:3]+'.png')

    
    return json_list
    