-- kafelnikof.luau: the mod's own fix for how the Kafelnikof cloaks in mission 13, the only mission
-- that places the base.
--
-- The game cloaks only the base's parts on its list, its machinery, and leaves the rest in sight.
-- The list leaves out the turrets, so they hang in space around the hidden base, though their
-- models can cloak. It also holds the cloak generator, so the player can't see it on the cloaked
-- rock, and the game never lets anything target a cloaked ship, so the mission's script can't
-- point the player at it either. Here the turrets cloak with the base, and the generator stays in
-- sight, as Diceman's "There it is" has it.
--
-- An OpenReliant without the list in the ship types' records (`cloaking_parts`, OpenReliant#1564)
-- leaves the base as the game has it.
local records = require("openreliant.records")

local kafelnikof = records.ship_types.kafelnikof
local found, parts = pcall(function()
    return kafelnikof.cloaking_parts
end)
if found and parts then
    local cloaking = {}
    for _, part in parts do
        if part ~= "Kaf shield gen" then
            table.insert(cloaking, part)
        end
    end
    for _, part in { "Rus Sml tur base", "Rus Sml Gun 1", "Rus Sml Gun 2", "Rus Big Tur Base", "Rus Big Tur Guns" } do
        table.insert(cloaking, part)
    end
    kafelnikof.cloaking_parts = cloaking
end
