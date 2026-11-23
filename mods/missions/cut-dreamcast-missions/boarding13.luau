-- boarding13.luau: the mod's own balance for the boarding ship in mission 13.
--
-- After each drop-off and pickup, the script sends the boarding ship to "Limpet hold off point" to
-- wait out of the fight, far from the base. The Basilisks the script then sends at the wing and at
-- the boarding ship jump in on the far side of the base and hunt it there, and in the restored
-- mission they destroyed it within seconds of reaching it. Here it can't be harmed while it holds
-- off, from the moment it is sent there until it is sent back in; on its runs to and from the base
-- the wing still has to protect it.
local world = require("openreliant.world")

-- "Limpet hold off point", where the mission places it.
local HOLD_OFF = vector.create(-850.0217, -436.4081, -117328.53)

local boarding_ship = nil
-- Whether this script made the boarding ship invulnerable, and so may make it vulnerable again.
local protecting = false

local function holding_off(ship)
    if ship.order ~= "fly" then
        return false
    end
    local target = ship.target
    local point = target and target.object
    return point ~= nil and vector.magnitude(point.position - HOLD_OFF) < 1
end

return {
    engine_handlers = {
        on_update = function()
            if not (boarding_ship and boarding_ship:is_valid()) then
                boarding_ship = nil
                for _, object in world.objects() do
                    if object.type == "limpet_car" then
                        boarding_ship = object
                    end
                end
                if not boarding_ship then
                    return
                end
            end
            local waiting = holding_off(boarding_ship)
            if waiting and not protecting then
                boarding_ship.invulnerable = "full"
                protecting = true
            elseif not waiting and protecting then
                boarding_ship.invulnerable = "none"
                protecting = false
            end
        end,
    },
}
