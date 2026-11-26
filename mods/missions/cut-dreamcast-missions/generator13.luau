-- generator13.luau: the mod's own fix for finding the Kafelnikof's cloak generator in mission 13.
--
-- The generator is hidden under the base's cloak. Once the Kurgans are down, Diceman finds it and
-- sends its coordinates, and the mission's script points the player at it. The game never lets
-- anything aim at a cloaked ship, so the player could only find it by shooting the rock. Here, as
-- Diceman sends the coordinates, the generator comes out of the cloak and becomes the player's
-- target and the primary one.
local hooks = require("openreliant.hooks")
local world = require("openreliant.world")

-- Diceman's line as he sends the coordinates, and the generator's component.
local COORDINATES = "ms_dice13_002.ut"
local GENERATOR = 6

local function base()
    for _, object in world.objects() do
        if object.type == "kafelnikof" then
            return object
        end
    end
    return nil
end

hooks.add("radio_say", function(e)
    if e.speech ~= COORDINATES then
        return
    end
    local kafelnikof = base()
    if not kafelnikof then
        return
    end
    kafelnikof:uncloak_component(GENERATOR)
    world.set_primary_target(kafelnikof, GENERATOR)
    world.set_player_target(kafelnikof, GENERATOR)
end)
