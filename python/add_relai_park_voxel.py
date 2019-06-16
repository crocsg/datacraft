# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# Dirt Visualisation Rennes is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 
import utm
import os
import sys
import requests
import math
import libminetest.map
import libminetest.utils
import minetest_util
from libminetest.utils import Pos
import voxelizer.stltovoxel



if __name__ == "__main__":


    print(sys.argv)
    print (len(sys.argv))

    if len (sys.argv) < 4:
        print ("usage script.py <map path> <stl path> floor_level[-30000,30000]")
        exit ()

    print (sys.argv[0])

    #x = int(sys.argv[1])
    #y = int(sys.argv[2])

    #print(x + y)

    mapfile = r"minetestutil_map.sqlite"
    mapdir = "./"
    mappath = os.path.join(mapdir, mapfile)
    mappath = sys.argv[1]
    print(mappath)

    stlfile = sys.argv[2]
    floorlevel = int(sys.argv[3])

    vol, boundingbox = voxelizer.stltovoxel.doVoxel(stlfile, "", 50)
    offset = [0,0,0]

    print (boundingbox)
    #exit ()

    db = libminetest.map.MapInterface(mappath)
    db.set_maxcachesize(2048)
    offset[0] = - (boundingbox[0] / 2)
    offset[1] = - (boundingbox[1] / 2)
    offset[2] = floorlevel
    print (offset)
    #for y in range(boundingbox[1]):
    #    for z in range(boundingbox[2]):
    #        for x in range(boundingbox[0]):
    #            if vol[z][x][y]:
    #                minetest_util.setblock(db, Pos(x, z + 10, y), minetest_util.claynode)

    db.save ()

    # center the map with 35238.geojson
    cx = 597691
    cy = 5329773

    # make parking request
    response = requests.get('https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-parcs-relais-du-reseau-star-en-temps-reel&facet=nom&facet=etat')
    data = response.json()
    print (data)
    print("######################### feature")

    for feature in data:
        print (feature)

    print("######################### record")
    for record in data['records']:
        #print (record)
        geometry = record['geometry']
        #print (geometry)
        fields = record['fields']
        #print (fields)
        print ('#################################################')
        print('id {0}'.format(fields['idparc']))
        print('nom {0}'.format(fields['nom']))
        print('position {0}'.format(fields['coordonnees']))
        print ('nb place dispo {0}'.format (fields['nombreplacesdisponibles']))
        print('capacite {0}'.format(fields['capaciteactuelle']))

        pospark = fields['coordonnees']
        print (pospark)

        cartpark = utm.from_latlon(pospark[0], pospark[1])
        #print (cartpark)

        parkx = int (cartpark[0] - cx)
        parky = int (cartpark[1] - cy)

        print (parkx, parky)

        capacite = fields['capaciteactuelle']
        dispo = fields['nombreplacesdisponibles']

        disporate = 0
        if capacite > 0:
            disporate = dispo/ capacite
        print (disporate * 100.0)

        startsignal = 1
        signal_height = 25
        signal_level = floorlevel + startsignal
        minetest_util.mark_totem(db, parkx, signal_level, parky, 2, signal_height, disporate, minetest_util.wgreennode, minetest_util.wrednode)


        parkoffset = [offset[0] + parkx, offset[1] + parky, floorlevel + 30]
        print (parkoffset)

        for y in range(boundingbox[1]):
            for z in range(boundingbox[2]):
                for x in range(boundingbox[0]):
                    lnode = minetest_util.wrednode
                    if z <= boundingbox[2] * disporate and disporate > 0.0:
                        lnode = minetest_util.wgreennode
                    if vol[z][x][y]:
                        minetest_util.setblock(db, Pos(x + parkoffset[0], z + parkoffset[2], y + parkoffset[1]), lnode)

        #display gauge
        gauge_rayon = 15
        gaugeoffset = [parkx, parky , 31 + boundingbox[2] + 3]
        minetest_util.lineblock(db, int(gaugeoffset[0] - gauge_rayon), int(gaugeoffset[1]), int(gaugeoffset[2] -1),
                                 int(gaugeoffset[0] + gauge_rayon), int(gaugeoffset[1]), int(gaugeoffset[2] -1),
                                 minetest_util.sandnode)
        for angl in range (0,180):
             radangl = math.radians(angl)
             x = math.cos(radangl) * gauge_rayon
             z = math.sin(radangl) * gauge_rayon
             y = 0

             minetest_util.setblock(db, Pos(int(x + gaugeoffset[0]), int(z + gaugeoffset[2]), int(y + gaugeoffset[1])), minetest_util.sandnode)
             lnode = minetest_util.wrednode
             if angl <= 180 * disporate and disporate > 0.0:
                 lnode = minetest_util.wgreennode
             for r in range (0, gauge_rayon):
                x = math.cos(radangl) * (r)
                z = math.sin(radangl) * (r)
                minetest_util.setblock(db, Pos(int(x + gaugeoffset[0]), int(z + gaugeoffset[2]), int(y + gaugeoffset[1])),
                                    lnode)

    db.save()
