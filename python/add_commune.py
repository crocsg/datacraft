#! python
# -*- encoding: utf-8 -*-
# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# Dirt Visualisation Rennes is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 
import sys
import math
import utm
import libminetest.map
import libminetest.utils
import pygeoj
import time
import os
import minetest_util
from libminetest.nodes import Node
from libminetest.utils import Pos


def build_soil (soil_startbox, soil_endbox, floor_levelz, node, stime):
    print ("construction du sol")
    chunk = 32
    solbloc = 0
    for zg in range (int(soil_startbox[1]), int(soil_endbox[1]), chunk):
        for xg in range (int(soil_startbox[0]), int(soil_endbox[0]), chunk):
            for z in range(zg,zg+chunk):
                for x in range (xg, xg+chunk):
                    minetest_util.setblock(db, Pos(int (x-cx), floor_levelz, int(z - cy)), node)
                    solbloc += 1
                    if solbloc % 8192 == 0:
                        print ("Z={0} blocs = {1} {2} blocs / s".format(z - cy, solbloc, solbloc / (time.time() - stime)))
                        db.save()




if __name__ == "__main__":

    print(sys.argv)
    print(len(sys.argv))

    if len(sys.argv) < 5:
        print("usage script.py <map path> <geojson path> floor_level[-30000,30000] floor[0/1]")
        exit()

    print(sys.argv[0])
    print(sys.argv[1])

    mapfile = r"map.sqlite"
    mapdir = "./"
    mappath = os.path.join(mapdir, mapfile)
    mapscale = 30
    mappath = sys.argv[1]
    geojsonpath = sys.argv[2]
    floor_level = int (sys.argv[3])
    build_floor =  int (sys.argv[4])

    print("map : {0}".format (mappath))
    print("geojson : {0}".format(geojsonpath))
    print ("floor level : {0}".format (floor_level))

    #create block array
    db = libminetest.map.MapInterface (mappath)
    db.set_maxcachesize(2048)


    #reading map info
    print ("reading map")
    testfile = pygeoj.load(geojsonpath)

    print (testfile.bbox )

    startbox = utm.from_latlon(testfile.bbox[1], testfile.bbox[0])
    endbox = utm.from_latlon(testfile.bbox[3], testfile.bbox[2])

    scale_startbox = (startbox[0] / mapscale, startbox[1] / mapscale)
    scale_endbox = (endbox[0] / mapscale, endbox[1] / mapscale)

    print (startbox)
    print (endbox)
    print(scale_startbox)
    print(scale_endbox)

    centerbox = (scale_startbox[0] + scale_endbox[0]) / 2
    centerboy = (scale_startbox[1] + scale_endbox[1]) / 2

    print ("size =" + str(scale_endbox[0] - scale_startbox[0]) + " " + str(scale_endbox[1] - scale_startbox[1]))

    cx = int(centerbox)
    cy = int (centerboy)

    print (cx)
    print (cy)

    minx = 1000000
    miny = 1000000
    maxx = -1000000
    maxy = -1000000

    nbfeature = 0



    start_time = time.time ()

    if build_floor != 0:
        build_soil(scale_startbox, scale_endbox, floor_level, minetest_util.dirtnode, start_time)


    start_time = time.time()

    for feature in testfile:
        print(feature.geometry.type)
        print(feature.geometry.coordinates)
        print(feature.properties)

        nbfeature = nbfeature + 1
        print (feature.properties['nom'])
        print(feature.properties['code_insee'])
        print(feature.properties['geo_point_2d'])

        if feature.properties['nom'] != 'Rennes':
            continue


        center_commune_geo2d = feature.properties['geo_point_2d']
        t = utm.from_latlon(center_commune_geo2d [0],center_commune_geo2d [1])
        center_commune = ((int((t[0] / mapscale) - cx), int((t[1] / mapscale) - cy)))
        print ("center commune : {0}".format (center_commune))

        # minetest_util.lineblock(db, center_commune[0] - 50, center_commune[1] - 50, floor_level + 1,
        #                         center_commune[0] + 50, center_commune[1] - 50, floor_level + 1, minetest_util.wrednode)
        # minetest_util.lineblock(db, center_commune[0] + 50, center_commune[1] - 50, floor_level + 1,
        #                         center_commune[0] + 50, center_commune[1] + 50, floor_level + 1, minetest_util.wrednode)
        # minetest_util.lineblock(db, center_commune[0] + 50, center_commune[1] + 50, floor_level + 1,
        #                         center_commune[0] - 50, center_commune[1] + 50, floor_level + 1, minetest_util.wrednode)
        # minetest_util.lineblock(db, center_commune[0] - 50, center_commune[1] + 50, floor_level + 1,
        #                         center_commune[0] - 50, center_commune[1] - 50, floor_level + 1, minetest_util.wrednode)
        #
        # for z in range (floor_level + 1, floor_level + 10):
        #     minetest_util.setblock(db, Pos (center_commune[0], z, center_commune[1]), minetest_util.wgreennode)

        for c in feature.geometry.coordinates:
            poly = []
            for e in c:
                a = utm.from_latlon(e[1],e[0])
                tx = int(a[0] / mapscale) - cx
                ty = int(a[1] / mapscale) - cy
                poly.append( (tx ,ty) )

                minx = min(minx, tx)
                miny = min (miny, ty)
                maxx = max (maxx, tx)
                maxy = max (maxy, ty)

            #print ("polygon")
            #print (poly)

            for idx in range (len(poly) - 1):
                minetest_util.lineblock(db, poly[idx][0], poly[idx][1], floor_level + 1, poly[idx + 1][0], poly[idx + 1][1], floor_level + 1, minetest_util.claynode)
            print ("done " + str(time.time() - start_time) + " sec "+ str(nbfeature) + " feature " + str (nbfeature / (time.time() - start_time) ) + " feature / sec  "+ str(nbfeature * 100.0 / len(testfile)))

    db.save()
    print (minx)
    print (miny)
    print (maxx)
    print (maxy)
    print ("size")
    print (maxx - minx)
    print (maxy - miny)
