
threehitbim.marker1 = {}
threehitbim.marker2 = {}
threehitbim.pos1 = {}
threehitbim.pos2 = {}
threehitbim.marker_region = {}
threehitbim.bim = {}

--worldedit.pos1 = {}
--worldedit.pos2 = {}

local function above_or_under(player, pnode)
	if player:get_player_control().sneak then
		return pnode.above
	else
		return pnode.under
	end
end

minetest.register_tool(":3hitbim:tool", {
	description = "Bim tool, Left-click to set 1st position, right-click to set 2nd",
	inventory_image = "tool.png",
	stack_max = 1, 				-- there is no need to have more than one
	liquids_pointable = true, 	-- ground with only water on can be selected as well

	on_use = function(itemstack, player, pointed_node) -- right click 
		print ("use tool")
		if player ~= nil and pointed_node ~= nil and pointed_node.type == "node" then
			local pname = player:get_player_name()
			threehitbim.pos1[pname] = above_or_under(player, pointed_node)
			threehitbim.tool_pos1(pname)
			
		elseif player ~= nil then
			print ("use on existing position")	
			-- count nodes by category
			local pname = player:get_player_name()
			
			local pos1 = threehitbim.pos1[pname]
			local pos2 = threehitbim.pos2[pname]
			
			if pos1 ~= nil and pos2 ~= nil then
			
				pos1, pos2 = threehitbim.sort_pos(pos1, pos2)
				
				local catsum = {}
				for k,v in pairs(threehitbim.categories) do
					catsum[v] = 0
				end
				
				for y = pos1.y,pos2.y do
					for z = pos1.z,pos2.z do
						for x = pos1.x,pos2.x do
							local node = minetest.get_node ({x=x,y=y,z=z})
							if node ~= nil then
								print (x,y,z,node.name)
								for k,v in pairs(threehitbim.categories) do
									for k1,v1 in pairs(v.bloc) do
										print (node.name, k1)
										if node.name == k1 then
											catsum[v] = catsum[v] + v1
										end
									end
								
								end
							end	
						end
					end
				end
				
				for k,v in pairs(threehitbim.categories) do
					print (v.name, catsum[v])
				end
				
				
				threehitbim.showform (pname , catsum) 
			end					
		end
		return itemstack 	
	end,

	on_place = function(itemstack, player, pointed_node) -- Left Click
		if player ~= nil and pointed_node ~= nil and pointed_node.type == "node" then
			local pname = player:get_player_name()
			threehitbim.pos2[pname] = above_or_under(player, pointed_node)
			threehitbim.tool_pos2(pname)
		end
		return itemstack 	
	end,
})

threehitbim.showform = function (pname , catsum)        
	local player = minetest.get_player_by_name (pname)

	if player ~= nil then
			
		local str = ""
		for k,v in pairs(threehitbim.categories) do
				--str = str .. v.name .. " " .. catsum[v] ..","
				str = str .. v.name .. "," .. catsum[v] .. ","
			end
				
		
		--str = table.concat (place,",")
		print (str)
		minetest.show_formspec(pname, 
			"threehitbim:form",
			"size[16,11]"..
			"no_prepend[]"..
			"real_coordinates[false]"..
			"bgcolor[#323232FF]"..
			"label[8,1;BIM]" ..
			--"hypertext[1,1;14,5;name;<big>text</big>]"..
			"image[7,1;3,3;bim.png]"..
			"textlist[1,3;14,5;Resultat;"..str.."]"..
			"tableoptions[border=true;background=#484848]"..
			"tablecolumns[text,width=35;text,width=16]"..
			"table[1,3;14,1;BIM;Catégorie,Note]"..
			--"label[1,3;Catégorie]" ..
			--"label[9,3;Note]" ..
			"tableoptions[background=#323232;border=true]"..
			"tablecolumns[text,width=35;text,width=16]"..
			"table[1,4;14,6;BIM;" .. str .. "]"..
			
			"button_exit[13,10;2,1;exit;Fin]")
			
	end
		
	return true, ""
end

--marks tool position 1
threehitbim.tool_pos1 = function(name)
	local pos1, pos2 = threehitbim.pos1[name], threehitbim.pos2[name]

	if pos1 ~= nil then
		--make area stay loaded
		local manip = minetest.get_voxel_manip()
		manip:read_from_map(pos1, pos1)
	end
	if threehitbim.marker1[name] ~= nil then --marker already exists
		threehitbim.marker1[name]:remove() --remove marker
		threehitbim.marker1[name] = nil
	end
	if pos1 ~= nil then
		--add marker
		threehitbim.marker1[name] = minetest.add_entity(pos1, "threehitbim:pos1")
		if threehitbim.marker1[name] ~= nil then
			threehitbim.marker1[name]:get_luaentity().player_name = name
		end
	end
	threehitbim.mark_region(name)
end

--marks worldedit region position 2
threehitbim.tool_pos2 = function(name)
	local pos1, pos2 = threehitbim.pos1[name], threehitbim.pos2[name]

	if pos2 ~= nil then
		--make area stay loaded
		local manip = minetest.get_voxel_manip()
		manip:read_from_map(pos2, pos2)
	end
	if threehitbim.marker2[name] ~= nil then --marker already exists
		threehitbim.marker2[name]:remove() --remove marker
		threehitbim.marker2[name] = nil
	end
	if pos2 ~= nil then
		--add marker
		threehitbim.marker2[name] = minetest.add_entity(pos2, "threehitbim:pos2")
		if threehitbim.marker2[name] ~= nil then
			threehitbim.marker2[name]:get_luaentity().player_name = name
		end
	end
	threehitbim.mark_region(name)
end

threehitbim.mark_region = function(name)
	local pos1, pos2 = threehitbim.pos1[name], threehitbim.pos2[name]

	if threehitbim.marker_region[name] ~= nil then --marker already exists
		--wip: make the area stay loaded somehow
		for _, entity in ipairs(threehitbim.marker_region[name]) do
			entity:remove()
		end
		threehitbim.marker_region[name] = nil
	end

	if pos1 ~= nil and pos2 ~= nil then
		local pos1, pos2 = threehitbim.sort_pos(pos1, pos2)

		local vec = vector.subtract(pos2, pos1)
		local maxside = math.max(vec.x, math.max(vec.y, vec.z))
		local limit = tonumber(minetest.setting_get("active_object_send_range_blocks")) * 16
		if maxside > limit * 1.5 then
			-- The client likely won't be able to see the plane markers as intended anyway,
			-- thus don't place them and also don't load the area into memory
			return
		end

		local thickness = 0.2
		local sizex, sizey, sizez = (1 + pos2.x - pos1.x) / 2, (1 + pos2.y - pos1.y) / 2, (1 + pos2.z - pos1.z) / 2

		--make area stay loaded
		local manip = minetest.get_voxel_manip()
		manip:read_from_map(pos1, pos2)

		local markers = {}

		--XY plane markers
		for _, z in ipairs({pos1.z - 0.5, pos2.z + 0.5}) do
			local marker = minetest.add_entity({x=pos1.x + sizex - 0.5, y=pos1.y + sizey - 0.5, z=z}, "threehitbim:region_cube")
			if marker ~= nil then
				marker:set_properties({
					visual_size={x=sizex * 2, y=sizey * 2},
					collisionbox = {-sizex, -sizey, -thickness, sizex, sizey, thickness},
				})
				marker:get_luaentity().player_name = name
				table.insert(markers, marker)
			end
		end

		--YZ plane markers
		for _, x in ipairs({pos1.x - 0.5, pos2.x + 0.5}) do
			local marker = minetest.add_entity({x=x, y=pos1.y + sizey - 0.5, z=pos1.z + sizez - 0.5}, "threehitbim:region_cube")
			if marker ~= nil then
				marker:set_properties({
					visual_size={x=sizez * 2, y=sizey * 2},
					collisionbox = {-thickness, -sizey, -sizez, thickness, sizey, sizez},
				})
				marker:setyaw(math.pi / 2)
				marker:get_luaentity().player_name = name
				table.insert(markers, marker)
			end
		end

		threehitbim.marker_region[name] = markers
	end
end

minetest.register_entity(":threehitbim:pos1", {
	initial_properties = {
		visual = "cube",
		visual_size = {x=1.1, y=1.1},
		textures = {"pos1.png", "pos1.png",
			"pos1.png", "pos1.png",
			"pos1.png", "pos1.png"},
		collisionbox = {-0.55, -0.55, -0.55, 0.55, 0.55, 0.55},
		physical = false,
	},
	on_step = function(self, dtime)
		if threehitbim.marker1[self.player_name] == nil then
			self.object:remove()
		end
	end,
	on_punch = function(self, hitter)
		self.object:remove()
		threehitbim.marker1[self.player_name] = nil
	end,
	on_rightclick = function(self, clicker)
		print ("on right click pos1")
	end,
})

minetest.register_entity(":threehitbim:pos2", {
	initial_properties = {
		visual = "cube",
		visual_size = {x=1.1, y=1.1},
		textures = {"pos2.png", "pos2.png",
			"pos2.png", "pos2.png",
			"pos2.png", "pos2.png"},
		collisionbox = {-0.55, -0.55, -0.55, 0.55, 0.55, 0.55},
		physical = false,
	},
	on_step = function(self, dtime)
		if threehitbim.marker2[self.player_name] == nil then
			self.object:remove()
		end
	end,
	on_punch = function(self, hitter)
		self.object:remove()
		threehitbim.marker2[self.player_name] = nil
	end,
})

minetest.register_entity(":threehitbim:region_cube", {
	initial_properties = {
		visual = "upright_sprite",
		visual_size = {x=1.1, y=1.1},
		textures = {"cube.png"},
		visual_size = {x=10, y=10},
		physical = false,
	},
	on_step = function(self, dtime)
		if threehitbim.marker_region[self.player_name] == nil then
			self.object:remove()
			return
		end
	end,
	on_punch = function(self, hitter)
		local markers = threehitbim.marker_region[self.player_name]
		
		if not markers then
			return
		end
		for _, entity in ipairs(markers) do
			entity:remove()
		end
		threehitbim.marker_region[self.player_name] = nil
	end,
})

--- Copies and modifies positions `pos1` and `pos2` so that each component of
-- `pos1` is less than or equal to the corresponding component of `pos2`.
-- Returns the new positions.
function threehitbim.sort_pos(pos1, pos2)
	pos1 = {x=pos1.x, y=pos1.y, z=pos1.z}
	pos2 = {x=pos2.x, y=pos2.y, z=pos2.z}
	if pos1.x > pos2.x then
		pos2.x, pos1.x = pos1.x, pos2.x
	end
	if pos1.y > pos2.y then
		pos2.y, pos1.y = pos1.y, pos2.y
	end
	if pos1.z > pos2.z then
		pos2.z, pos1.z = pos1.z, pos2.z
	end
	return pos1, pos2
end

