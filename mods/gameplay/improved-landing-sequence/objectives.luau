-- objectives.luau: adds the approach objective to each mission of the campaign, after the
-- mission's own objectives. The global script shows it once the carrier clears the player to land.

local records = require("openreliant.records")
local shared = require("shared")

-- A mission has at most ten objectives.
local most = 10

for _, number in records.campaign do
    local mission = records.missions[number]
    local names = mission.objectives
    if #names < most and not table.find(names, shared.objective) then
        table.insert(names, shared.objective)
        mission.objectives = names
    end
end
