-- faces.luau: the cut missions' ships with the pilots the PC's missions give the same people and
-- the same kinds of ship. The Dreamcast's mission files number their pilots from an older pilot
-- table, so most of their lines would show someone else's face, and their other ships would fly,
-- taunt and report as pilots who don't belong in them, such as Coalition fighters flown by the
-- nanny's pilot.
local hooks = require("openreliant.hooks")
local world = require("openreliant.world")

-- For each mission:
-- - ships: the pilot of each ship that speaks, by its slot among the mission's ships, and of the
--   others that a type's pilot doesn't suit;
-- - pilots: the pilot each pilot number of its CommsFromPilot commands stands for;
-- - types: the pilot of every other ship of a type, the one the PC's missions most often give that
--   type. The player's wing keeps the pilots the game gives it.
local missions = {
    [12] = {
        -- Bandit's Patriot, the Reliant, Nicolai Petrov's Basilisk, the nanny, the Lueneberg and
        -- the Yamato.
        ships = { [5] = 6, [6] = 60, [9] = 16, [15] = 52, [16] = 193, [53] = 84 },
        -- Bandit, Moose and Diceman of the 45th Volunteers, the Reliant's bridge officer, Nicolai
        -- Petrov and the nanny's pilot.
        pilots = { [4] = 6, [102] = 4, [8] = 5, [116] = 60, [63] = 16, [115] = 52 },
        -- Coalition fighters, the Black Guard's Basilisks, the torpedo bombers, a Kurgan and the
        -- second nanny.
        types = { kossac = 24, sabre = 24, basilisk = 9, kamov = 123, kurgan = 47, nanny = 52 },
    },
    [13] = {
        -- Bandit's Patriot, Diceman's Tempest and the boarding ship, whose pilot is the Marine
        -- leader of mission 11's boarding ship; and Alpha 1, a 45th Volunteers pilot as in mission
        -- 11, and the Reliant.
        ships = { [5] = 6, [4] = 5, [7] = 188, [1] = 5, [6] = 60 },
        -- Stahl with his Marines, and Moose.
        pilots = { [103] = 72, [102] = 4 },
        -- The Black Guard's Basilisks, and Kurgans.
        types = { basilisk = 9, kurgan = 47 },
    },
    [17] = {
        -- Bandit's Grendel, the Reliant, the Gegarin, Gamma's two Hades, the Mitchell and the
        -- Cougars' two Hades.
        ships = { [5] = 0, [6] = 60, [7] = 56, [26] = 36, [27] = 36, [74] = 51, [112] = 22, [113] = 22 },
        -- Diceman and Moose of the 45th Tigers.
        pilots = { [8] = 120, [102] = 2 },
        -- Coalition fighters, Kurgans, the capital ships' comms officers, the cruisers' crews and the
        -- Cougars' Reapers.
        types = {
            sabre = 24, lagg = 24, loki = 24, kurgan = 47,
            gurevich = 23, sharov = 23, berijev = 23, zakov = 40, reaper = 22,
        },
    },
    [22] = {
        -- Diceman's Patriot, Alpha 1, the wing's leader, and the leaders of the Ronin and the
        -- Marauders.
        ships = { [5] = 1, [7] = 62, [202] = 186 },
        -- Moose of the 45th Tigers, who says the jump drive is online.
        pilots = { [102] = 2 },
        -- Coalition fighters, Kurgans, the convoy's escorts and capital ships, the cruisers' crews,
        -- the Ronin, the Yamato's bridge, the Mammoths, Gamma's Hades, the Rippers, and the
        -- Maulers' Coyotes and the Marauders' Mirages. The mission file gives the Ronin, the
        -- Yamato and the Mammoths no pilot at all, which leaves them Bandit's.
        types = {
            sabre = 24, lagg = 24, loki = 24, kurgan = 47,
            haidar = 69, azan = 37, salin = 67,
            badanov = 23, krasnaya = 23, troop_car = 23, gurevich = 23, sharov = 23, zakov = 40,
            naginata = 63, yamato = 84, mammoth = 127,
            hades = 36, ripper = 61, coyote = 49, mirage = 187,
        },
    },
}

local mission = missions[world.mission and world.mission.number]

-- Gives `object` the pilot its mission names for it, if there is one.
local function fit(object)
    local pilot = mission.ships[object.slot] or mission.types[object.type]
    if pilot then
        object.pilot = pilot
    end
end

local function fit_all()
    for _, object in world.objects() do
        fit(object)
    end
end

-- The ships added since the last step, which get their pilots then: the game gives a new ship the
-- pilot its record names only after it tells the scripts of the ship.
local added = {}

if mission then
    hooks.add("vm_command", function(e)
        if e.command == "comms_from_pilot" or e.command == "comms_from_pilot_once" then
            local arguments = e.arguments
            local pilot = mission.pilots[arguments[1]]
            if pilot then
                e.arguments = { pilot, arguments[2], arguments[3] }
            end
        end
    end)
    -- The ships of a flight group the mission creates get theirs once the command is done, with
    -- their records' pilots given, so that a line said right after comes from the right face.
    hooks.after("vm_command", function(e)
        if e.command == "create_flight_group" then
            fit_all()
        end
    end)
    -- Ships the game adds any other way get theirs on the next step.
    hooks.add("object_added", function(e)
        table.insert(added, e.object)
    end)
end

return {
    engine_handlers = {
        on_mission_start = function()
            if mission then
                fit_all()
            end
        end,
        on_step = function()
            if not mission or #added == 0 then
                return
            end
            for _, object in added do
                if object:is_valid() then
                    fit(object)
                end
            end
            table.clear(added)
        end,
    },
}
