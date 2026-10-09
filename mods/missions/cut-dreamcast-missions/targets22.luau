-- targets22.luau: the mod's own help for mission 22, whose last part is crowded. When the Tigers
-- reach the convoy, the Badinov's shield generator becomes the player's target. Each time a
-- shield generator goes down, the nearest one left that can be hit becomes the target. If none can
-- be hit yet, such as the cruisers' before the Ronin call for help, the first one the mission makes
-- hittable becomes the target. Each is the primary target too, so the PRIMARY TARGET key goes back
-- to it after the player picks another target.
local hooks = require("openreliant.hooks")
local world = require("openreliant.world")
local lines = require("radio22_lines")

-- The line that stands for the text the mission prints as the Tigers reach the convoy.
local REACHED = "ms_moo22_006"

local started = false
-- Whether the last search found no shield generator that can be hit.
local waiting = false

-- Whether `part` is a shield generator the player can destroy now.
local function open_generator(part)
    return part.class == "shield_generator" and part.component and not part.destroyed and part.invulnerable ~= "full"
end

-- The shield generator of `ship` that the player can destroy now, if it has one.
local function generator_of(ship)
    for _, part in ship:parts() do
        if open_generator(part) then
            return part
        end
    end
    return nil
end

-- The enemy shield generator nearest the player that can be destroyed now, and its ship.
local function nearest_generator()
    local player = world.player
    local ship, generator, distance = nil, nil, math.huge
    for _, object in world.objects() do
        if object.side == "hostile" and not object.exploding then
            local part = generator_of(object)
            if part then
                local away = vector.magnitude(part.position - player.position)
                if away < distance then
                    ship, generator, distance = object, part, away
                end
            end
        end
    end
    return ship, generator
end

local function target(ship, generator)
    waiting = ship == nil
    if ship then
        world.set_player_target(ship, generator.component)
        world.set_primary_target(ship, generator.component)
    end
end

local function class_of(ship, component)
    for _, part in ship:parts() do
        if part.component == component then
            return part.class
        end
    end
    return nil
end

hooks.add("vm_command", function(e)
    if started or e.command ~= "print_debug_message" then
        return
    end
    local said = lines[e.arguments[1]]
    if said == nil or said.line ~= REACHED then
        return
    end
    started = true
    for _, object in world.objects() do
        if object.type == "badanov" and object.side == "hostile" then
            local part = generator_of(object)
            if part then
                return target(object, part)
            end
        end
    end
    target(nearest_generator())
end)

-- The mission makes a shield generator hittable: if the last search found none, it's the target.
hooks.after("vm_command", function(e)
    if waiting and e.command == "set_invulnerability" then
        target(nearest_generator())
    end
end)

hooks.add("destroyed", function(e)
    if not started or e.component == nil or class_of(e.object, e.component) ~= "shield_generator" then
        return
    end
    target(nearest_generator())
end)
