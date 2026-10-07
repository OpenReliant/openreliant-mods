-- What follows a death in the prequel. The trial plays no movie, so the prequel borrows the
-- retail game's: the Yamato's funeral, as the Ronin wing flies from the Yamato, and the pilot in
-- the enemy's hands for a capture.
local core = require("openreliant.core")
local hooks = require("openreliant.hooks")

hooks.add("mission_lost", function(e)
    if core.game_mode ~= "prequel:prequel" then
        return
    end
    if e.ending == "destroyed" then
        e.movie = "new_funeral2.bik"
    elseif e.ending == "captured" then
        e.movie = "int.bik"
    end
end)
