# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# Dirt Visualisation Rennes is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 
import utm
import libminetest.map
import libminetest.utils
import pygeoj
import os
import sys
import requests
import minetest_util
from libminetest.utils import Pos




if __name__ == "__main__":


    print(sys.argv)
    print (len(sys.argv))

    if len (sys.argv) < 2:
        print ("usage script.py <map path>")
        exit ()

    print (sys.argv[0])
    print (sys.argv[1])
	
    #x = int(sys.argv[1])
    #y = int(sys.argv[2])

    #print(x + y)

    mapfile = r"minetestutil_map.sqlite"
    mapdir = "./"
    mappath = os.path.join(mapdir, mapfile)
    mappath = sys.argv[1]
    print(mappath)

    db = libminetest.map.MapInterface(mappath)
    db.set_maxcachesize(8192)

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
        print (cartpark)

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
        maxsignal = 25
        signal_level = 1
        minetest_util.mark_totem(db, parkx, signal_level, parky, 2, 25, disporate, minetest_util.wgreennode, minetest_util.wrednode)

    db.save()
