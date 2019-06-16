#! python
# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# Dirt Visualisation Rennes is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 

import os
import libminetest.map
import libminetest.utils
import libminetest.errors
from libminetest.nodes import Node
from libminetest.utils import Pos
from bresenham import bresenham


def setblock(dbmap: libminetest.map.MapInterface, nodepos: Pos, node: Node):
    """
    Set a node at nodepos position (minetest coord)
    :param dbmap: libminetest.map.MapInterface to sqlite minetest map
    :param nodepos: position
    :param node: node
    :return:
    """
    mapblock = libminetest.utils.determineMapBlock(nodepos)
    mapblockpos = libminetest.utils.getMapBlockPos(mapblock)
    bexist = dbmap.check_for_pos(mapblockpos)
    if not bexist:
        dbmap.init_mapblock(mapblockpos)
    try:
        dbmap.set_node(nodepos, node)
    except libminetest.errors.IgnoreContentReplacementError:
        print("oops")
        pass


def lineblock(dbmap: libminetest.map.MapInterface, from_x: object, from_y: object, from_z: object, to_x: object,
              to_y: object, to_z: object, node: Node):
    """
    Draw a line of bloc in the map beetween (from_x, from_y) and (to_x, to_y) at from_z altitude
    :param dbmap: libminetest.map.MapInterface to sqlite minetest map
    :param from_x: from X bloc position
    :param from_y: from Y bloc position
    :param from_z: from Z bloc position
    :param to_x: to X bloc position
    :param to_y: to Y bloc position
    :param to_z: to Z bloc position
    :param node: bloc identification to use

    """
    point = bresenham(from_x, from_y, to_x, to_y)
    for pt in point:
        setblock(dbmap, Pos(pt[0], from_z, pt[1]), node)


def mark_totem(dbmap, posx, posy, posz, width, height, rate, node, nodeempty):
    for y in range(posy, posy + height + 1):
        for x in range(posx - width, posx + width):
            for z in range(posz - width, posz + width):
                lnode = nodeempty
                if y - posy <= height * rate and rate > 0.0:
                    lnode = node
                setblock(dbmap, Pos(x, y, z), lnode)


defnode = Node("default:stone")
dirtnode = Node("default:dirt")
claynode = Node("default:clay")
glassnode = Node("default:glass")
wgreennode = Node('wool:green')
wrednode = Node('wool:red')
glassnode = Node('default:glass')
sandnode = Node('default:sandstone')
airnode = Node ('air')

if '__main__' == __name__:
    mapfile = r"minetestutil_map.sqlite"
    mapdir = "./"
    mappath = os.path.join(mapdir, mapfile)
    print(mappath)
    print(__name__)
    mmap = libminetest.map.MapVessel(mappath)
    mmap.create(mappath)
    ids = mmap.get_all_mapblock_ids()
    nids = len(ids)
    print(r"nb blocks")
    print(nids)
    mmap.empty_map()
    ids = mmap.get_all_mapblock_ids()
    nids = len(ids)
    print(r"nb blocks")
    print(nids)
    mmap.commit()
    mmap.close()

    db = libminetest.map.MapInterface(mappath)
    db.set_maxcachesize(2048)

    lineblock(db, 10, 10, 20, -10, 10, 20, dirtnode)
    lineblock(db, -10, 10, 20, -10, -10, 20, dirtnode)
    lineblock(db, -10, -10, 20, 10, -10, 20, dirtnode)
    lineblock(db, 10, -10, 20, 10, 10, 20, dirtnode)
    lineblock(db, 10, 10, 20, -10, -10, 20, defnode)

    for ix in range(-10, 10):
        for iz in range(-10, 10):
            setblock(db, Pos (ix, 0, iz), claynode)

    db.save()
