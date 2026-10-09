-- radio22.luau: mission 22 prints its draft radio as debug text, and says nothing. As the mission
-- reaches each text, this has the radio say the line that stands for it (radio22_lines.luau), with
-- its speaker's face, and sets the mission's objectives, which its own script never does. Their
-- names are in campaign.luau.
--
-- The script's waits between texts are timed for reading, shorter than the lines take to say, so
-- the voices would fall behind the mission. The wait after a voiced text is held while the radio
-- is busy, so the mission goes on once the line is said, as the PC's missions wait for their
-- speech.
local hooks = require("openreliant.hooks")
local radio = require("openreliant.radio")
local records = require("openreliant.records")
local world = require("openreliant.world")
local lines = require("radio22_lines")

-- The pilots whose faces show each film, from the records, by the names the radio's window shows
-- over them. Many share a film, such as the 45th Tigers' pilots, so a line's speaker picks the one
-- named for them, such as Stalker, or else the first with the film.
local pilots_with = {}
for number, face in records.faces do
    local named = pilots_with[face.talking]
    if named == nil then
        named = { first = number }
        pilots_with[face.talking] = named
    end
    local name = records.text[face.name]
    if name and named[name:lower()] == nil then
        named[name:lower()] = number
    end
end

local function pilot_for(said)
    local named = pilots_with[said.face]
    if named == nil then
        return nil
    end
    return named[said.speaker:lower()] or named.first
end

-- The objective each moment makes current, numbered from 0 as campaign.luau names them. The one
-- current before is listed again.
local current_from = {
    ms_dice22_006 = 1, -- The Laggs jump in: destroy the scouts.
    ms_moo22_006 = 2, -- Arriving at the convoy: disable the Badinov.
    ms_had22_001 = 5, -- Hades come in: protect the bombers.
    ms_had22_002 = 5,
    ms_had22_004 = 5,
    ms_dice22_034 = 3, -- The Badinov destroyed: the troop carriers.
    ms_stal22_010 = 3, -- Or escaped.
    ms_enq22_010 = 4, -- The troop carriers destroyed: the Krasnaya's shields.
    ms_enq22_017 = 6, -- Enriquez calls them in: land on the Yamato.
}
local current = 0
-- Whether the last text the script printed was voiced, so its next wait is held.
local voiced = false

local function make_current(objective)
    if objective == current then
        return
    end
    world.set_objective(current, "listed")
    world.set_objective(objective, "current")
    current = objective
end

hooks.add("vm_command", function(e)
    if e.command == "wait" and voiced then
        if radio.busy() then
            e.result = "hold"
            return false
        end
        voiced = false
        return
    end
    if e.command ~= "print_debug_message" then
        return
    end
    local said = lines[e.arguments[1]]
    voiced = said ~= nil
    if said == nil then
        return
    end
    local pilot = pilot_for(said)
    if pilot then
        -- Queued, as the texts can come one after another.
        radio.say_pilot(pilot, said.line .. ".ut", { mode = "queued" })
    else
        print("radio22: no pilot has the face " .. said.face .. " for " .. said.line)
    end
    local objective = current_from[said.line]
    if objective then
        make_current(objective)
    end
end)
