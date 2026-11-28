-- approach.luau: once the carrier clears the player to land, the landing waits until the
-- player's ship flies through an approach marker off the carrier.
--
-- The player asks PERMISSION TO LAND as usual, and the carrier's bridge answers. Once the mission
-- has set `landing_cleared`, the answer gives the player's ship a Land order aimed at the whole
-- carrier. This script refuses that order and shows instead the red escort marker at the carrier's
-- approach point, with the mod's objective. When the player's ship flies into the marker, the
-- script gives the Land order itself, aimed at the carrier's component 0, which starts the
-- landing's cutaway at once.
--
-- Without `world.set_escort_marker`, in an OpenReliant that can't show the marker away from an
-- object, the script lets the landing go as in the game. It does so too in the first part of a
-- mission that has a second part, such as mission 25, where the 45th lands its Kamovs on the
-- Yamato before it flies out again.

local hooks = require("openreliant.hooks")
local records = require("openreliant.records")
local util = require("openreliant.util")
local world = require("openreliant.world")
local shared = require("shared")

-- Where the approach point stands off each carrier, in the carrier's frame (x to its right, y
-- down, z forward), in carrier radii, and which way the player flies through the marker: "aft"
-- toward the carrier's stern, "fore" toward its bow. Both come in from behind, as a ship lands
-- on a carrier, and were placed in game against the Reliant's and the Yamato's models.
local approaches = {
    reliant = { offset = vector.create(0.2, -0.2, -0.75), toward = "fore" },
    yamato = { offset = vector.create(-0.2, -0.12, -0.42), toward = "fore" },
}

-- How close to the marker's middle the player's ship has to come, in the marker's frame: the
-- marker is 1280 across and 1920 long.
local across = 800
local along = 1100

-- How long after the request the script waits for the carrier's answer, in seconds. The answer
-- comes 3 seconds after the request.
local answer_wait = 6

-- Whether this OpenReliant can show the marker away from an object.
local has_marker = (function()
    local ok, found = pcall(function()
        return world.set_escort_marker
    end)
    return ok and found ~= nil
end)()

local requested_at = nil -- the game time of the last PERMISSION TO LAND, while its answer may come
local approach = nil -- the approach under way: { carrier, offset, turn, objective }
local clock = 0

-- The approach of `carrier`, if it is one the mod knows.
local function approachOf(carrier)
    if carrier == nil or not carrier:is_valid() then
        return nil
    end
    local landing = carrier.landing
    local known = landing and approaches[landing]
    if known == nil then
        return nil
    end
    local turn
    if known.toward == "aft" then
        turn = { right = vector.create(-1, 0, 0), down = vector.create(0, 1, 0), forward = vector.create(0, 0, -1) }
    else
        turn = { right = vector.create(1, 0, 0), down = vector.create(0, 1, 0), forward = vector.create(0, 0, 1) }
    end
    return { carrier = carrier, offset = known.offset * carrier.radius, turn = turn }
end

-- The campaign's record of the mission that runs, and whether it runs its own file,
-- mission<number>.dte, rather than its second part, mission<number>1.dte.
local function missionRecord()
    local mission = world.mission
    if mission == nil then
        return nil, false
    end
    local ok, record = pcall(function()
        return records.missions[mission.number]
    end)
    if not ok then
        return nil, false
    end
    return record, mission.file:lower() == `mission{mission.number}.dte`
end

-- Whether the mod changes the landing in the mission that runs: not in the first part of a
-- mission that goes on to a second part, whose landing leads into it.
local function changesLanding()
    local record, own_file = missionRecord()
    return not (record ~= nil and own_file and record.second_part)
end

-- The number of the mod's objective in the mission that runs, from 0, if it has one. A second
-- part takes its objectives from the game's own table rather than the mission's record, so it
-- has none of the mod's.
local function objectiveNumber()
    local record, own_file = missionRecord()
    if record == nil or not own_file then
        return nil
    end
    local ok, names = pcall(function()
        return record.objectives
    end)
    if not ok or names == nil then
        return nil
    end
    local found = table.find(names, shared.objective)
    return found and found - 1
end

-- Ends the approach: the marker goes, and the objective takes `state`.
local function stop(state)
    if approach ~= nil then
        world.set_escort_marker(nil)
        if approach.objective then
            world.set_objective(approach.objective, state)
        end
    end
    approach = nil
end

local function start(carrier)
    approach = approachOf(carrier)
    if approach == nil then
        return false
    end
    world.set_escort_marker(carrier, approach.offset, approach.turn)
    approach.objective = objectiveNumber()
    if approach.objective then
        world.set_objective(approach.objective, "current")
    end
    return true
end

-- Whether the player's ship is in the marker.
local function inMarker()
    local carrier = approach.carrier
    local player = world.player
    local middle = util.to_world(carrier.position, carrier.orientation, approach.offset)
    local axes = carrier.orientation
    local turn = approach.turn
    local orientation = {
        right = axes.right * turn.right.x + axes.down * turn.right.y + axes.forward * turn.right.z,
        down = axes.right * turn.down.x + axes.down * turn.down.y + axes.forward * turn.down.z,
        forward = axes.right * turn.forward.x + axes.down * turn.forward.y + axes.forward * turn.forward.z,
    }
    local at = util.to_local(middle, orientation, player.position)
    return math.abs(at.x) < across and math.abs(at.y) < across and math.abs(at.z) < along
end

hooks.add("permission_to_land", function()
    if has_marker and changesLanding() then
        requested_at = clock
    end
end)

-- The carrier's answer gives the player's ship a Land order aimed at the whole carrier: it is
-- refused, and the approach starts, or goes on where the player asked again. The script's own
-- order, aimed at a component, goes through, as does a landing that no request led to, such as
-- the sending home for friendly fire, which ends the approach.
hooks.add("order_push", function(e)
    if e.order ~= "land" or not e.object.is_player or e.target.component ~= nil then
        return
    end
    local answered = requested_at ~= nil and clock - requested_at <= answer_wait
    requested_at = nil
    if not answered then
        stop("hidden")
        return
    end
    if approach ~= nil or start(e.target.object) then
        return false
    end
end)

-- Moose's reminders to land would only nag while the player flies to the marker.
hooks.add("radio_say", function(e)
    if approach ~= nil and e.speech:lower():find("moolnd_", 1, true) then
        return false
    end
end)

return {
    engine_handlers = {
        on_mission_start = function()
            requested_at = nil
            approach = nil
        end,
        on_mission_end = function()
            requested_at = nil
            approach = nil
        end,
        on_update = function(seconds)
            clock += seconds
            if approach == nil then
                return
            end
            local player = world.player
            if player == nil or not player:is_valid() or not approach.carrier:is_valid() or player.exploding then
                stop("hidden")
                return
            end
            if inMarker() then
                local carrier = approach.carrier
                stop("listed")
                player:give_order("land", carrier, 0)
            end
        end,
    },
}
