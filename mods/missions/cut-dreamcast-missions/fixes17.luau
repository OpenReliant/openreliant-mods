-- fixes17.luau: the mod's own fix for a flaw of mission 17's draft script, which otherwise can
-- leave it with no way to finish.
--
-- The Cougars' torpedoes: the Gegarin is destroyed once every torpedo of the bombers' first run is
-- gone and the second run's has hit her. The script aims each torpedo at one of her parts, by the
-- numbers of an older model of her class. A torpedo goes off against whatever part it strikes, so
-- the first torpedoes can destroy the parts the later ones are aimed at, and the guns can destroy
-- them too. A torpedo aimed at a part that's gone has nothing to fly at: it flies on for good, and
-- the mission waits for it. Here a friendly torpedo aimed at a part of the Gegarin that's gone, or
-- that loses its part on the way, is aimed at her hull.
local hooks = require("openreliant.hooks")
local world = require("openreliant.world")

-- The orders a torpedo flies at its target with, and is launched with.
local FLYING = { torpedo = true, find_new_target = true, launch = true }

-- The Gegarin, a Pukov, aimed at by each friendly torpedo, by the torpedo's slot.
local aimed = {}

-- The component that is `ship`'s hull, or nil to aim at the ship as a whole.
local function hull_of(ship)
    for _, part in ship:parts() do
        if part.class == "hull" and part.component then
            return part.component
        end
    end
    return nil
end

-- Whether `ship`'s component `component` is gone.
local function gone(ship, component)
    for _, part in ship:parts() do
        if part.component == component then
            return part.destroyed
        end
    end
    return true
end

hooks.add("order_push", function(e)
    local torpedo, target = e.object, e.target
    if torpedo.class ~= "torpedo" or torpedo.side == "hostile" then
        return
    end
    local ship = target.object
    if ship == nil or ship.type ~= "pukov" then
        return
    end
    aimed[torpedo.slot] = ship
    if target.component and gone(ship, target.component) then
        e.target = { object = ship, component = hull_of(ship) }
    end
end)

hooks.add("object_removed", function(e)
    aimed[e.object.slot] = nil
end)

return {
    engine_handlers = {
        on_step = function()
            for _, torpedo in world.objects() do
                local ship = aimed[torpedo.slot]
                if ship and not FLYING[tostring(torpedo.order)] then
                    local aiming = ship:is_valid() and not ship.exploding and not torpedo.exploding
                    if aiming and torpedo:give_order("find_new_target", ship, hull_of(ship)) then
                        print("fixes17: a torpedo lost its part of the Gegarin, so it's aimed at her hull")
                    else
                        aimed[torpedo.slot] = nil
                    end
                end
            end
        end,
    },
}
