-- fixes22.luau: the mod's own fixes for flaws of mission 22's draft script. The first two
-- otherwise leave the mission with no way to finish.
--
-- The Hades bombers: the script never checks whether they survive, and without their torpedoes
-- the convoy's cruisers or the Krasnaya can't be destroyed. They take no damage here.
--
-- The torpedoes: a torpedo hit is what destroys a cruiser, and the script counts a hit only on the
-- ship that torpedo was aimed at. A torpedo can end some other way: it strikes another ship in its
-- path, or the wreck of one, or the convoy's guns shoot it down. Its target then never goes. Here,
-- once a friendly torpedo is gone, its target explodes, as the script's own hit has it, unless it
-- already has. The script waits two seconds after a hit before its target explodes, so this waits
-- three.
--
-- The convoy's count: the Yamato comes once the script has counted six of the convoy's eight
-- defence ships destroyed. Its two Shavrovs can't be destroyed by fighters, so the player must
-- destroy all six of the others. The script counts each in a trigger that waits two seconds after
-- counting, and the game doesn't run a trigger again while it still runs, so a ship destroyed in
-- those two seconds goes uncounted and the Yamato never comes. Here the trigger doesn't wait.
--
-- The Badinov's escape: the script tells her to jump out, shows her going, and disables her at
-- once, which takes her out of the picture, so the camera shows nothing. Here she's disabled once
-- her jump is done, or after a minute.
local hooks = require("openreliant.hooks")
local world = require("openreliant.world")

-- The steps to wait after a torpedo is gone, 25 a second.
local GRACE = 75
-- The Badinov's record in the mission's file, which the script's commands name her by: ship 16,
-- each ship's record 76 bytes on from the one before.
local BADINOV = 201911
-- The steps her jump may take before she's disabled anyway.
local JUMP_LIMIT = 60 * 25
-- The text the convoy's count prints before it waits, by its place in the mission's file.
local CONVOY_SHIP_GONE = 296363

-- Each friendly torpedo in flight and the ship it's aimed at, as last seen.
local aimed = {}
-- The ships whose torpedoes are gone, and the step at which each explodes if it hasn't yet.
local due = {}
local steps = 0
-- The Badinov while she jumps out, and the step her jump began.
local leaving = nil
local leaving_since = 0
-- Whether the convoy's count has just printed its text, so the next command is its wait.
local counted = false

hooks.add("object_added", function(e)
    if e.object.type == "hades" then
        e.object.invulnerable = "full"
    end
end)

hooks.add("vm_command", function(e)
    if e.command == "print_debug_message" then
        counted = e.arguments[1] == CONVOY_SHIP_GONE
    elseif e.command == "wait" and counted then
        counted = false
        return false
    end
end)

hooks.add("vm_command", function(e)
    if e.command ~= "disable_object" or e.arguments[1] ~= BADINOV or e.arguments[2] == 0 then
        return
    end
    for _, object in world.objects() do
        if object.type == "badanov" and object.order == "jump_out" then
            leaving, leaving_since = object, steps
            return false
        end
    end
end)

return {
    engine_handlers = {
        on_step = function()
            steps += 1
            if leaving and (not leaving:is_valid() or leaving.order ~= "jump_out" or steps - leaving_since > JUMP_LIMIT) then
                if leaving:is_valid() then
                    leaving.disabled = true
                end
                leaving = nil
            end
            for torpedo, target in aimed do
                if not torpedo:is_valid() then
                    aimed[torpedo] = nil
                    if due[target] == nil then
                        due[target] = steps + GRACE
                    end
                end
            end
            for target, at in due do
                if steps >= at then
                    due[target] = nil
                    if target:is_valid() and target.side == "hostile" and not target.exploding then
                        print("fixes22: a torpedo aimed at " .. target.type .. " " .. target.slot .. " is gone without destroying it, so it explodes")
                        target:give_order("explode")
                    end
                end
            end
            for _, object in world.objects() do
                if object.class == "torpedo" and object.side ~= "hostile" and object.order == "torpedo" and object.target and object.target.object then
                    aimed[object] = object.target.object
                end
            end
        end,
    },
}
