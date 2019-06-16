# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# Dirt Visualisation Rennes is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 
import sys


import libminetest.map
import libminetest.utils

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage create_empty_map <map path>")
        exit()
    mappath = sys.argv[1]

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
