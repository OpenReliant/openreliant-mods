-- The StarLancer trial's two prequel missions as a campaign, with the trial's records for them.
local core = require("openreliant.core")
local ui = require("openreliant.ui")

-- The trial's ending, after its last mission: its blurb of the full game, for three seconds or
-- until a key.
local ending_seconds = 3
local ending_shown = 0

ui.register_screen("ending", {
    frame = function(seconds)
        ending_shown += seconds
        local height = ui.height
        local width = height * 4 / 3
        ui.picture(vector.create((ui.width - width) / 2, 0, 0), "blurb.png", vector.create(width, height, 0))
        if ending_shown >= ending_seconds then
            ending_shown = 0
            ui.go_to("main_menu")
        end
    end,
    key = function(_, down)
        if down then
            ending_shown = 0
            ui.go_to("main_menu")
        end
    end,
})

core.register_game_mode({
    name = "prequel",
    label = "PREQUEL",
    description = "The two prequel missions of the StarLancer trial. The Ronin wing patrols for pirates, then the war begins.",
    -- The trial flies them as its missions 1 and 2, with these objectives. Enriquez's last word
    -- after the loadout is the game's for missions 1 and 2, which the trial has too.
    missions = {
        {
            number = 91,
            as = 1,
            hologram = "prequel_m01.bik",
            last_word = "ms_speech\\enrbr_tag01.ut",
            objectives = {
                "Initiate Patrol for Pirate activity",
                "Rendezvous with supply convoy",
                "Engage Pirate wing",
                "Intercept Pirate Fighter",
                "Retreat to early warning station",
                "Destroy Bombers and torpedos",
                "Rendezvous with the Yamato",
                "Destroy enemy fighters",
                "Destroy incoming torpedos",
                "Come in to land",
            },
        },
        {
            number = 92,
            as = 2,
            hologram = "prequel_m02.bik",
            last_word = "ms_speech\\enrbr_tag02.ut",
            objectives = {
                "Initiate Patrol for Coalition Strike Force",
                "Rendezvous with Alliance Convoy",
                "Protect Alliance convoy from Coalition attack",
                "Investigate Coalition Signature Readings",
                "Destroy fighters and Kurgans",
                "Destroy Capital Ship's shield generator",
                "Intercept Troop carriers and destroy them",
                "Come in to land",
            },
        },
    },
    campaign = true,
    -- The trial briefs its missions in the Yamato's briefing room, debriefs them in the ITAC, and
    -- ends on its blurb.
    briefing_room = "yamato",
    debriefing = true,
    ending = "ending",
    records = "records.luau",
})
