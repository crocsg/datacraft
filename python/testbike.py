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
import minetest_util
from libminetest.nodes import Node
from libminetest.utils import Pos

def createmap ():
    map = libminetest.map.MapVessel(r"./map.sqlite")
    map.create(r"./map.sqlite")
    ids = map.get_all_mapblock_ids()
    nids = len(ids)
    print(r"nb blocks")
    print(nids)
    map.empty_map()
    ids = map.get_all_mapblock_ids()
    nids = len(ids)
    print(r"nb blocks")
    print(nids)
    map.close()

def genmap (db):
    defnode = Node("default:stone")
    dirtnode = Node("default:dirt")
    bikenode = Node("bike:bike")

    for x in range(-40, 40):
        print(x)
        for z in range(-40, 40):

            try:
                minetest_util.setblock(db, Pos(x, 0, z), defnode)

            except libminetest.errors.IgnoreContentReplacementError:
                print("oops")
                pass
    for y in range(1, 50):
        minetest_util.setblock(db, Pos(0, y, 0), dirtnode)

    for v in range(-40, 40, 10):
        minetest_util.setblock(db, Pos(v, 1, v), bikenode)

    db.save()


if __name__ == "__main__":

    #createmap ()

    #create block array
    db = libminetest.map.MapInterface (r"./map.sqlite")

    #genmap(db)

    for u in range(-40, 40, 1):
        for v in range (-40, 40, 1):
            node = minetest_util.getblock (db, Pos(u,1,v))
            print (node.get_param0 ())
            print(node.get_param1())
            print(node.get_param2())

            if (node.get_name () != 'air' ):
                print (node)