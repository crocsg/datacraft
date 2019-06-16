-- Dirt Visualisation Rennes (c) by S GODIN and 3HitCombo
--
-- Dirt Visualisation Rennes is licensed under a
-- Creative Commons Attribution-ShareAlike 4.0 International License.
-- You should have received a copy of the license along with this
-- work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

minetest.set_timeofday(0.3) -- morning time

dofile(minetest.get_modpath("rennesdatacraft") .. "/geom_util.lua")

local http_api = minetest.request_http_api()
print ("http_api ", http_api)
local texture_name = {"default:leaves",
                        "default:stone_with_iron", 
                        "default:stone",
                        "default:sandstone",
                        "default:clay",
                        "default:cloud",
                        "default:brick",
                        "stairs:slab_brick",
                        "stairs:slab_stone",
                        "default:nyancat_rainbow"
                        }
local matiere_texture = {
        friture = "default:desert_stone_block",
        Pneumatiques = "default:stone_block",
        verts = "default:leaves",
        Plâtre = "default:clay",
        Ferrailles = "basic_materials:chain_steel",
        Réemploi = "default:stone",
        venant = "default:sandstone",
        Incinérables = "default:torch",
        vidange = "default:permafrost",
        Textiles = "wool:cyan",
        Batteries = "default:coral_orange",
        Souches = "default:wood",
        Gravats = "default:gravel",
        Cartons = "default:tinblock",
        Bois = "default:acacia_bush_stem",
        DDS = "default:sandstone_block",
        Amiante = "default:dirt_with_rainforest_litter",
        Mobilier = "default:bookshelf",
        DEEE = "default:furnace",
        Piles = "default:diamondblock",
        Cartouches = "default:bronzeblock"
		}
local floor_level= 10000

if not http_api then
   print("ERROR: in minetest.conf, this mod must be in secure.http_mods!")
end



minetest.register_chatcommand("pos", {
	params = "",
	description = "Send text to chat",
	privs = {talk = false},
	func = function( pname , text)        
		minetest.chat_send_all("Get player position")
		local player = minetest.get_player_by_name (pname)
		if player ~= nil then
			local pos = player:get_pos()
			minetest.chat_send_all (tostring(pos.x) .. " " .. tostring(pos.y) .. " " .. tostring(pos.z))
		end
		
		return true, "Cmd end"
	end
})

function datacraft_build_dirt_viz (x1,z1,x2,z2, ypos, height, data, data_percent, data_name, block_name)
	local width = x2 - x1
	local length = z2 - z1
	
	local start = z1
	local maxv =0
	for idx, value in ipairs(data_percent) do
		if value > maxv then
			maxv = value
		end
	end	
	
	for idx, value in ipairs(data_percent) do
		local dirt_length = length * value
		local center = {x= (x1 + x2) / 2, y = ypos, z = start + dirt_length / 2}
		local rayon = math.abs(width) / 2
		local scalez = (dirt_length /2)/rayon
		local scaley = height * (value / maxv) / rayon / 2
		
		print (dump(center))
		print (rayon)
		print (rayon * scaley)
		print (rayon * scalez)
		dome_scale (center.x, center.y, center.z, rayon, 1, scaley, scalez, block_name[idx])
		start = start + dirt_length
	end
	
end

function datacraft_build_heap_viz (x1,y1,z1, width, length, height, ratio, blockname)

	local maxv = 5
	local rayon = math.abs(width) / 2
	local scalez = ratio * maxv
	local scalex = ratio * 5
	local scaley = ratio * 3
	dome_scale (x1 + length / 2, y1, z1 + width / 2, rayon, scalex, scaley, scalez, blockname)
end

minetest.register_chatcommand("test_data_dirt_rennes", {
	params = "",
	description = "build dirt viz",
	privs = {talk = false},
	func = function( _ , text)        
		minetest.chat_send_all("Récupération des dechets en cours ...")
		print ("Récupération des dechets en cours ...")
		print (http_api)
        http_api.fetch({
            url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=matieres-collectees-en-decheteries-et-plateformes-de-vegetaux-a-rennes-metropole&rows=500&facet=site&facet=annee&facet=matiere&refine.annee=2017",
            timeout = 50
         }, function (res)
        local text =  dump(res.data)
		print (text)
        local data2 = minetest.parse_json(text)
        data2 = minetest.parse_json(data2)
        print (dump(data2))
        local data = {}
		local data_name = {}
        
		print (data2.records)
		print (dump(data2.records))
		local dirt_value = {}
		for i=1,table.getn(data2.records) do
			if data2.records[i].fields.annee == '2017' then
				if string.find (data2.records[i].fields.site, 'RENNES') ~= nil then
					minetest.chat_send_all(data2.records[i].fields.matiere)
					print ("matiere ", data2.records[i].fields.matiere)
					print ("tonnage ", data2.records[i].fields.tonnage)
					if dirt_value[data2.records[i].fields.matiere] == nil then
						dirt_value[data2.records[i].fields.matiere] = 0
					end
					
					dirt_value[data2.records[i].fields.matiere] = dirt_value[data2.records[i].fields.matiere] + data2.records[i].fields.tonnage
				end
			end
		end
		print (dump(dirt_value))
		
		
		local center_map_x = 84
		local center_map_z = -30
		
		local dump_length = 20
		local dump_width = 20
		local dump_nb = 5
		
		local sum_dirt = sum_array_pair(dirt_value)
		print (sum_dirt)
		local sum = 0
		
		print ("dirt values")
		for index, valeur in pairs(dirt_value) do
			print (index, valeur)
		end
		
	
		local dirt_ratio = {}
		for index, valeur in pairs(dirt_value) do
			dirt_ratio[index] = valeur / sum_dirt
			print (valeur / sum_dirt)
		 end
		
		print (dump(dirt_ratio))
		
		
		
		local tasx = 0
		local tasz = 0
		local start_tasx = center_map_x - (dump_length * dump_nb / 2)
		local start_tasz = center_map_z - (dump_width * dump_nb / 2)
		
		clear_node ({x=start_tasx, y=floor_level + 1, z=start_tasz},{x=start_tasx + (dump_length * dump_nb),y=floor_level + 25 + 1,z=start_tasz + (dump_width * dump_nb)})
		
		for index, valeur in pairs(dirt_ratio) do
			-- get texture
			local texture = "default:desert_stone_block"
			for id, text in pairs (matiere_texture) do
				if string.find (index, id) ~= nil then
					texture = text
				end
			end
			datacraft_build_heap_viz (start_tasx + tasx * dump_length,floor_level + 1,start_tasz + tasz * dump_width, 
				dump_width, dump_length, 25, valeur, texture)
			tasx = tasx + 1
			if tasx >= dump_nb then
				tasx = 0
				tasz = tasz + 1
			end
			
		end
		-- datacraft_build_dirt_viz (50,0,75,100, 76, 25, data, datapercent, data_name, texture_name)
		
        end)
        
		return true, "Décharge OK"
	end,
})

minetest.register_chatcommand("test_data", {
	params = "",
	description = "Send text to chat",
	privs = {talk = false},
	func = function( _ , text)        
		minetest.chat_send_all("Récupération des dechets en cours ...")
        http_api.fetch({
            url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=matieres-collectees-en-decheteries-et-plateformes-de-vegetaux-a-rennes-metropole&facet=site&facet=annee&facet=matiere",
            timeout = 50
         }, function (res)
        local text =  dump(res.data)
		print (text)
        local data2 = minetest.parse_json(text)
        data2 = minetest.parse_json(data2)
        print (dump(data2))
        local data = {}
		local data_name = {}
         for i=1,10 do  
            minetest.chat_send_all(data2.facet_groups[3].facets[i].name)
            minetest.chat_send_all(data2.facet_groups[3].facets[i].count)
            
			--sgdo_bar(20,10+(i*2),data2.facet_groups[3].facets[i].count, texture_name[i])
			-- table[data2.facet_groups[3].facets[i].name] = data2.facet_groups[3].facets[i].count
			table.insert (data, data2.facet_groups[3].facets[i].count)
			table.insert (data_name, tostring(data2.facet_groups[3].facets[i].name))
			
			
         end
		 dome (50,76,0, 10, "default:stone_with_iron")
		 dome_scale (50,76,20, 10, 1,0.5,0.5,"default:brick")
		 
		 print (dump(data))
		 print (dump(data_name))
		 print ("table content")
		 local sum = sum_array(data)
		 local datapercent = {}
		 for index, valeur in ipairs(data) do
			table.insert (datapercent, valeur/sum)
		 end
		 print (sum)
		 print (dump(datapercent))
		 local vec = vector_center ({x=0,y=0,z=0},{x=1,y=1,z=1})
		 print (dump(vec))
        end)
        
		return true, "Décharge OK"
	end,
})

minetest.register_chatcommand("clear_data", {
	params = "",
	description = "Send text to chat",
	privs = {talk = false},
	func = function( _ , text)        
		minetest.chat_send_all("Effacement des dechets en cours ...")
        
         for i=1,10 do  
            
            erase_bar(20,10+(i*2),1000, "air")
         end
		 dome (50,76,0, 10, "air")
		 dome_scale (50,76,20, 10, 1,1,2,"air")
        
       
        
		return true, "Décharge OK"
	end,
})

minetest.register_chatcommand("test", {
	params = "",
	description = "Send text to chat",
	privs = {talk = false},
	func = function( _ , text)        
		minetest.chat_send_all("Test...")
        
         test_voxel ({x=50,y=76,z=50},{x=100,y=126,z=100}, 25)
		 
		return true, "Décharge OK"
	end,
})

minetest.register_chatcommand("clear", {
	params = "",
	description = "Send text to chat",
	privs = {talk = false},
	func = function( _ , text)        
		minetest.chat_send_all("Clear...")
        
         
		 clear_node ({x=10,y=76, z=0},{x=100,y=76+250,z=150})
		return true, "OK"
	end,
})

function vert_bar (px, py, pz, ph, typeof)
	for i = pz, ph do
		minetest.swap_node ({x=px, y=py, z=i}, {name=typeof})
	end
end




function test_voxel (p1, p2, r)
	local c_dirt = minetest.get_content_id("default:stone")	
	local vm = minetest.get_voxel_manip()
    local emin, emax = vm:read_from_map(p1,p2)
    local avx = VoxelArea:new{
        MinEdge = emin,
        MaxEdge = emax
    }
	local vmdata = vm:get_data()
	local dx = p2.x - p1.x
	local dy = p2.y - p1.y
	local dz = p2.z - p1.z
	
	for z = p1.z,p2.z do
		for y = p1.y,p2.y do
			for x = p1.x,p2.x do
				local idx = avx:index(x,y,z)
				print (idx)
				if distance2 (p1, {x=x,y=y,z=z}) < r*r then
					vmdata[idx] = c_dirt
				end	
			end	
		end	
	end
	vm:set_data(vmdata)
    vm:write_to_map(true)
end

function dome_scale (cx, cy, cz, rayon, scalex, scaley, scalez, typeof)
	local startx = math.floor(cx - rayon);
	local endx = math.ceil(cx + rayon);
	local startz = math.floor(cz - rayon);
	local endz = math.ceil(cz + rayon);
	
	local center = vector.new (cx,cy,cz)
	
	local vm = minetest.get_voxel_manip()
    local emin, emax = vm:read_from_map({x=math.floor(startx), y=math.floor(cy), z=math.floor(startz)}, {x=math.ceil(endx), y=math.ceil(cy+rayon), z=math.ceil(endz)})
    local avx = VoxelArea:new{
        MinEdge = emin,
        MaxEdge = emax
    }   
	print ("emin")
	print (dump(emin))
	print ("emax")
	print (dump(emax))	
    local vmdata = vm:get_data()
	
	for y = cy, cy + rayon do
		for z = startz, endz do
			for x = startx,endx do
				local v = vector.new (x,y,z)
				if distance2_scale (center, v, scalex, scaley, scalez) <= rayon * rayon then
					--minetest.swap_node (v, {name=typeof})
					local vi = avx:index(math.floor(x), math.floor(y), math.floor(z))
					print (vi)
					local machin = minetest.get_content_id(typeof) 
					vmdata[vi] =  machin
					-- minetest.set_node(v, {name=typeof})
				end
			end
		end
	end
	
	vm:set_data(vmdata)
    vm:write_to_map(true)
	
end

function dome (cx, cy, cz, rayon, typeof)
	local startx = cx - rayon;
	local endx = cx + rayon;
	local startz = cz - rayon;
	local endz = cz + rayon;
	
	local center = vector.new (cx,cy,cz)
	
	for y = cy, cy + rayon do
		for z = startz, endz do
			for x = startx,endx do
				local v = vector.new (x,y,z)
				if distance2 (center, {x=x,y=y,z=z}) <= rayon * rayon then
					minetest.swap_node ({x=x, y=y, z=z}, {name=typeof})
				end
			end
		end
	end
end


function do_bar(coor_x, coor_y, nb, typeof)
    for i=0,nb do
        -- print(typeof);
        --minetest.set_node({x=coor_x, y=10+i, z=coor_y}, {name=type})  
        --minetest.set_node({x=coor_x, y=9+i, z=coor_y}, {name=typeof})        
		minetest.swap_node ({x=coor_x, y=75+i, z=coor_y}, {name=typeof})
    end
end

function erase_bar(coor_x, coor_y,nb, type)
    for i=0,nb do
		local node = minetest.get_node({x=coor_x, y=9+i, z=coor_y})
		if node ~= nil then
			print (dump(node))
			minetest.set_node({x=coor_x, y=75+i, z=coor_y}, {name=type})
		end	
        
    end
end

minetest.register_privilege("fly", {
	description = "Player can fly around using the free_move mode.",
	give_to_singleplayer= true,
})

