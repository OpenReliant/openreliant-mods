-- Adds the master recordings that the CD player's 24 tracks don't play, in full, after them: the
-- album's tracks in the album's order, the game's other pieces, the movies' other music and the
-- characters' themes. The names are the album's titles where the album has the piece, and the
-- masters' own names otherwise. The Jukebox mod shows the pages they're on.
local records = require("openreliant.records")

local tracks = {
    -- The album.
    { piece = "Masters_Big Intro", name = "Big Intro" },
    { piece = "Masters_Alone", name = "Alone" },
    { piece = "Masters_Prepare for Battle", name = "Prepare for Battle" },
    { piece = "Masters_The Search", name = "The Search" },
    { piece = "Masters_Reliant Execution", name = "Reliant Execution" },
    { piece = "Masters_Fosters Last Stance", name = "Foster's Last Stance" },
    { piece = "Masters_The Search Part 7", name = "The Search Part 7" },
    { piece = "Masters_Reliant Funeral", name = "Reliant Funeral" },
    { piece = "Masters_The Search Part 10", name = "The Search Part 10" },
    { piece = "Masters_Yamato Funeral", name = "Yamato Funeral" },
    { piece = "Masters_Yamato Transfer", name = "Yamato Transfer" },
    { piece = "Masters_Final Battle", name = "Final Battle" },
    { piece = "Masters_Ending", name = "Ending" },
    -- The game's other pieces.
    { piece = "Masters_Mission 7", name = "Mission 7" },
    { piece = "Masters_Mission 8", name = "Mission 8" },
    { piece = "Masters_Searching Mission 2", name = "Searching Mission 2" },
    { piece = "Masters_Searching Mission 4", name = "Searching Mission 4" },
    { piece = "Masters_Searching Mission 8", name = "Searching Mission 8" },
    { piece = "Masters_Sim Pod 3", name = "Sim Pod 3" },
    { piece = "Masters_Sim Pod 6", name = "Sim Pod 6" },
    { piece = "Masters_Sim Pod 9", name = "Sim Pod 9" },
    -- The movies' other music.
    { piece = "Masters_Reliant Medal", name = "Reliant Medal" },
    { piece = "Masters_Reliant Transfer", name = "Reliant Transfer" },
    { piece = "Masters_Yamato Medal", name = "Yamato Medal" },
    { piece = "Masters_Yamato Execution", name = "Yamato Execution" },
    -- The characters' themes.
    { piece = "Masters_American Character Theme", name = "American Character Theme" },
    { piece = "Masters_Australian Character Theme", name = "Australian Character Theme" },
    { piece = "Masters_British Character Theme", name = "British Character Theme" },
    { piece = "Masters_Chinese Character Theme", name = "Chinese Character Theme" },
    { piece = "Masters_French Character Theme", name = "French Character Theme" },
    { piece = "Masters_German Character Theme", name = "German Character Theme" },
    { piece = "Masters_Italian Character Theme", name = "Italian Character Theme" },
    { piece = "Masters_Japanese Character Theme", name = "Japanese Character Theme" },
    { piece = "Masters_Scottish Character Theme", name = "Scottish Character Theme" },
    { piece = "Masters_South African Character Theme", name = "South African Character Theme" },
    { piece = "Masters_Spanish Character Theme", name = "Spanish Character Theme" },
}

for _, track in tracks do
    records.cd_player[#records.cd_player + 1] = track
end
