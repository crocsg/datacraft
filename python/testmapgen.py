#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# Dirt Visualisation Rennes is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 

import libminetest.map

import libminetest.utils

from libminetest.nodes import Node
from libminetest.utils import Pos


if __name__ == "__main__":

    map = libminetest.map.MapVessel(r"./map.sqlite")
    map.create(r"./map.sqlite")
    ids = map.get_all_mapblock_ids()
    nids = len(ids)
    print (r"nb blocks")
    print (nids)
    map.empty_map()
    ids = map.get_all_mapblock_ids()
    nids = len(ids)
    print(r"nb blocks")
    print(nids)
    map.close()


    #create block array
    db = libminetest.map.MapInterface (r"./map.sqlite")

    defnode = Node("default:stone")
    dirtnode = Node("default:dirt")

    for x in range (-100,100):
        print(x)
        for z in range (-100,100):
            mapblock = libminetest.utils.determineMapBlock(Pos(x,0,z))
            mapblockpos = libminetest.utils.getMapBlockPos(mapblock)

            #print (mapblockpos)
            #print (type(mapblockpos))

            bexist = db.check_for_pos(mapblockpos)
            #print (bexist)
            #print(type(bexist))
            if not bexist:
                db.init_mapblock(mapblockpos)
            #db.init_mapblock(libminet)
            try:
                db.set_node(Pos(x,0,z), defnode)
            except libminetest.errors.IgnoreContentReplacementError:
                print ("oops")
                pass
    for y in range (1,500):
        mapblock = libminetest.utils.determineMapBlock(Pos(0, y, 0))
        mapblockpos = libminetest.utils.getMapBlockPos(mapblock)

        # print (mapblockpos)
        # print (type(mapblockpos))

        bexist = db.check_for_pos(mapblockpos)
        # print (bexist)
        # print(type(bexist))
        if not bexist:
            db.init_mapblock(mapblockpos)
        # db.init_mapblock(libminet)
        try:
            db.set_node(Pos(0, y, 0), dirtnode)
        except libminetest.errors.IgnoreContentReplacementError:
            print("oops")
            pass
    db.save()

