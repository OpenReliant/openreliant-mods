-- yamato22.luau: the mod's own ending for mission 22, which the Dreamcast's script doesn't have.
-- Once most of the convoy's defences are down, the mission calls the Yamato in and tells the Tigers
-- to land, and leaves whatever is left of the convoy fighting. As the Yamato arrives, the convoy's
-- ships that can still fly jump out, as the ITAC's news after the mission has it: the Coalition
-- retreated to its own lines. The Yamato then picks off the big ships left behind, one at a time:
-- she flies at each until her guns reach it, and holds there while they finish it.
local hooks = require("openreliant.hooks")
local orders = require("openreliant.orders")
local records = require("openreliant.records")
local world = require("openreliant.world")
local lines = require("radio22_lines")

-- The line that stands for the text the mission prints once the Yamato has jumped in.
local ARRIVED = "ms_dice22_050"
-- The steps between looks at what's left, 25 a second.
local EVERY = 50
-- How close she comes to a ship before she stops for her guns: a little inside her Huge Gun's
-- reach, its shots' speed times the ticks they last.
local huge_gun = records.guns.allied_huge_gun
local REACH = 0.8 * huge_gun.speed * huge_gun.range

-- The big ships, which she goes after: the convoy's cruisers, the Zakovs, are of class other.
-- Fighters only retreat.
local big = { capital = true, support = true, other = true }

-- The orders that carry a ship into or out of the mission.
local jumping = {
    jump_in = true, jump_out = true, jump_in_spread = true, jump_out_spread = true,
    warp_in = true, warp_out = true, fixed_gate_jump_in = true, fixed_gate_jump_out = true,
}

local arrived = false
local steps = 0
local target = nil

local function the_yamato()
    for _, object in world.objects() do
        if object.type == "yamato" then
            return object
        end
    end
    return nil
end

local function enemy(object)
    return object.side == "hostile" and (big[object.class] or object.class == "fighter")
end

-- Whether a ship can still fly: it has no engine parts, or one that isn't destroyed.
local function can_fly(ship)
    local engines, working = 0, 0
    for _, part in ship:parts() do
        if part.class == "engine" and not part.damaged then
            engines += 1
            if not part.destroyed then
                working += 1
            end
        end
    end
    return engines == 0 or working > 0
end

-- The convoy's ships that can still fly jump out.
local function retreat()
    for _, object in world.objects() do
        if enemy(object) and can_fly(object) and not jumping[object.order] then
            orders.clear(object)
            object:give_order("jump_out")
        end
    end
end

-- The nearest big ship left behind that isn't leaving.
local function next_target(yamato)
    local best, best_distance = nil, math.huge
    for _, object in world.objects() do
        if object.side == "hostile" and big[object.class] and not jumping[object.order] then
            local distance = vector.magnitude(object.position - yamato.position)
            if distance < best_distance then
                best, best_distance = object, distance
            end
        end
    end
    return best
end

hooks.add("vm_command", function(e)
    if not arrived and e.command == "print_debug_message" then
        local said = lines[e.arguments[1]]
        if said and said.line == ARRIVED then
            arrived = true
            retreat()
        end
    end
end)

return {
    engine_handlers = {
        on_step = function()
            steps += 1
            if not arrived or steps % EVERY ~= 0 then
                return
            end
            local yamato = the_yamato()
            if yamato == nil or jumping[yamato.order] then
                return
            end
            if target == nil or not target:is_valid() or jumping[target.order] then
                target = next_target(yamato)
                if target == nil then
                    return
                end
            end
            local gap = vector.magnitude(target.position - yamato.position) - target.radius - yamato.radius
            local flying_at_it = yamato.order == "fly" and yamato.target and yamato.target.object == target
            if gap > REACH then
                if not flying_at_it then
                    yamato:give_order("fly", target)
                end
            elseif flying_at_it then
                -- Within her guns' reach: she stops, and they finish it.
                orders.cancel(yamato)
            end
        end,
    },
}
