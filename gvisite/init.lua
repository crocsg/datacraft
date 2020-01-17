-- teleport mod

--
-- load place x,y,z position
--
dofile(minetest.get_modpath("gvisite").."/places.txt")
local place = _gvisite_place


--
-- user context
--
local _contexts = {}
local function get_context(name)
    local context = _contexts[name] or {}
    _contexts[name] = context
    return context
end

minetest.register_on_leaveplayer(function(player)
    _contexts[player:get_player_name()] = nil
end)

--
-- register compass
--
minetest.register_craftitem("gvisite:compass", {
    description = "Magic teleport",
    inventory_image = "compass.png",
	on_use = function (itemstack, user, pointed_thing)
			local name = user:get_player_name()
			showform (name , "") 
			return nil
		end,
})


--
-- Formspec callback
--
minetest.register_on_player_receive_fields (function (player,formname,fields)
	if formname ~= "gvisite:form" then
		print ("not correct form")
		return
	end
	
	--print ("fields =============================")
	--for k,v in pairs(fields) do
	--	print (k,v)
	--end
	--print ("====================================")
	
	local name = player:get_player_name()
    local context = get_context(name)
    
	
	if fields.Place then
		local evt = minetest.explode_textlist_event(fields.Place)
		--print ("event:",evt.type," ", evt.index)	
		--print ("place", place[evt.index])
		local a = 1
		for k,v in pairs(place) do
			if a == evt.index then
				--print ("place ", k, " ", v, " ", v.comment)
				context["location"] = v
			end
			a = a + 1
		end
		
		-- double click on location
		if (evt.type == "DCL") then
			if context.location then
				-- teleport the player
				player:set_pos({x=context.location[1], y=context.location[2], z=context.location[3]})
				minetest.close_formspec (name, "gvisite:form")
			end	
			end
	end
	
	if fields.exit then
		
		if context.location then
			-- teleport the player
			player:set_pos({x=context.location[1], y=context.location[2], z=context.location[3]})
		end
		
	end
	
	
end)

--
-- display formspec
--
function showform (pname , text)        
	local player = minetest.get_player_by_name (pname)
	print (player)
	if player ~= nil then
		print ("build place")

		-- build place list
		local str = ""
		for k, v in pairs(place) do
			print (k,v.comment)
			str = str .. k .. " " .. v.comment ..","
		end
		str = str:sub(1, -2)
		--str = table.concat (place,",")
		print (str)
		minetest.show_formspec(pname, 
			"gvisite:form",
            "size[10,10]" ..
            "label[0,0;Allez à...]" ..
            "textlist[1,1;8,7;Place;"..str.."]"..
			"button_exit[6,9;2,1;exit;Aller..]"..
			"button_exit[2,9;2,1;exit;Annuler]")
	end
		
	return true, ""
end

	
--
-- register command
--		
minetest.register_chatcommand("go", {
	params = "",
	description = "List place to visit",
	privs = {talk = false},
	func = function (pname , text)
		showform (pname, text)
	end,	
})



