-- visite (c) by S GODIN and 3HitCombo
--
-- Dirt Visualisation Rennes is licensed under a
-- Creative Commons Attribution-ShareAlike 4.0 International License.
-- You should have received a copy of the license along with this
-- work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.






local place = {HFR={986, 30, -2900}, 
	JFK={-1985, 30, 750}, 
	PRE={3490, 30, 17.0},
	VU={-1283, 30, 852},
	POT={3301, 30, -2965},
	CITY={0, -990, 0},
	DECHET={0,10010,0} }

minetest.register_chatcommand("place", {
	params = "",
	description = "List place to visit",
	privs = {talk = false},
	func = function( pname , text)        
		
		
		local player = minetest.get_player_by_name (pname)
		if player ~= nil then
			local pos = player:get_pos()
			local placestr = ""
			for idx,value in pairs(place) do
				placestr = placestr .. tostring(idx) .. " "
			end
			minetest.chat_send_player(pname, placestr)
			
		end
		
		return true, "Wonderful places to visit"
	end
})

minetest.register_chatcommand("visite", {
	params = "<place>",
	description = "Teleporting virtual journey",
	privs = {talk = false},
	func = function( pname , text)        
		
		
		local player = minetest.get_player_by_name (pname)
		if player ~= nil then
			local pos = player:get_pos()
			for idx,value in pairs(place) do
				if string.find (idx, text) then
					player:set_pos({x=value[1], y=value[2], z=value[3]})
				end	
			end
		end
		
		return true, "Enjoy the place"
	end
})

