#! python
# -*- encoding: utf-8 -*-
# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# Dirt Visualisation Rennes is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 
import math
import utm
import libminetest.map
import libminetest.utils
import pygeoj
import numpy as np
import time
import os
from libminetest.nodes import Node
from libminetest.utils import Pos
from bresenham import bresenham

def setblock (dbmap, nodepos, node):
    mapblock = libminetest.utils.determineMapBlock(nodepos)
    mapblockpos = libminetest.utils.getMapBlockPos(mapblock)
    bexist = db.check_for_pos(mapblockpos)
    # print (bexist)
    # print(type(bexist))
    if not bexist:
        db.init_mapblock(mapblockpos)
    # db.init_mapblock(libminet)
    try:
        db.set_node(nodepos, node)
    except libminetest.errors.IgnoreContentReplacementError:
        print("oops")
        pass

def lineblock (dbmap, from_x, from_y, from_z, to_x,to_y,to_z, node):
    point = bresenham(from_x, from_y, to_x, to_y)
    for pt in point:
        setblock (dbmap, Pos (pt[0], from_z, pt[1]), node)


mapfile = r"map.sqlite"
mapdir = "./"
mappath = os.path.join (mapdir, mapfile)
print (mappath)
if __name__ == "__main__":

    map = libminetest.map.MapVessel(mappath)
    map.create(mappath)
    ids = map.get_all_mapblock_ids()
    nids = len(ids)
    print (r"nb blocks")
    print (nids)
    map.empty_map()
    ids = map.get_all_mapblock_ids()
    nids = len(ids)
    print(r"nb blocks")
    print(nids)
    map.commit()
    map.close()


    #create block array
    db = libminetest.map.MapInterface (mappath)
    db.set_maxcachesize(8192)

    defnode = Node ("default:stone")
    dirtnode = Node ("default:dirt")
    claynode = Node ("default:clay")

    #reading map info
    print ("reading map")
    testfile = pygeoj.load(r"./referentiel-batiment_35238.geojson")

    print (testfile.bbox )

    startbox = utm.from_latlon(testfile.bbox[1], testfile.bbox[0])
    endbox = utm.from_latlon(testfile.bbox[3], testfile.bbox[2])
    print (startbox)
    print (endbox)

    centerbox = (startbox[0] + endbox[0]) / 2
    centerboy = (startbox[1] + endbox[1]) / 2

    print ("size =" + str(endbox[0] - startbox[0]) + " " + str(endbox[1] - startbox[1]))

    cx = int(centerbox)
    cy = int (centerboy)

    print (cx)
    print (cy)

    minx = 1000000
    miny = 1000000
    maxx = -1000000
    maxy = -1000000

    nbfeature = 0
    solbloc = 0
    start_time = time.time ()

    print ("construction du sol")

    chunk = 32
    for zg in range (int(startbox[1]), int(endbox[1]), chunk):
        for xg in range (int(startbox[0]), int(endbox[0]), chunk):
            for z in range(zg,zg+chunk):
                for x in range (xg, xg+chunk):
                    setblock(db, Pos(int (x-cx), 0, int(z - cy)), dirtnode)
                    solbloc += 1
                    if solbloc % 8192 == 0:
                        print ("Z={0} blocs = {1} {2} blocs / s".format(z - cy, solbloc, solbloc / (time.time() - start_time)))
                        db.save()


    for feature in testfile:
        #print(feature.geometry.type)
        #print(feature.geometry.coordinates)
        #print(feature.properties)

        nbfeature = nbfeature + 1
        if (nbfeature > 1000):
            break

        for c in feature.geometry.coordinates:
            for d in c:
                poly = []
                for e in d:
                    #print(e)
                    #a = get_cartesian(e[1],e[0])
                    a = utm.from_latlon(e[1],e[0])
                    poly.append( (int(a[0] - cx), int(a[1] - cy)) )
                    #print (a)
                    minx = min(minx, int(a[0]) - cx)
                    miny = min (miny, int(a[1]) - cy)
                    maxx = max (maxx, int(a[0]) - cx)
                    maxy = max (maxy, int(a[1]) - cy)

                #print ("polygon")
                #print (poly)

                for idx in range (len(poly) - 1):
                    lineblock(db, poly[idx][0], poly[idx][1], 1, poly[idx+1][0], poly[idx+1][1], 1, claynode)
                print ("done " + str(time.time() - start_time) + " sec "+ str(nbfeature) + " feature " + str (nbfeature / (time.time() - start_time) ) + " feature / sec  "+ str(nbfeature * 100.0 / len(testfile)))

    db.save()
    print (minx)
    print (miny)
    print (maxx)
    print (maxy)
    print ("size")
    print (maxx - minx)
    print (maxy - miny)
