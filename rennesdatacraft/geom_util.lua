-- Dirt Visualisation Rennes (c) by S GODIN and 3HitCombo
--
-- Dirt Visualisation Rennes is licensed under a
-- Creative Commons Attribution-ShareAlike 4.0 International License.
-- You should have received a copy of the license along with this
-- work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

function sum_array(tabl)

	local sum = 0
	for index, valeur in ipairs(tabl) do
		sum = sum + valeur
	end
	return sum
end

function sum_array_pair(tabl)

	local sum = 0
	for index, valeur in pairs(tabl) do
		sum = sum + valeur
	end
	return sum
end

function distance2 (p1, p2)
	local distance = (p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) *  (p2.y - p1.y) + (p2.z - p1.z) * (p2.z - p1.z)
	return distance
end

function distance2_scale (p1, p2, sx, sy, sz)
	local distance = ((p2.x - p1.x) /sx) * ((p2.x - p1.x) / sx) + ((p2.y - p1.y) / sy) *  ((p2.y - p1.y) / sy) + ((p2.z - p1.z) / sz) * ((p2.z - p1.z) /sz) 
	return distance
end

function vector_center (vec1, vec2)
	local vec = {x=(vec1.x + vec2.x)/2, y=(vec1.y+vec2.y)/2, z=(vec1.z+vec2.z)/2}
	return vec
end

function clear_node_old (vec1,vec2)
	for y = vec1.y, vec2.y do
		for z = vec1.z, vec2.z do
			for x = vec1.x, vec2.x do
				minetest.swap_node ({x=x, y=y, z=z}, {name="air"})
			end
		end
	end
end

local c_air  = minetest.get_content_id("air")


function clear_node(pos1, pos2)
    -- Read data into LVM
    local vm = minetest.get_voxel_manip()
    local emin, emax = vm:read_from_map(pos1, pos2)
    local a = VoxelArea:new{
        MinEdge = emin,
        MaxEdge = emax
    }    
    local data = vm:get_data()

    -- Modify data
    for z = pos1.z, pos2.z do
        for y = pos1.y, pos2.y do
            for x = pos1.x, pos2.x do
                local vi = a:index(x, y, z)
				data[vi] = c_air
            end
        end
    end

    -- Write data
    vm:set_data(data)
    vm:write_to_map(true)
end
