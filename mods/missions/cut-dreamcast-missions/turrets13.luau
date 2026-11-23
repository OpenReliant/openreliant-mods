-- turrets13.luau: the mod's own balance for the Kafelnikof's turrets in mission 13.
--
-- The base's model left 13 of its 16 turrets unable to fire, and the mod's model lets them
-- (`patch_kafelnikof.py`). A turret aims at any ship not of its side, so they wore down the boarding
-- ship's shields as it docked, before the Basilisks the mission sends at it arrive. Here a turret
-- never aims at the boarding ship: the turrets step before the scripts in each game frame, and a
-- turret that picks a target fires at it no sooner than the next, so one picked is dropped first.
local world = require("openreliant.world")

local base = nil

return {
    engine_handlers = {
        on_update = function()
            if not (base and base:is_valid()) then
                base = nil
                for _, object in world.objects() do
                    if object.type == "kafelnikof" then
                        base = object
                    end
                end
                if not base then
                    return
                end
            end
            for _, turret in base:turrets() do
                local target = turret.target
                if target and target.object and target.object.type == "limpet_car" then
                    turret.target = nil
                end
            end
        end,
    },
}
