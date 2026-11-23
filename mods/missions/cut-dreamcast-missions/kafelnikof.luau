-- kafelnikof.luau: the mod's own fix for how the Kafelnikof cloaks in mission 13, the only mission
-- that places the base.
--
-- The game cloaks only the base's parts on its list, its machinery, and leaves the rest in sight.
-- The list leaves out the turrets, so they hang in space around the hidden base, though their
-- models can cloak. Here they cloak with the base. `generator13.luau` brings the cloak generator
-- out of the cloak once the wing finds it.
local records = require("openreliant.records")

local kafelnikof = records.ship_types.kafelnikof
local parts = kafelnikof.cloaking_parts
for _, part in { "Rus Sml tur base", "Rus Sml Gun 1", "Rus Sml Gun 2", "Rus Big Tur Base", "Rus Big Tur Guns" } do
    table.insert(parts, part)
end
kafelnikof.cloaking_parts = parts
