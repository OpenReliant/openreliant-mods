-- Drops the instructor's first line in mission 29, msia_ins_001.ut. The mission's script waits for
-- each line to end, so it carries on at once.
local hooks = require("openreliant.hooks")
local world = require("openreliant.world")

hooks.add("radio_say", function(e)
    if world.mission and world.mission.number == 29 and e.speech:lower():find("msia_ins_001", 1, true) then
        return false
    end
end)
