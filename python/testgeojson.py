# DataCraft Rennes (c) by S GODIN and 3HitCombo
#
# Dirt Visualisation Rennes is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
# 
import pygeoj
import utm
import os

#with open(r"I:\home\python\minetest\constructions-baties.geojson") as f:
#    gj = geojson.load(f)
#features = gj['features'][0]

#print(features)



#for t in gj['features']:
#    print (t['geometry'])

print ("Reading geo file")
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

cnt = 0
for feature in testfile:
    cnt +=1
    if cnt > 5:
        break
    print (cnt)
    print (feature.geometry.type)
    print (feature.geometry.coordinates)
    print (feature.properties)
    for c in feature.geometry.coordinates:
        for d in c:
            for e in d:
                poly = []
                print (e)
                poly.append(e)
