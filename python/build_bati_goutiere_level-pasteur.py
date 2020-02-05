#! python
# -*- encoding: utf-8 -*-
# jeu de données associé : https://data.rennesmetropole.fr/explore/dataset/constructions-baties/information/?refine.code_insee=35238&location=19,48.09221,-1.66381&basemap=0a029a
# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 

import sys
import utm
import math
import libminetest.map
import libminetest.utils
import pygeoj
import time
import os
from libminetest.nodes import Node
from libminetest.utils import Pos

import minetest_util




if __name__ == "__main__":
    mapfile = r"map.sqlite"
    mapdir = "./"
    mappath = os.path.join(mapdir, mapfile)
    print(mappath)

    print(sys.argv)
    print(len(sys.argv))

    if len(sys.argv) < 7:
        print("usage build_bati_goutiere_level-pasteur <map path> <geojson path> floor_level[-30000,30000] floor [0/1] prune[0/1] fill[0/1]")
        exit()

    mappath = sys.argv[1]
    geopath = sys.argv[2]
    floor_level = int(sys.argv[3])
    create_floor = int(sys.argv[4])
    prune = int(sys.argv[5])
    fill = int(sys.argv[6])

    #create block array
    db = libminetest.map.MapInterface (mappath)
    db.set_maxcachesize(2048)

    defnode = Node ("default:stone")
    dirtnode = Node ("default:dirt")
    claynode = Node ("default:clay")
    wrednode = Node('wool:red')
    wgreennode = Node('wool:green')
    wyellownode = Node('wool:yellow')

    #reading map info
    print ("reading map")
    testfile = pygeoj.load(geopath)

    print ("Map bounding box : {0}".format(testfile.bbox))

    startbox = utm.from_latlon(testfile.bbox[1], testfile.bbox[0])
    endbox = utm.from_latlon(testfile.bbox[3], testfile.bbox[2])
    print ("Mercator map bounding box : {0},{1}".format (startbox, endbox))

    centerbox = (startbox[0] + endbox[0]) / 2
    centerboy = (startbox[1] + endbox[1]) / 2

    print ("size =" + str(endbox[0] - startbox[0]) + " " + str(endbox[1] - startbox[1]))

    cx = int(centerbox)
    cy = int (centerboy)

    print ("map center in bloc : {0}, {1}".format (cx,cy))

    minx = 1000000
    miny = 1000000
    maxx = -1000000
    maxy = -1000000

    nbfeature = 0
    solbloc = 0
    start_time = time.time ()

    if (prune != 0):
        time.sleep(1)

    if create_floor > 0:
        print ("building floor...")

        chunk = 32
        for zg in range (int(startbox[1]), int(endbox[1]), chunk):
            for xg in range (int(startbox[0]), int(endbox[0]), chunk):
                for z in range(zg,zg+chunk):
                    for x in range (xg, xg+chunk):
                        if prune == 0:
                            minetest_util.setblock(db, Pos(int (x-cx), floor_level, int(z - cy)), minetest_util.dirtnode)
                        solbloc += 1
                        if solbloc % 8192 == 0:
                            print ("Z={0} blocs = {1} {2} blocs / s".format(z - cy, solbloc, solbloc / (time.time() - start_time)))
                            if prune == 0:
                                db.save()
    else:
        print ("skip floor building")

    print ("building shape")
    total_feature = len(testfile)
    for feature in testfile:
        #print(feature.geometry.type)
        #print(feature.geometry.coordinates)
        #print(feature.properties)


        if not 'h_faitage' in feature.properties:
            print(feature.geometry.type)
            print(feature.geometry.coordinates)
            print(feature.properties)
            print ("ERROR faitage not present")
            hfaitage = 1
            continue
        else:
            hfaitage = math.ceil(feature.properties['h_faitage'])
            print ('h faitage : {0}'.format(hfaitage))


        nbfeature = nbfeature + 1

        #if (nbfeature > 10):
        #    break

        for c in feature.geometry.coordinates:
            #print (c)

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

                #close polygon
                poly.append (poly[0])

                if prune == 0:
                    for alt in range (floor_level + 1, floor_level + 1 + hfaitage + 1):
                        if fill == 0:
                            for idx in range (len(poly) - 1):
                                minetest_util.lineblock(db, poly[idx][0], poly[idx][1], alt, poly[idx+1][0], poly[idx+1][1], alt, claynode)
                        else:
							if alt < floor_level + 1 + hfaitage:
								minetest_util.lineblock(db, poly[idx][0], poly[idx][1], alt, poly[idx+1][0], poly[idx+1][1], alt, claynode)
							else:	
								minetest_util.polygon_filled_block(db, poly, alt, claynode)

                #print ("done " + str(time.time() - start_time) + " sec | "+ str(nbfeature) + " feature | " + str (nbfeature / (time.time() - start_time) ) + " feature / sec  | "+ str(nbfeature * 100.0 / len(testfile)) + " % ")
                print ("{0} sec | feature {1} / {2} | {3} features / sec | polygon {5} | {4} % done".format (int(time.time() - start_time), nbfeature, total_feature, nbfeature / (time.time() - start_time), nbfeature * 100.0 / total_feature, len(poly)))
                if nbfeature % 250 == 0 and prune == 0:
                    db.save ()


    if prune == 0:
        db.save()


    print (minx)
    print (miny)
    print (maxx)
    print (maxy)
    print ("size")
    print (maxx - minx)
    print (maxy - miny)
    print("map center in bloc : {0}, {1}".format(cx, cy))