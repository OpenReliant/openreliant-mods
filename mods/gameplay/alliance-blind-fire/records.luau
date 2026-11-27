-- Alliance Blind Fire: every Alliance fighter the player flies carries blind fire.
--
-- The game fits blind fire to the Predator, the Coyote, the Patriot, the Reaper, the Shroud and the
-- Phoenix alone (OpenReliant's src/engine/game/main.zig, `player_ships`). OpenReliant keeps it in
-- each ship type's record (`records.ship_types`, `blind_fire`), so this load script gives it to the
-- other six. The loadout then lists it with their specials, and TOGGLE BLINDFIRE works in them.
--
-- Each ship has a twin, the `t_` type, which the simulator's missions fly, so both get it.
--
-- Blind fire works as before: it aims the fighters' guns at the lead cursor when the target is
-- near the middle of the display, and they fire a third more slowly while it aims
-- (src/engine/game/guns.zig, `blindAim` and `refire`). The Nova Cannon and the turrets' guns still
-- fire along their muzzles.

local records = require("openreliant.records")

local FIGHTERS = { "naginata", "grendel", "crusader", "mirage", "tempest", "wolverine" }

for _, name in FIGHTERS do
    records.ship_types[name].blind_fire = true
    records.ship_types["t_" .. name].blind_fire = true
end
