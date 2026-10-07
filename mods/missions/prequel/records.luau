-- The StarLancer trial's records for its prequel missions, which only this mod's game mode sees.
local records = require("openreliant.records")

-- The Kalan Shuttle.
local kalan = records.ships.kalan_shuttle
kalan.max_speed = 250
kalan.yaw_rate = 0.09
-- The Yakob Shuttle, which the trial's executable makes a fighter, so that the pirates fly and fight
-- like fighters.
local yakob = records.ships.yakob_shuttle
yakob.max_speed = 300
yakob.yaw_rate = 0.07
yakob.yaw_inertia = 0.9
yakob.pitch_rate = 0.07
yakob.pitch_inertia = 0.85
yakob.roll_rate = 0.15
yakob.roll_inertia = 0.9
yakob.shield_power = 14
yakob.armor_class = 16
yakob.shield_recharge = 15
records.ship_types.yakob_shuttle.class = "fighter"

-- The trial's text: the Ronin wing, its pilots and the pirates. The objectives' names are in
-- menu.luau, with the missions.
records.text[30] = "Takakatsu" -- was "RONIN LEADER"
records.text[32] = "Ronin Pilot" -- was "Frenchy"
records.text[33] = "Ronin Pilot" -- was "Bandit"
records.text[34] = "Ronin Pilot" -- was "Silky"
records.text[35] = "Ronin Pilot" -- was "Mayday"
records.text[36] = "Ronin Pilot" -- was "Trigger"
records.text[57] = "Ronin Pilot" -- was "Worm"
records.text[81] = "ENEMY PILOT" -- was "SABERS"
records.text[82] = "ENEMY LEADER" -- was "SABER LEADER"
records.text[131] = "Tanaka" -- was "Moose"
records.text[166] = "RONIN WING" -- was "THE 45TH"
records.text[337] = "Ronin Pilots" -- was "Alpha Pilots"
records.text[338] = "Ronin 1" -- was "Alpha 1"
records.text[339] = "Ronin 2" -- was "Alpha 2"
records.text[340] = "Ronin 3" -- was "Alpha 3"
records.text[341] = "Ronin 4" -- was "Alpha 4"
records.text[342] = "Ronin 5" -- was "Alpha 5"
records.text[343] = "Ronin Leader" -- was "Alpha Leader"
records.text[344] = "Ronin Wing" -- was "Alpha Wing"
records.text[644] = "LINCOLN" -- was "RELIANT"
records.text[668] = "ENEMY FIGHTER" -- was "Coalition Fighter"
records.text[677] = "RONIN 1" -- was "Ego"
records.text[1104] = "PIRATE" -- was "YAKOB SHUTTLE"

-- The trial's faces: Tanaka, in Moose's place, and the Ronin pilots wear the Ronin wing's helmet.
records.faces.moose_volunteers = { talking = "Ronin_Plt", laughing = "Ronin_Plt", dying = "Ronin_Plt_D" }
for _, pilot in { "frenchy", "silky", "mayday", "trigger", "worm", "ego", "bandit" } do
    records.faces[pilot] = { talking = "Ronin_Plt", dying = "Ronin_Plt_D" }
end

-- The trial's ITAC: its debriefings of missions 1 and 2, and its other sections closed.
records.itac_text[11] = "Good work pilot. This has been one hell of a day with all out war now officially declared and the loss of a significant number of our Battle Fleets; it is the dawn of a new era of survival for the Alliance."
records.itac_text[12] = "Unfortunately the loss of station LG9 will place an extra burden on our remaining early warning stations but you very likely saved the Yamato from a surprise attack and almost certain destruction. "
records.itac_text[13] = "The Coalition has finally showed their true colours and its now our job to defeat this enemy and send them to hell."
records.itac_text[14] = "That was a good performance out there today. Well-done pilot."
records.itac_text[15] = "Commander Enriquez"
records.itac_text[241] = "Good work pilot. Although we lost one convoy ship Alliance Command has reported that the remaining ships you saved made it back into port intact. The materials that were on board will prove vital to our efforts. The Captain was pleased with the way you handled this engagement with the enemy capital ships and heavy support craft. "
records.itac_text[242] = "With the enemy closing on all fronts our actions today have impressed Command and given the unit added credibility at a time when we need to prove ourselves once again to the rest of the Fleet and the people on our remaining colonies."
records.itac_text[243] = "Good work out there today.\n\nCommander Enriquez\n"
records.itac_text[244] = "A very average display out there pilot. We lost too many convoy ships and Alliance Command is less than happy with the loss of the vital materials on board those ships. The Captain was very displeased with the way you handled this engagement with the enemy capital ships, stay out of his way for a few days, he's spitting blood about this operation. "
records.itac_text[245] = "With the enemy closing on all fronts you failed to impress and prove your value to command. Get you act together pilot, I will not tolerate this level of performance. "
records.itac_text[246] = "Commander Enriquez"
records.itac_text[247] = "With the Prowler destroyed this mission was destined to be a complete and utter disaster. The Captain is considering removing your flight combat status after your lack of commitment and ability. Given another display like that I can guarantee you will be flying cargo loaders and transports for the rest of the war. "
records.itac_text[248] = "I expect more from my pilots; there will be no second chances."
records.itac_text[249] = "Commander Enriquez"
records.itac_text[250] = " "
records.itac_text[1641] = "Great work out there pilot. This has been one hell of a day with all out war now officially declared and the loss of a significant number of our Battle Fleets; it is the dawn of a new era of survival for the Alliance."
records.itac_text[1642] = "Your vigilance today not only saved station LG9 but also very likely saved the Yamato from a surprise attack and almost certain destruction. The Captain is proud of the way you performed and he will be sending medal citations to Command for all pilots involved in today's actions."
records.itac_text[1643] = "The Coalition has finally showed their true colours and its now our job to defeat this enemy and send them to hell."
records.itac_text[1644] = "An excellent performance pilot. "
records.itac_text[1645] = "Commander Enriquez"
records.itac_text[1770] = "Great job pilot. Alliance Command has reported that the convoy you saved has made it back into port intact. The materials that were on board will prove vital to our efforts. The Captain is extremely pleased with the way you handled this engagement with the enemy capital ships and heavy support craft. "
records.itac_text[1771] = "With the enemy closing on all fronts our actions today have impressed Command and given the unit added credibility at a time when we need to prove ourselves once again to the rest of the Fleet and the people on our remaining colonies. "
records.itac_text[1772] = "Klaus Steiner has sent a positive report on the your performance to Command. Keep up the good work, but remember we've got a long way to go, if we are going to win this war you need to keep our performance at this level.  "
records.itac_text[1773] = "That was great work out there today.\n\nCommander Enriquez\n"
records.itac_text[1811] = "News Reports are not available in the TRIAL VERSION"
records.itac_text[1812] = "Video Archives are not available in the TRIAL VERSION"
records.itac_text[1813] = "Fighter Ships are not available in the TRIAL VERSION"
records.itac_text[1814] = "Capital Ships are not available in the TRIAL VERSION"
records.itac_text[1815] = "Squadron Profiles are not available in the TRIAL VERSION"
records.itac_text[1816] = "Personnel Profiles are not available in the TRIAL VERSION"
records.itac_text[1817] = "Killboard is not available in the TRIAL VERSION"
