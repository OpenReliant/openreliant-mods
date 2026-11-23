-- The loadout lets a ship carry at most 3 Jack Hammers. This raises the limit to 999, the same
-- limit as every other missile, so a ship can fill all of its hardpoints with them.
local records = require("openreliant.records")

records.loadout_missiles.jack_hammer.limit = 999
