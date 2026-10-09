-- campaign.luau: the Dreamcast's missions 12, 13, 17 and 22 in the campaign, where their numbers
-- put them: 12 and 13 after 11, 17 after 16, and 22 after 21.
local records = require("openreliant.records")

local campaign = records.campaign
for _, mission in { 12, 13, 17, 22 } do
    if not table.find(campaign, mission) then
        table.insert(campaign, mission)
    end
end
table.sort(campaign)
records.campaign = campaign

-- What the game lacks for them. The game has no hologram for these missions, so Enriquez speaks
-- her briefing over the room, while another mission's hologram that fits plays on the screen
-- without its sound, one from the disc the mission's carrier reads: the Allied fleet for the
-- Reliant's defence (12), a Coalition base (13), a strike on a Coalition carrier near asteroids
-- (17), and a Coalition convoy (22).
--
-- The date the launch shows is "aaaa" in the game's text for all four; the ITAC's table of mission
-- dates has their real ones, and matches the launch's for the other missions, except for mission
-- 18's month and mission 25's year. A date another mod has already given is left as it is. The
-- game names no objectives for mission 22, whose own script sets none: radio22.luau sets them as
-- it goes.
local restored = {
    [12] = { hologram = "new_m05.bik", speech = "dreamcast_brief12.ut", date = "February 2, 2161" },
    [13] = { hologram = "new_m16.bik", speech = "dreamcast_brief13.ut", date = "February 21, 2161" },
    [17] = { hologram = "new_m14.bik", speech = "dreamcast_brief17.ut", date = "June 6, 2161" },
    [22] = {
        hologram = "new_m20.bik",
        speech = "dreamcast_brief22.ut",
        date = "October 17, 2161",
        objectives = {
            "Find the Coalition convoy",
            "Destroy the scouts before they warn the convoy",
            "Disable the Badinov: destroy its shield generator, then its engines",
            "Destroy the troop carriers",
            "Take down the Krasnaya's shields for the bombers",
            "Protect Gamma's bombers",
            "Land on the Yamato",
        },
    },
}
for number, given in restored do
    local mission = records.missions[number]
    mission.hologram = given.hologram
    mission.speech = given.speech
    if mission.date == "aaaa" then
        mission.date = given.date
    end
    if given.objectives then
        mission.objectives = given.objectives
    end
end
