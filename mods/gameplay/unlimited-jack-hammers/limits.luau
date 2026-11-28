-- The loadout lets a ship carry at most 3 Jack Hammers. This removes the limit, so a ship can fill
-- all of its hardpoints with them.
local records = require("openreliant.records")

records.missiles.jack_hammer.loadout_limit = nil
